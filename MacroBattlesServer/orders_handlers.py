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
"""
import logging

from google.appengine.ext import ndb

from models import MoveOrder
from models import Order

from orders_constants import MOVE_KEY
from orders_constants import ORDER_TYPE_INT_MAPPING

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
