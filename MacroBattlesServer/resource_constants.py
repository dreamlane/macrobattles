## resource_constants.py
""" This file defines all of the constant values for resources."""

""" The keys for the types of resources. """
METAL_KEY = "METAL"
WOOD_KEY = "WOOD"
LEATHER_KEY = "LEATHER"

""" The key-value pairs for types of resources."""
RESOURCE_TYPES_INT_MAPPING = {
  METAL_KEY: 0,
  WOOD_KEY: 1,
  LEATHER_KEY: 2,
}

""" The list of resource properties for each type of resource."""
## TODO: make this less string typed, and more in line with the ndb model.
RESOURCE_PROPERTY_TYPES = {
  METAL_KEY: ['hardness', 'lustre', 'density'],
  WOOD_KEY: ['hardness', 'workability', 'figure'],
  LEATHER_KEY: ['durability', 'flexibility', 'smoothness']
}
