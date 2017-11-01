## gamelogic.py

from random import *
import logging

from google.appengine.ext import ndb

from names import males
from resource_constants import RESOURCE_TYPES_INT_MAPPING
from resource_constants import RESOURCE_PROPERTY_TYPES
from resource_constants import METAL_KEY
from resource_constants import WOOD_KEY
from resource_constants import LEATHER_KEY

from models import ResourceTemplate
from models import TileResource
from models import MetalProperties
from models import WoodProperties
from models import LeatherProperties
from models import MapTile
from models import Player
from models import Resource

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
    resource_template = resource_template,
    saturation = randint(1,99))

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

def addPlayerToWorld(player_id):
  map_query = MapTile.query()
  map_tiles = map_query.fetch(map_query.count())
  home_tile = choice(map_tiles)
  while not validateHomeTileSelection(home_tile):
    # TODO: guard against infinite loop
    home_tile = choice(map_tiles)
    logging.info('trying again')
  # Get player
  player_query = Player.query(Player.username == player_id)
  if player_query.count() > 0:
    player = player_query.get()
    # TODO: figure out if this is safe, due to 1 failing, and other succeeding.
    home_tile.is_home_tile = True
    player.home_tile = home_tile.put()
    player.put()
  else:
    logging.error('no playoooooor')

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

def testGivePlayerResource(player_key_string):
  player = ndb.Key(urlsafe=player_key_string).get()
  player.resources.append(Resource(
        resource_template = ResourceTemplate(
            resource_type = 0,
            metal_properties = MetalProperties(
                hardness = 200,
                lustre = 400,
                density = 600,
            ),
            name = 'testMetal'
        ),
        quantity = 150
    ).put())
  player.put()
