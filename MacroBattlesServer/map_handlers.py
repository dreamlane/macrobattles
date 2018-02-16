## map_handlers.py Handles API calls involving the map.

import json
import logging

from google.appengine.ext import ndb

from constants_equipment import ARMOR_KEY
from constants_equipment import EQUIPMENT_TYPE_INT_MAPPING
from constants_equipment import WEAPON_KEY
from constants_resources import LEATHER_KEY
from constants_resources import METAL_KEY
from constants_resources import WOOD_KEY
from constants_resources import RESOURCE_TYPES_INT_MAPPING
from constants_structures import HARVESTING_CAMP_KEY
from constants_structures import STRUCTURE_TYPE_INT_MAPPING
from models import Equipment
from models import MapTile
from models import PlayerStructure
from models import ResourceTemplate
from models import Unit
from requestutils import ResponseBuilder

def handleGetMapRequest(inputs):
  """
    Gets the map state of the game from the given player's interest model.
    @returns A built Response with the following sets of data:
             map_tiles: a list of serialized MapTiles.
             units: a list of serialized Units.
             resource_templates: a list of ResourceTemplates.
             equipment: a list of Equipment, only including equiped items.
    NOTE: Eventually this will include a more detailed interest model, to allow
    for fog of war, but for now we return the entire world, and only use the
    interest model (player_id) to determine if a tile is a player home or enemy
    home.
  """

  # Make sure the player is already in the game.
  player_key = ndb.Key(urlsafe=inputs['player_id'])
  player = player_key.get()
  if not player.home_tile:
    # If the player does not have a home tile, then they aren't in the game, and
    # they need to join the game.
    logging.error('Player: ' + player_key.urlsafe() + " is not in the game!")
    error_message = 'Player is not in the game.'
    return ResponseBuilder().setErrorMessage(error_message).build()

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
      serialized_tile['structure_keys'] = []
      structure_keys = tile.structures.fetch(keys_only=True)
      for structure_key in structure_keys:
        serialized_tile['structure_keys'].append(structure_key.urlsafe())
      # Tell the client if this map tile is a home tile.
      serialized_tile['is_player_home'] = False
      serialized_tile['is_enemy_home'] = False
      if tile.is_home_tile:
        if tile.key == player.home_tile:
          serialized_tile['is_player_home'] = True
        else:
          # For now, anyone that isn't the player is an enemy.
          serialized_tile['is_enemy_home'] = True
      map_object['mapTiles'].append(serialized_tile)

  # TODO: There is a lot of repetition here, find a way to DRY this up.
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
    map_object['resource_templates'] = []
    resource_templates = rt_query.fetch()
    for template in resource_templates:
      # Serialize the resource_template into what the client needs.
      serialized_rt = {}
      serialized_rt['key'] = template.key.urlsafe()
      serialized_rt['name'] = template.name
      serialized_rt['type'] = template.resource_type
      if template.resource_type == RESOURCE_TYPES_INT_MAPPING[METAL_KEY]:
        serialized_rt['metal_properties'] = template.metal_properties.to_dict()
      if template.resource_type == RESOURCE_TYPES_INT_MAPPING[WOOD_KEY]:
        serialized_rt['wood_properties'] = template.wood_properties.to_dict()
      if template.resource_type == RESOURCE_TYPES_INT_MAPPING[LEATHER_KEY]:
        serialized_rt['leather_properties'] = template.leather_properties.to_dict()
      map_object['resource_templates'].append(serialized_rt)

  # Get the equipment.
  eq_query = Equipment.query()
  if eq_query.count() > 0:
    map_object['equipment'] = []
    equipment_list = eq_query.fetch()
    for equipment in equipment_list:
      # Serialize the equipment into what the client needs.
      serialized_eq = {}
      serialized_eq['key'] = equipment.key.urlsafe()
      serialized_eq['owner_key'] = equipment.player.urlsafe()
      serialized_eq['type'] = equipment.type
      if equipment.type == EQUIPMENT_TYPE_INT_MAPPING[ARMOR_KEY]:
        serialized_eq['armor_data'] = equipment.armor_data.to_dict()
      if equipment.type == EQUIPMENT_TYPE_INT_MAPPING[WEAPON_KEY]:
        serialized_eq['weapon_data'] = equipment.weapon_data.to_dict()
      map_object['equipment'].append()

  # Get the structures
  struct_query = PlayerStructure.query()
  if struct_query.count() > 0:
    map_object['structures'] = []
    structures = struct_query.fetch()
    for structure in structures:
      # Serialize the structure into what the client needs.
      serialized_struct = {}
      serialized_struct['key'] = structure.key.urlsafe()
      serialized_struct['owner_key'] = structure.owner_key.urlsafe()
      serialized_struct['type'] = structure.structure_type
      serialized_struct['health'] = structure.health
      location_tile = structure.location.get()
      serialized_struct['coordinate_x'] = location_tile.coordinate_x
      serialized_struct['coordinate_y'] = location_tile.coordinate_y
      if (structure.structure_type ==
          STRUCTURE_TYPE_INT_MAPPING[HARVESTING_CAMP_KEY]):
        # We need to further serialize the camp data.
        camp_data = {'tile_resource_key':
                     structure.harvesting_camp_data.tile_resource_key}
      map_object['structures'].append(serialized_struct)

  # The map_object is built, set it on the response data as a json string.
  if len(map_object['mapTiles']) > 0:
    return ResponseBuilder().setData(json.dumps(map_object)).build()
  # No tiles exist, the game has not started.
  else:
    return ResponseBuilder().setErrorMessage("No game has started.")
