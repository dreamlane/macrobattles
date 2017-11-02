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

""" The keys for the equipment templates. """
SWORD_TEMPLATE_KEY = 'SWORD_TEMPLATE'
PLATE_ARMOR_TEMPLATE_KEY = 'PLATE_ARMOR_TEMPLATE'

""" The key to integer mapping for the templates for equipment."""
EQUIPMENT_TEMPLATE_IDS = {
  SWORD_TEMPLATE_KEY: 0,
  PLATE_ARMOR_TEMPLATE_KEY: 1
}

class CraftCost():
  """ A simple class to represent the cost of crating an equipment."""

  def __init__(self, metal=0, leather=0, wood=0):
    self.metal = metal
    self.leather = leather
    self.wood = wood

""" The mapping of crafting costs to the equipment templates."""
EQUIPMENT_TEMPLATE_CRAFT_COSTS = {
  SWORD_TEMPLATE_KEY: CraftCost(metal=4, wood=1, leather=1),
  PLATE_ARMOR_TEMPLATE_KEY: CraftCost(metal=12, leather=4)
}

""" The mapping of the equipment template key to the Equipment type int."""
EQUIPMENT_TEMPLATE_TO_TYPE_MAPPING = {
  SWORD_TEMPLATE_KEY: EQUIPMENT_TYPE_INT_MAPPING[WEAPON_KEY],
  PLATE_ARMOR_TEMPLATE_KEY: EQUIPMENT_TYPE_INT_MAPPING[ARMOR_KEY]
}
