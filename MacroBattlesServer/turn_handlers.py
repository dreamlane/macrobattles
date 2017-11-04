## turn_handlers.py Handles API calls involving turns in the game.
## These should only be callable by admins, and cron jobs set to call them.
import logging
import random

from google.appengine.ext import ndb

from constants_structures import HARVESTING_CAMP_KEY
from constants_structures import STRUCTURE_TYPE_INT_MAPPING
from resource_utils import determineHarvestRate

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
  def resolveOrders():
    # Get the orders.
    # TODO: Re-verify them.
    # Execute them.
    pass # TODO

  @staticmethod
  def resolveCombat():
    # Get all of the map tiles.
    # Find the ones that are contested.
    # Resolve combat on the contested tiles. (including structure damage.)
    pass # TODO

  @staticmethod
  def handleTurn():
    """ Makes a turn happen. """
    # Step 1: Payout resources.
    camp_query = PlayerStructure.query(PlayerStructure.structure_type ==
        STRUCTURE_TYPE_INT_MAPPING[HARVESTING_CAMP_KEY])
    if camp_query.count() > 0:
      logging.info('got me some camps')
      TurnHandler.payoutResources(camp_query.fetch())
    else:
      logging.info('aint got no camps')
    # Step 2: Handle all orders.
    TurnHandler.resolveOrders()
    # Step 3: Resolve Combat.
    TurnHandler.resolveCombat()
    # Step 4: Inform the clients?
    pass # TODO
