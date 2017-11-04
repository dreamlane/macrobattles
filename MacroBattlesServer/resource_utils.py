## resource_utils.py

def determineHarvestRate(tile_resource):
  """@param tile_resource a TileResource Model. """
  # In python, when a float is cast into an int, the floor is taken.
  # 3.99999 will cast to 3. Truncation.
  return int(tile_resource.saturation * 0.33)
