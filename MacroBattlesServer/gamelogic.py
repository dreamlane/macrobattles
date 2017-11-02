## gamelogic.py

from random import *
import logging

from google.appengine.ext import ndb

from names import males
from equipment_constants import ARMOR_KEY
from equipment_constants import EQUIPMENT_TEMPLATE_CRAFT_COSTS
from equipment_constants import EQUIPMENT_TEMPLATE_TO_TYPE_MAPPING
from equipment_constants import EQUIPMENT_TYPE_INT_MAPPING
from equipment_constants import WEAPON_KEY
from resource_constants import RESOURCE_TYPES_INT_MAPPING
from resource_constants import RESOURCE_PROPERTY_TYPES
from resource_constants import METAL_KEY
from resource_constants import WOOD_KEY
from resource_constants import LEATHER_KEY
from unit_constants import UNIT_TYPES_INT_MAPPING
from unit_constants import UNIT_COSTS
from unit_constants import UNIT_BASE_HEALTH

from models import Equipment
from models import MapTile
from models import Player
from models import ResourceTemplate
from models import TileResource
from models import Unit

def generateTileResource():
  ## Randomly choose a resource type key.
  resource_type = choice(RESOURCE_TYPES_INT_MAPPING.keys())
  ## Randomly choose a value for each of the resource type's properties.
  properties = {}
  for resource_property in RESOURCE_PROPERTY_TYPES[resource_type]:
    properties[resource_property] = randint(1,999)
  resource_template = ResourceTemplate(
      resource_type = RESOURCE_TYPES_INT_MAPPING[resource_type])

  # Determine which properties to fill on the resource_template:
  if resource_type == METAL_KEY:
    # TODO: Use string properties to remove the if/elif altogether.
    resource_template.metal_properties = properties
  elif resource_type == WOOD_KEY:
    resource_template.wood_properties = properties
  elif resource_type == LEATHER_KEY:
    resource_template.leather_properties = properties
  else:
    logging.error('Error in the genresourceTemplate')

  resource_template.name = choice(males)

  return TileResource(
    resource_template = resource_template.put(),
    saturation = randint(1,99)).put()

def generateMapTiles():
  map_tile_models = []
  for x in range(0,4):
    for y in range(0,4):
      tile_resources = []
      for i in range(0,3):
        tile_resources.append(generateTileResource())
      map_tile_models.append(MapTile(
        coordinate_x = x,
        coordinate_y = y,
        resources = tile_resources,
        is_home_tile = False
      ))
  ndb.put_multi(map_tile_models)

def addPlayerToWorld(player_key_string):
  map_query = MapTile.query()
  map_tiles = map_query.fetch(map_query.count())
  home_tile = choice(map_tiles)
  while not validateHomeTileSelection(home_tile):
    # TODO: guard against infinite loop
    home_tile = choice(map_tiles)
    logging.info('trying again')

  player = ndb.Key(urlsafe=player_key_string).get()
  # TODO: figure out if this is safe, due to 1 failing, and other succeeding.
  home_tile.is_home_tile = True
  player.home_tile = home_tile.put()
  player.money = 100
  player.put()

def validateHomeTileSelection(tile):
  return not tile.is_home_tile

def resolveTurn():
  # TODO make
  pass

def getValuePerUnit(resource):
  """
      @param resource models.Resource.
      @returns the amount of money each unit of resource is worth.
  """
  template = resource.resource_template
  value = 0
  if template.resource_type == METAL_KEY:
    #TODO: Figure out how to make this more generic.
    value += template.metal_properties.hardness
    value += template.metal_properties.lustre
    value += template.metal_properties.density
  elif template.resource_type == WOOD_KEY:
    value += template.wood_properties.hardness
    value += template.wood_properties.workability
    value += template.wood_properties.figure
  elif template.resource_type == LEATHER_KEY:
    value += template.leather_properties.durability
    value += template.leather_properties.flexibilty
    value += template.leather_properties.smoothness
  else:
    logging.error('cannot get value of unknown type: ' +
                   str(template.resource_type))
  return value / 300

def sellResource(player_key_string, resource_key_string, quantity_string):
  # TODO: make sure the requestor is authorized to make the sale.
  player_key = ndb.Key(urlsafe=player_key_string)
  resource_key = ndb.Key(urlsafe=resource_key_string)
  player = player_key.get()
  resource = resource_key.get()
  quantity = 0
  try:
    quantity = int(quantity_string)
  except ValueError:
    logging.error('Input quantity was not an int')
    return None # TODO: return an error response

  if quantity > 0 and quantity <= resource.quantity:
    # TODO: move this function to a resource utils file
    payout = quantity * getValuePerUnit(resource)
    resource.quantity -= quantity
    # This if shouldn't exist if they player object is created correctly.
    if player.money:
      player.money += payout
    else:
      player.money = payout

    #TODO: remove the resource key from the player if quantity == 0.

    #TODO: single transaction
    player.put()
    resource.put()

    logging.info("successful sale")
  else:
    logging.info('quantity wrong or resource quantity too low' + str(quantity) + str(resource.quantity))

