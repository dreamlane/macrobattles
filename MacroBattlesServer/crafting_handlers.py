## crafting_handlers.py

from random import *
import logging

from google.appengine.ext import ndb

from constants_equipment import ARMOR_KEY
from constants_equipment import EQUIPMENT_TEMPLATE_CRAFT_COSTS
from constants_equipment import EQUIPMENT_TEMPLATE_TO_TYPE_MAPPING
from constants_equipment import EQUIPMENT_TYPE_INT_MAPPING
from constants_equipment import WEAPON_KEY
from constants_resources import LEATHER_KEY
from constants_resources import METAL_KEY
from constants_resources import RESOURCE_TYPES_INT_MAPPING
from constants_resources import WOOD_KEY
from constants_weapons import WEAPON_POWER_FORMULA
from constants_weapons import WEAPON_RELIABILITY_FORMULA
from constants_weapons import WEAPON_TYPE_INT_MAPPING

from models import Armor
from models import Equipment
from models import Weapon

from craft_utils import getAttributeValue

def craftEquipment(inputs):
  """ @param inputs a json object with inputs."""
  # TODO: Break up this code into functional pieces.
  # TODO: Validate inputs.
  # TODO: Think hard about redesigning the crafting logic.
  equipment_template_key = inputs['equipment_template_key']
  # Make sure the player has all of the necessary resources.
  cost_to_craft = EQUIPMENT_TEMPLATE_CRAFT_COSTS[equipment_template_key]
  player_key = ndb.Key(urlsafe=inputs['player_id']) # TODO: error handle.
  player = player_key.get()
  resources_to_put = []
  formula_input = {}
  # TODO: Make this more generic, instead of checking each. DRY this up.
  if cost_to_craft.metal > 0:
    # Check for adequate metal resources.
    if 'metal_resource_key' not in inputs:
      logging.error('metal_resource_key missing from input!')
      # TODO: handle failure better than returning none.
      return None
    resource_key = ndb.Key(urlsafe=inputs['metal_resource_key'])
    if resource_key in player.resources:
      resource = resource_key.get()
      template = resource.resource_template.get()
      if (resource.quantity >= cost_to_craft.metal and
          template.resource_type == RESOURCE_TYPES_INT_MAPPING[METAL_KEY]):
        resource.quantity -= cost_to_craft.metal
        resources_to_put.append(resource)
        formula_input[METAL_KEY] = template
        # TODO: Add crafting power formulas logic here!
      else:
        logging.error('Metal Quantity too low, or resource is not metal!')
        # TODO: handle failure better than returning none.
        return None
    else:
      logging.error('Player does not own metal resource!')
      # TODO: handle failure better than returning none.
      return None
  if cost_to_craft.wood > 0:
    # Check for adequate wood resources.
    if 'wood_resource_key' not in inputs:
      logging.error('wood_resource_key missing from input!')
      # TODO: handle failure better than returning none.
      return None
    resource_key = ndb.Key(urlsafe=inputs['wood_resource_key'])
    if resource_key in player.resources:
      resource = resource_key.get()
      template = resource.resource_template.get()
      if (resource.quantity >= cost_to_craft.wood and
          template.resource_type == RESOURCE_TYPES_INT_MAPPING[WOOD_KEY]):
        resource.quantity -= cost_to_craft.wood
        resources_to_put.append(resource)
        formula_input[WOOD_KEY] = template
        # TODO: Add crafting power formulas logic here!
      else:
        logging.error('Wood Quantity too low, or resource is not wood!')
        # TODO: handle failure better than returning none.
        return None
    else:
      logging.error('Player does not own wood resource!')
      # TODO: handle failure better than returning none.
      return None
  if cost_to_craft.leather > 0:
    # Check for adequate leather resources.
    if 'leather_resource_key' not in inputs:
      logging.error('leather_resource_key missing from input!')
      # TODO: handle failure better than returning none.
      return None
    resource_key = ndb.Key(urlsafe=inputs['leather_resource_key'])
    if resource_key in player.resources:
      resource = resource_key.get()
      template = resource.resource_template.get()
      if (resource.quantity >= cost_to_craft.leather and
          template.resource_type == RESOURCE_TYPES_INT_MAPPING[LEATHER_KEY]):
        resource.quantity -= cost_to_craft.leather
        resources_to_put.append(resource)
        formula_input[LEATHER_KEY] = template
        # TODO: Add crafting power formulas logic here!
      else:
        logging.error('Leather Quantity too low, or resource is not leather!')
        # TODO: handle failure better than returning none.
        return None
    else:
      logging.error('Player does not own leather resource!')
      # TODO: handle failure better than returning none.
      return None

  # Validation has passed. Create the equipment.
  equipment_type = EQUIPMENT_TEMPLATE_TO_TYPE_MAPPING[equipment_template_key]
  crafted_equipment = Equipment(
    equipment_type = equipment_type,
    player = player_key)

  if equipment_type == EQUIPMENT_TYPE_INT_MAPPING[WEAPON_KEY]:
    crafted_equipment.weapon_data = Weapon(
      weapon_type = WEAPON_TYPE_INT_MAPPING[equipment_template_key],
      power = int(getAttributeValue(formula_input,
                  WEAPON_POWER_FORMULA[equipment_template_key])),
      reliability = getAttributeValue(formula_input,
                    WEAPON_RELIABILITY_FORMULA[equipment_template_key])
    )
    player.equipment.append(crafted_equipment.put())
    player.put()

  # TODO: Handle armor crafting.

  # Crafting complete. Now update the resources.
  ndb.put_multi(resources_to_put)
