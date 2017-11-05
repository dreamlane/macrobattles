## orders_handlers.py Handles API calls involving Orders.
"""
    Orders are the way that a player informs the game what it is that they want
    To have happen when a turn resolves. This includes all of the following
    player initiated actions:
      - Move a Unit
      - Build a gathering camp
      - Equip a Unit
      - Craft an Item
    There are actions that can occur in real-time (not turn-based). Those
    actions are handled elsewhere.

    Any action that can affect the outcome of a multi-player interaction should
    be implemented as an Order.
"""
import logging

from google.appengine.ext import ndb

from models import BuildCampOrder
from models import MoveOrder
from models import Order

from constants_orders import MOVE_KEY
from constants_orders import BUILD_CAMP_KEY
from constants_orders import ORDER_TYPE_INT_MAPPING
from constants_units import WORKER_KEY
from constants_units import UNIT_TYPE_INT_MAPPING

class OrderHandler():
  """
    The order Handler class will keep the list of orders, and provide storage
    functionality as needed.
    NOTE: This code is unused, and is just an idea for if simple ndb commands
    end up being too costly. This layer can be used to reduce the number of
    read/write requests.
  """

  def __init__(self, orders={}):
    """
      @param orders A dictionary of orders, where the key is the turn, and the
                    value is a list of Order models. It should be used to when
                    initializing the OrderHandler from an already stored set of
                    orders in the DB.
    """
    self.orders = orders

  def addOrder(turn, order):
    """
      Adds an order to the local cache.
      @param turn An integer that represents the turn that the order will be
                  executed on.
      @param order An Order model.
    """
    # If the turn is already in the orders cache, add this order to it.
    if turn in self.orders:
      self.orders[turn].append(Order)
    # If the turn is not in the cache yet, add it with the order.
    else:
      self.orders[turn] = [order]

  def _removeTurnFromCache(turn):
    """
      Removes the turn from the cache. This should only be used after a turn has
      been completed, and all of it's orders have been completed.
      @param turn An integer that represents the turn as a key in the cache. All
                  orders from the given turn will be deleted.
    """
    if turn in self.orders:
      del self.orders[turn]

def isMoveValid(unit, target_tile):
  # TODO: Add error checking.

  owner = unit.owner_key.get();
  if target_tile.is_home_tile and owner.hometile != target_tile:
    logging.info('The target is a home tile not owned by the player')
    return False;

  # Get the unit position
  unit_tile = unit.location_tile.get()
  unit_x, unit_y = unit_tile.coordinate_x, unit_tile.coordinate_y
  # Get target position
  target_x, target_y = target_tile.coordinate_x, target_tile.coordinate_y

  # Make sure the target is no more than 1 tile away (diagonal counts as 1).
  if abs(target_x - unit_x) <= 1 and abs(target_y - unit_y) <= 1:
    return True
  else:
    logging.info('the target is too far')
    return False


def handleUnitMoveRequest(unit_id, target_tile_id):
  # TODO: Handle invalid keys.
  unit_key = ndb.Key(urlsafe=unit_id)
  unit = unit_key.get()
  if unit.has_order:
    logging.error('The unit already has an order')
    return
  tile_key = ndb.Key(urlsafe=target_tile_id)
  # TODO: Handle checking that the unit doesn't already have an order.
  # Check if the movement is valid
  if isMoveValid(unit_key.get(), tile_key.get()):
    Order(
      order_type = ORDER_TYPE_INT_MAPPING[MOVE_KEY],
      unit_key = unit_key,
      move_order = MoveOrder(
        destination_map_tile_key = tile_key
      )).put()
  else:
    logging.error('order not created, because move was not valid')

def isCampBuildValid(unit, tile_resource_key):
  # TODO: Move this to a Util file?
  # Check if the unit is a worker.
  if unit.unit_type != UNIT_TYPE_INT_MAPPING[WORKER_KEY]:
    logging.error('Unit is not a worker.')
    return False

  # Check if the tile is contested.
  tile = unit.location_tile.get()
  if tile.is_contested:
    logging.error('Unit is on a contested tile.')
    return False

  # Check if there is already a structure on the tile.
  if tile.has_structure:
    logging.error('Tile already has a structure.')
    return False

  # Check if the selected resource is valid.
  if tile_resource_key not in tile.resources:
    logging.error('Selected resource not available.')
    return False

  return True

def handleBuildCampOrderRequest(unit_id, tile_resource_id):
  # TODO: Handle invalid keys.
  unit_key = ndb.Key(urlsafe=unit_id)
  unit = unit_key.get()
  if unit.has_order:
    logging.error('The unit already has an order')
    return
  tile_resource_key = ndb.Key(urlsafe=tile_resource_id)

  if isCampBuildValid(unit_key.get(), tile_resource_key):
    Order(
      order_type = ORDER_TYPE_INT_MAPPING[BUILD_CAMP_KEY],
      unit_key = unit_key,
      build_camp_order = BuildCampOrder(
        tile_resource_key = tile_resource_key
      )
    ).put()
  else:
    logging.error('The camp build was invalid, order not created.')
  # TODO: return something useful.