def hireUnit(player_key_string, unit_type_string):
  """
     @param player_key_string urlsafe key string for models.Player ndb model.
     @param unit_type_string which unit type to hire.
  """
  # TODO: replace this with a function that does this common thing.
  player = ndb.Key(urlsafe=player_key_string).get()
  unit_cost = UNIT_COSTS[unit_type_string]
  if player.money >= unit_cost:
    player.money -= unit_cost
    player.units.append(Unit(
      unit_type = UNIT_TYPES_INT_MAPPING[unit_type_string],
      unit_owner = ndb.Key(urlsafe=player_key_string),
      health = UNIT_BASE_HEALTH[unit_type_string],
      location_tile = player.home_tile
    ).put())
    player.put()
    logging.info('unit added')
  else:
    logging.error('unit too expensive')

def isUnitOnHomeTile(unit):
  # TODO: Move this to a util file?
  player = unit.unit_owner.get()
  return player.home_tile == unit.location_tile

def playerHasEquipment(player, equipment_key):
  # TODO: move this to a util file?
  return equipment_key in player.equipment

def equipUnit(unit_id, equipment_id):
  # TODO: Handle invalid keys.
  unit_key = ndb.Key(urlsafe=unit_id)
  equipment_key = ndb.Key(urlsafe=equipment_id)
  unit = unit_key.get()
  # Make sure the unit is standing at home, otherwise it cannot be equiped.
  if not isUnitOnHomeTile(unit):
    # TODO: write an error response.
    logging.error('cannot equip unit, not on home tile')
    return None

  # Make sure the player has the equipment.
  player = unit.unit_owner.get()
  if not playerHasEquipment(player, equipment_key):
    # TODO: write an error response
    logging.error('cannot equip unit, player does not have equipment')
    return None

  # Handle case where Unit already has equipment equiped.
  current_equipment_key = None
  # TODO: Error handle this, to make sure it is equipment, and not a subclass.
  equipment = equipment_key.get()
  if equipment.equipment_type == EQUIPMENT_TYPE_INT_MAPPING[ARMOR_KEY]:
    current_equipment_key = unit.armor
    logging.info('unit armor key: ' + str(unit.armor))
    unit.armor = equipment_key
    logging.info('unit armor key after: ' + str(unit.armor))
    # Remove the equipment from the list.
    player.equipment.remove(equipment_key)
  elif equipment.equipment_type == EQUIPMENT_TYPE_INT_MAPPING[WEAPON_KEY]:
    current_equipment_key = unit.weapon
    logging.info('unit weapon key: ' + str(unit.weapon))
    unit.weapon = equipment_key
    logging.info('unit weapon key after: ' + str(unit.weapon))
    player.equipment.remove(equipment_key)
  else:
    logging.error('equipment kind matching failed')
    return None
  # If the unit already has something equiped, put that equipment back on the
  # player's equipment list.
  if current_equipment_key != None:
    player.equipment.append(current_equipment_key)

  # TODO: make sure this is transactional with the player put.
  unit.put()
  player.put()

def craftItem(inputs):
  """ @param inputs a json object with inputs."""
  # TODO: Break up this code into functional pieces, and move into craftinglogic.py
  # TODO: Validate inputs.
  equipment_template_key = inputs['equipment_template_key']
  # Make sure the player has all of the necessary resources.
  cost_to_craft = EQUIPMENT_TEMPLATE_CRAFT_COSTS[equipment_template_key]
  player_key = ndb.Key(urlsafe=inputs['player_id']) # TODO: error handle.
  player = player_key.get()
  resources_to_put = []
  # TODO: Make this more generic, instead of checking each. DRY this up.
  if cost_to_craft.metal > 0:
    # Check for adequate metal resources.
    # TODO: validate the input!
    resource_key = ndb.Key(urlsafe=inputs['metal_resource_key'])
    if resource_key in player.resources:
      resource = resource_key.get()
      template = resource.resource_template.get()
      if (resource.quantity >= cost_to_craft.metal and
          template.resource_type == RESOURCE_TYPES_INT_MAPPING[METAL_KEY]):
        resource.quantity -= cost_to_craft.metal
        resources_to_put.append(resource)
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
    # TODO: validate the input!
    resource_key = ndb.Key(urlsafe=inputs['wood_resource_key'])
    if resource_key in player.resources:
      resource = resource_key.get()
      template = resource.resource_template.get()
      if (resource.quantity >= cost_to_craft.wood and
          template.resource_type == RESOURCE_TYPES_INT_MAPPING[WOOD_KEY]):
        resource.quantity -= cost_to_craft.wood
        resources_to_put.append(resource)
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
    # TODO: validate the input!
    resource_key = ndb.Key(urlsafe=inputs['leather_resource_key'])
    if resource_key in player.resources:
      resource = resource_key.get()
      template = resource.resource_template.get()
      if (resource.quantity >= cost_to_craft.leather and
          template.resource_type == RESOURCE_TYPES_INT_MAPPING[LEATHER_KEY]):
        resource.quantity -= cost_to_craft.leather
        resources_to_put.append(resource)
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

  # TODO: Do type specific stuff here. and then put() the equipment
