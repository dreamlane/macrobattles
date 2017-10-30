## resource_constants.py
""" This file defines all of the constant values for resources."""


""" The key-value pairs for types of resources."""
RESOURCE_TYPES = {
  0: "Metal",
  1: "Wood",
  2: "Leather"
}

""" The list of resource properties for each type of resource, where the key
    is the same as the key to the RESOURCE_TYPES dict.
    TODO: make this less string typed, and more in line with the ndb model """
RESOURCE_PROPERTY_TYPES = {
  0: ['hardness', 'lustre', 'density'],
  1: ['hardness', 'workability', 'figure'],
  2: ['durability', 'flexibility', 'smoothness']
}
