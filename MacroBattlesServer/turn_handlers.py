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

from models import HarvestingCamp
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
    # Get all of the map tiles.
    # Find the ones that are contested.
    # Resolve combat on the contested tiles. (including structure damage.)
    # Set the is_contested bit on tiles appropriatelye
    pass # TODO

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
