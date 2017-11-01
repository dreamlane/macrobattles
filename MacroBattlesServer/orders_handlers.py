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

from orders_constants import MOVE_KEY
from orders_constants import BUILD_CAMP_KEY
from orders_constants import ORDER_TYPE_INT_MAPPING
from unit_constants import WORKER_KEY
from unit_constants import UNIT_TYPES_INT_MAPPING

def isMoveValid(unit, target_tile):
  # Get the unit position
  # TODO: Add error checking.
  # TODO: Add home tile check, so players home tile will be safe.
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
  tile_key = ndb.Key(urlsafe=target_tile_id)
  # TODO: Handle checking that the unit doesn't already have an order.
  # Check if the movement is valid
  if isMoveValid(unit_key.get(), tile_key.get()):
    Order(
      order_type = ORDER_TYPE_INT_MAPPING[MOVE_KEY],
      move_order = MoveOrder(
        unit_key = unit_key,
        destination_map_tile_key = tile_key
      )).put()
  else:
    logging.error('order not created, because move was not valid')

def isCampBuildValid(unit, tile_resource_key):
  # TODO: Move this to a Util file?
  # Check if the unit is a worker.
  if unit.unit_type != UNIT_TYPES_INT_MAPPING[WORKER_KEY]:
    logging.error('Unit is not a worker.')
    return False

  # Check if the tile is contested.
  tile = unit.location_tile.get()
  if tile.is_contested:
    logging.error('Unit is on a contested tile.')
    return False

  # Check if there is already a structure on the tile.
  if tile.structure:
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
  tile_resource_key = ndb.Key(urlsafe=tile_resource_id)

  if isCampBuildValid(unit_key.get(), tile_resource_key):
    Order(
      order_type = ORDER_TYPE_INT_MAPPING[BUILD_CAMP_KEY],
      build_camp_order = BuildCampOrder(
        unit_key = unit_key,
        tile_resource_key = tile_resource_key
      )
    ).put()
  # TODO: return something useful.
