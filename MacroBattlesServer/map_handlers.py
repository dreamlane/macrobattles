## map_handlers.py Handles API calls involving the map.

import logging
import json

from models import MapTile
from requestutils import ResponseBuilder

def handleGetMapRequest():
  """
    Grabs all of the map tiles and returns an ordered 2d list.
    @returns A built Response with the dictionary of MapTile models.
  """
  map_query = MapTile.query()
  if map_query.count() > 0:
    map_tiles = map_query.fetch()
    ## The map_object will be built up and built into the response.
    ## Its keys will be a the urlsafe key of the serialized maptile value.
    map_object = {'mapTiles': []}
    for tile in map_tiles:
      # Serialized the map tile into what the client needs.
      serialized_tile = {}
      serialized_tile['coordinate_x'] = tile.coordinate_x
      serialized_tile['coordinate_y'] = tile.coordinate_y
      serialized_tile['resource_keys'] = []
      for resource_key in tile.resources:
        serialized_tile['resource_keys'].append(resource_key.urlsafe())
      serialized_tile['key'] = tile.key.urlsafe()
      map_object['mapTiles'].append(serialized_tile)
    # The map_object is built, set it on the response data as a json string.
    return ResponseBuilder().setData(json.dumps(map_object)).build()
  # No tiles exist, the game has not started.
  else:
    return ResponseBuilder().setErrorMessage("No game has started.")
