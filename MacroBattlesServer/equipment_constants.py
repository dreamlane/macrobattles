## equipment_constants.py
""" This file defines all of the constant values for equipment. """

""" The keys for the types of equipment. """
WEAPON_KEY = 'WEAPON'
ARMOR_KEY = 'ARMOR'

""" The key to integer mapping for the Equipment type in ndb Model. """
EQUIPMENT_TYPE_INT_MAPPING = {
  WEAPON_KEY: 0,
  ARMOR_KEY: 1
}
