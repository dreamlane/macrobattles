## map_handlers.py Handles API calls involving the map.

import logging
import json

from constants_resources import LEATHER_KEY
from constants_resources import METAL_KEY
from constants_resources import WOOD_KEY
from constants_resources import RESOURCE_TYPES_INT_MAPPING
from models import MapTile
from models import ResourceTemplate
from models import Unit
from requestutils import ResponseBuilder

def handleGetMapRequest():
  """
    Grabs all of the map tiles and returns an ordered 2d list.
    @returns A built Response with the following sets of data:
             map_tiles: a list of serialized MapTiles.
             units: a list of serialized Units.
             resource_templates: a list of ResourceTemplates.
             equipment: a list of Equipment, only including equiped items.
    NOTE: Eventually this will include an interest model, to allow for fog of
    war, but for now we return the entire world.
  """
  # Get the tiles
  map_query = MapTile.query()
  if map_query.count() > 0:
    map_tiles = map_query.fetch()
    ## The map_object will be built up and built into the response.
    ## Its keys will be a the urlsafe key of the serialized maptile value.
    map_object = {'mapTiles': []}
    for tile in map_tiles:
      # Serialize the map tile into what the client needs.
      serialized_tile = {}
      serialized_tile['key'] = tile.key.urlsafe()
      serialized_tile['coordinate_x'] = tile.coordinate_x
      serialized_tile['coordinate_y'] = tile.coordinate_y
      serialized_tile['resources'] = []
      for resource_key in tile.resources:
        tile_resource = resource_key.get()
        resource = {}
        resource['saturation'] = tile_resource.saturation;
        resource['template_key'] = tile_resource.resource_template.urlsafe()
        serialized_tile['resources'].append(resource)
      serialized_tile['unit_keys'] = []
      unit_keys = tile.units.fetch(keys_only=True)
      for unit_key in unit_keys:
        serialized_tile['unit_keys'].append(unit_key.urlsafe())
      map_object['mapTiles'].append(serialized_tile)

  # Get the units.
  unit_query = Unit.query()
  if unit_query.count() > 0:
    map_object['units'] = []
    units = unit_query.fetch()
    for unit in units:
      # Serialize the unit into what the client needs.
      serialized_unit = {}
      serialized_unit['key'] = unit.key.urlsafe()
      serialized_unit['unit_type'] = unit.unit_type
      serialized_unit['owner_key'] = unit.owner_key.urlsafe()
      serialized_unit['health'] = unit.health

      if unit.weapon:
        serialized_unit['weapon_key'] = unit.weapon.urlsafe()
      if unit.armor:
        serialized_unit['armor_key'] = unit.armor.urlsafe()

      location_tile = unit.location_tile.get()
      serialized_unit['coordinate_x'] = location_tile.coordinate_x
      serialized_unit['coordinate_y'] = location_tile.coordinate_y

      serialized_unit['has_order'] = unit.has_order
      if unit.has_order:
        serialized_unit['current_order_key'] = unit.current_order.urlsafe()

      map_object['units'].append(serialized_unit)

  # Get the resource_templates.
  rt_query = ResourceTemplate.query()
  if rt_query.count() > 0:
    map_object['resource_templates'] = [];
    resource_templates = rt_query.fetch()
    for template in resource_templates:
      # Serialize the resource_template into what the client needs.
      serialized_rt = {}
      serialized_rt['key'] = template.key.urlsafe()
      serialized_rt['type'] = template.resource_type
      if template.resource_type == RESOURCE_TYPES_INT_MAPPING[METAL_KEY]:
        serialized_rt['metal_properties'] = template.metal_properties.to_dict()
      if template.resource_type == RESOURCE_TYPES_INT_MAPPING[WOOD_KEY]:
        serialized_rt['wood_properties'] = template.wood_properties.to_dict()
      if template.resource_type == RESOURCE_TYPES_INT_MAPPING[LEATHER_KEY]:
        serialized_rt['leather_properties'] = template.leather_properties.to_dict()
      map_object['resource_templates'].append(serialized_rt)

  # TODO: Add equipment.
  # TODO: Add structures.

  # The map_object is built, set it on the response data as a json string.
  if len(map_object['mapTiles']) > 0:
    return ResponseBuilder().setData(json.dumps(map_object)).build()
  # No tiles exist, the game has not started.
  else:
    return ResponseBuilder().setErrorMessage("No game has started.")
