## gamelogic.py

from random import *
import logging

from google.appengine.ext import ndb

from names import males
from constants_equipment import ARMOR_KEY
from constants_equipment import EQUIPMENT_TYPE_INT_MAPPING
from constants_equipment import WEAPON_KEY
from constants_resources import RESOURCE_TYPES_INT_MAPPING
from constants_resources import RESOURCE_PROPERTY_TYPES
from constants_resources import METAL_KEY
from constants_resources import WOOD_KEY
from constants_resources import LEATHER_KEY
from constants_units import UNIT_TYPE_INT_MAPPING
from constants_units import UNIT_COSTS
from constants_units import UNIT_BASE_HEALTH

from models import MapTile
from models import Player
from models import ResourceTemplate
from models import TileResource
from models import Unit
from requestutils import ResponseBuilder

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
    for y in range(0,6):
      tile_resources = []
      for i in range(0,3):
        tile_resources.append(generateTileResource())
      map_tile_models.append(MapTile(
        coordinate_x = x,
        coordinate_y = y,
        resources = tile_resources
      ))
  ndb.put_multi(map_tile_models)

def addPlayerToWorld(inputs):
  map_query = MapTile.query()
  map_tiles = map_query.fetch(map_query.count())
  # TODO: improve the map tile choice logic.
  home_tile = choice(map_tiles)
  while not validateHomeTileSelection(home_tile):
    # TODO: guard against infinite loop, by making the map grow, or blocking the
    # player from joining.
    home_tile = choice(map_tiles)
    logging.info('trying again')

  player = ndb.Key(urlsafe=inputs['player_id']).get()
  player.home_tile = home_tile.key
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

def sellResource(inputs):
  # TODO: make sure the requestor is authorized to make the sale.
  player_key = ndb.Key(urlsafe=inputs['player_id'])
  resource_key = ndb.Key(urlsafe=inputs['resource_id'])
  player = player_key.get()
  resource = resource_key.get()
  quantity = 0
  try:
    quantity = int(inputs['quantity_string'])
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
    logging.info('quantity wrong or resource quantity too low' +
                 str(quantity) + str(resource.quantity))

def hireUnit(inputs):
  """
     @param player_key_string urlsafe key string for models.Player ndb model.
     @param unit_type_string which unit type to hire.
  """
  player_key = ndb.Key(urlsafe=inputs['player_id'])
  player = player_key.get()
  unit_type_string = inputs['unit_type_string']
  unit_cost = UNIT_COSTS[unit_type_string]
  logging.info(player.money)
  if player.money >= unit_cost:
    player.money -= unit_cost
    player.units.append(Unit(
      unit_type = UNIT_TYPE_INT_MAPPING[unit_type_string],
      owner_key = player_key,
      health = UNIT_BASE_HEALTH[unit_type_string],
      location_tile = player.home_tile
    ).put())
    player.put()
    logging.info('unit added')
  else:
    logging.error('unit too expensive')
    return ResponseBuilder().setErrorMessage('unit too expensive').build()

def isUnitOnHomeTile(unit):
  # TODO: Move this to a util file?
  player = unit.owner_key.get()
  return player.home_tile == unit.location_tile

def playerHasEquipment(player, equipment_key):
  # TODO: move this to a util file?
  return equipment_key in player.equipment

def equipUnit(inputs):
  # TODO: Handle invalid keys.
  unit_key = ndb.Key(urlsafe=inputs['unit_id'])
  equipment_key = ndb.Key(urlsafe=inputs['equipment_id'])
  unit = unit_key.get()
  # Make sure the unit is standing at home, otherwise it cannot be equiped.
  if not isUnitOnHomeTile(unit):
    # TODO: write an error response.
    logging.error('cannot equip unit, not on home tile')
    return None

  # Make sure the player has the equipment.
  player = unit.owner_key.get()
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
    unit.armor = equipment_key
    # Remove the equipment from the list.
    player.equipment.remove(equipment_key)
  elif equipment.equipment_type == EQUIPMENT_TYPE_INT_MAPPING[WEAPON_KEY]:
    current_equipment_key = unit.weapon
    unit.weapon = equipment_key
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

