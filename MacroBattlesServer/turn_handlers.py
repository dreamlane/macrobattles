## turn_handlers.py Handles API calls involving turns in the game.
## These should only be callable by admins, and cron jobs set to call them.
import logging
import random

from google.appengine.ext import ndb

from constants_orders import MOVE_KEY
from constants_orders import BUILD_CAMP_KEY
from constants_orders import ORDER_TYPE_INT_MAPPING
from constants_structures import HARVESTING_CAMP_KEY
from constants_structures import STRUCTURE_TYPE_INT_MAPPING
from resource_utils import determineHarvestRate
from battle_utils import resolveAttack

from models import HarvestingCamp
from models import MapTile
from models import Order
from models import PlayerStructure
from models import Resource

# TODO: figure out if the class + static method approach is better than the
# file full of functions approach.
class TurnHandler():
  """ This is the handler for making a turn happen. """

  @staticmethod
  def payoutResources(camps):
    """ Grabs all of the camp type structures and gives resources to owners."""
    # TODO: If this starts to become costly, look into optimizing this via
    # Keys-only queries.

    logging.info('called it')

    # map the players that need to updated into a cache.
    players_to_update = {}
    # Map the resources that need to be updated into a cache.
    resources_to_update = {}

    for camp in camps:
      logging.info('camp: ' + str(camp))
      # TODO: Add some contested area checking.
      # TODO: Add error checking on all of this.
      # Get the player who owns camp, first from the cache, then the store.
      owner_key = camp.owner_key
      owner = None
      if owner_key in players_to_update:
        owner = players_to_update[owner_key]
      else:
        owner = camp.owner_key.get()
      tile_resource = camp.harvesting_camp_data.tile_resource_key.get()
      template_key = tile_resource.resource_template

      # If the player already has the resource, up the quantity.
      for resource_key in owner.resources:
        # Get the resource from the cache first, otherwise get it from store.
        resource = None
        if resource_key in resources_to_update:
          logging.info('getting resource from dict')
          resource = resources_to_update[resource_key]
        else:
          logging.info('getting resource from resource_key: ' +str(resource_key))
          resource = resource_key.get()
        if not resource:
          logging.error('Resource is None. Key is: ' + str(resource_key))
          continue
        if resource.resource_template == template_key:
          resource.quantity += determineHarvestRate(tile_resource)
          resources_to_update[resource_key] = resource
          # In python, if you break a for loop, the else does not trigger.
          # This is the for/else logic...
          # http://book.pythontips.com/en/latest/for_-_else.html
          break
      # If the player doesn't already have the resource, create one.
      else:
        # TODO: Find out if there is a way to put_multi this resource.
        owner.resources.append(
          Resource(
            resource_template = template_key,
            quantity = determineHarvestRate(tile_resource)
        ).put())
        players_to_update[owner_key] = owner
    # Now all of the resources and players to update should be ready to be put.
    entities_to_put = players_to_update.values() + resources_to_update.values()
    ndb.put_multi(entities_to_put)


  @staticmethod
  def resolveOrders(orders):
    # TODO: Re-verify the orders, so a camp can't be plopped down on a spot that
    # has become contested.
    entities_to_put = {}
    entity_keys_to_delete = []
    entities_to_create = []
    for order in orders:
      if order.order_type == ORDER_TYPE_INT_MAPPING[MOVE_KEY]:
        # TODO: Add error handling.
        move_order = order.move_order
        unit_key = order.unit_key
        # Update the unit so it can take an order next turn.
        unit = None
        if unit_key in entities_to_put:
          unit = entities_to_put[unit_key]
        else:
          unit = unit_key.get()
        # TODO: See if this code is needed. Does deleting the order auto remove
        # the keyproperty reference?
        # unit.order = None
        # Move the unit.
        unit.location_tile = move_order.destination_map_tile_key
        entities_to_put[unit_key] = unit

        # Check to see if the tile is now contested:
        # TODO: Optimize this eventually... figuring out contested state is ugly.
        map_tile = None
        if unit.location_tile in entities_to_put:
          map_tile = entities_to_put[unit.location_tile]
        else:
          map_tile = unit.location_tile.get()
        if not map_tile.is_contested:
          units_on_tile = map_tile.units.fetch()
          # Check for multiple players on the same tile.
          player_keys = [unit.owner_key]
          for tile_unit in units_on_tile:
            if tile_unit.owner_key not in player_keys:
              # More than one player has been found on the tile.
              player_keys.append(tile_unit.owner_key)
              map_tile.is_contested = True
              break
          if len(player_keys) < 2:
            tile_structures = map_tile.structures.fetch()
            for tile_structure in tile_structures:
              if tile_structure.owner_key not in player_keys:
                # More than one player has been found on the tile.
                player_keys.append(tile_structure.owner_key)
                map_tile.is_contested = True
          if len(player_keys) >= 2:
            map_tile.put()

      elif order.order_type == ORDER_TYPE_INT_MAPPING[BUILD_CAMP_KEY]:
        # TODO: Add error handling.
        build_camp_order = order.build_camp_order
        unit_key = order.unit_key
        # Building a camp consumes the worker.
        entity_keys_to_delete.append(unit_key)
        new_camp = PlayerStructure(
          structure_type = STRUCTURE_TYPE_INT_MAPPING[HARVESTING_CAMP_KEY],
          owner_key = unit_key.get().owner_key,
          harvesting_camp_data = HarvestingCamp(
            tile_resource_key = build_camp_order.tile_resource_key
          )
        )
        entities_to_create.append(new_camp)

      # Done with the order, set it to be deleted.
      entity_keys_to_delete.append(order.key)

    # Put and Delete all the entities.
    ndb.delete_multi(entity_keys_to_delete)
    ndb.put_multi(entities_to_put.values() + entities_to_create)

  @staticmethod
  def resolveCombat():
    contested_tiles = MapTile.query(MapTile.is_contested == True).fetch()
    if len(contested_tiles) > 0:
      for contested_tile in contested_tiles:
        # Key = player_key, Value = list of units the player owns.
        armies = {}
        # Key = player_key, Value = list of strutures the player owns.
        structures = {}
        units_on_tile = contested_tile.units.fetch()
        structures_on_tile = contested_tile.structures.fetch()
        # The use of setdefault below allows us to automatically create a dict
        # entry if one isn't there already.
        for unit in units_on_tile:
          armies.setdefault(unit.owner_key, []).append(unit)
        for structure in structures:
          structures.setdefault(structure.owner_key, []).append(structure)

        # To resolve combat, each unit randomly attacks an enemy unit.
        # There can be any number of players on a single tile.
        # Each unit will get to hit, even if they get killed this round.
        # For now, overkill is possible, meaning a unit with <= 0 health can get
        # hit multiple times.
        for player, army in armies.iteritems():
          targets = []
          for opponent in armies.keys():
            # Don't add the attacker's own units to the target list!
            if opponent != player:
              for opponent_unit in armies[opponent]:
                targets.append(opponent_unit)
          for unit in army:
            # Randomly choose a target and hit it!
            target = random.choice(targets)
            resolveAttack(unit, target)
        # TODO: attack the buildings if no units are present.

        # Now that the battle is done, delete all of the dead units.
        for army in armies.values():
          for unit in army:
            if unit.health <= 0:
              unit.key.delete()
        # TODO: Take the map tile out of contested state if there is no contest
        # remaining.

    else:
      logging.info('there is no combat to resolve.')

  @staticmethod
  def handleTurn():
    """ Makes a turn happen. """
    # Step 1: Payout resources.
    camp_query = PlayerStructure.query(PlayerStructure.structure_type ==
        STRUCTURE_TYPE_INT_MAPPING[HARVESTING_CAMP_KEY])
    if camp_query.count() > 0:
      TurnHandler.payoutResources(camp_query.fetch())
    else:
      logging.info('There are no camps, so payoutResources was not called.')

    # Step 2: Handle all orders.
    orders_query = Order.query()
    if orders_query.count() > 0:
      logging.info("Handling orders. There are: " + str(orders_query.count()))
      TurnHandler.resolveOrders(orders_query.fetch())
    else:
      logging.info('There are no orders to resolve.')
    # Step 3: Resolve Combat.
    TurnHandler.resolveCombat()
    # TODO: Add a turn counter, and turn counter logic for multi-turn Orders.
    # Step 4: Inform the clients?
    pass # TODO
