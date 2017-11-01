## orders_constants.py
""" This file defines all of the constant values for orders. """

""" The keys for the types of orders. """
MOVE_KEY = 'MOVE'
BUILD_CAMP_KEY = 'BUILD_CAMP'

""" The key to integer mapping for the Order type in ndb Model. """
ORDER_TYPE_INT_MAPPING = {
  MOVE_KEY: 0,
  BUILD_CAMP_KEY: 1
}
