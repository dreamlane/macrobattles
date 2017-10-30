## gamelogic.py

from random import *
import logging

from google.appengine.ext import ndb

from names import males
from resource_constants import RESOURCE_TYPES, RESOURCE_PROPERTY_TYPES

from models import ResourceTemplate
from models import TileResource
from models import MetalProperties
from models import WoodProperties
from models import LeatherProperties
from models import MapTile

def generateTileResource():
  ## Randomly choose a resource type key.
  resource_type = choice(RESOURCE_TYPES.keys())
  ## Randomly choose a value for each of the resource type's properties.
  properties = {}
  for resource_property in RESOURCE_PROPERTY_TYPES[resource_type]:
    properties[resource_property] = randint(1,999)
  resource_template = ResourceTemplate(resource_type = resource_type)

  # Determine which properties to fill on the resource_template:
  # TODO: Make this less ugly for the type checking.
  if resource_type == 0:
    resource_template.metal_properties = properties
  elif resource_type == 1:
    resource_template.wood_properties = properties
  elif resource_type == 2:
    resource_template.leather_properties = properties
  else:
    logging.error('Error in the genresourceTemplate')

  resource_template.name = choice(males)

  return TileResource(
    resource_template = resource_template,
    saturation = randint(1,99))



def generateMapTiles():
  map_tile_models = []
  for x in range(0,3):
    for y in range(0,3):
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
