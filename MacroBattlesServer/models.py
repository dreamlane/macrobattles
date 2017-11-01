## models.py Holds all model information.

from google.appengine.ext import ndb

class MetalProperties(ndb.Model):
  """Models the properties that a metal resource has."""
  hardness = ndb.IntegerProperty()
  lustre = ndb.IntegerProperty()
  density = ndb.IntegerProperty()

class WoodProperties(ndb.Model):
  """Models the properties that a wood resource has."""
  hardness = ndb.IntegerProperty()
  workability = ndb.IntegerProperty()
  figure = ndb.IntegerProperty()

class LeatherProperties(ndb.Model):
  """Models the properties that a leather resource has."""
  durability = ndb.IntegerProperty()
  flexibility = ndb.IntegerProperty()
  smoothness = ndb.IntegerProperty()

class ResourceTemplate(ndb.Model):
  # An integer representing the type of this resource.
  # 0 = Metal
  # 1 = Wood
  # 2 = Leather
  resource_type = ndb.IntegerProperty()

  # Metal properties
  metal_properties = ndb.StructuredProperty(MetalProperties)

  # Wood properties
  wood_properties = ndb.StructuredProperty(WoodProperties)

  # Leather properties
  leather_properties = ndb.StructuredProperty(LeatherProperties)

  name = ndb.StringProperty()


class TileResource(ndb.Model):
  """Models a resource on the game map tiles."""
  # Which resource it is.
  resource_template = ndb.StructuredProperty(ResourceTemplate)

  # How much of the resource there is.
  saturation = ndb.IntegerProperty()

class Resource(ndb.Model):
  """Models a stack of resources in the game"""
  # The template describing the resource.
  resource_template = ndb.StructuredProperty(ResourceTemplate)

  # The amount of the resource held by the player.
  quantity = ndb.IntegerProperty()

class Player(ndb.Model):
  """Models an individual player of the game"""
  # The player's chosen name or gamertag.
  username = ndb.StringProperty()
  password = ndb.StringProperty(indexed=False)

  # The resources the player owns.
  resources = ndb.KeyProperty(kind='Resource', repeated=True)

  # The home tile for this player
  home_tile = ndb.KeyProperty(kind='MapTile')

  # How much money the player has
  money = ndb.IntegerProperty()

class MapTile(ndb.Model):
  """Models a map tile in the game"""
  # The X and Y coordinates of the tile in the game map.
  coordinate_x = ndb.IntegerProperty()
  coordinate_y = ndb.IntegerProperty()

  # The Resources available to gather from the tile.
  resources = ndb.StructuredProperty(TileResource, repeated=True)

  # Whether or not this tile is a home tile for a player.
  is_home_tile = ndb.BooleanProperty()

  # Armies that are currently present on this tile.
  units_on_tile = ndb.KeyProperty(kind='Unit', repeated=True)

class Unit(ndb.Model):
  """Models a player-owned unit in the game."""
  # What type of unit it is.
  # 0 = Unknown
  # 1 = Worker
  # 2 = Soldier
  unit_type = ndb.IntegerProperty()

  # Who owns this unit.
  unit_owner = ndb.KeyProperty(kind=Player)

  # How much health this unit has.
  health = ndb.IntegerProperty()

  # What equipment this unit is carrying
  equipment = ndb.KeyProperty(kind='Equipment', repeated=True)

class Equipment(ndb.Model):
  """The top level class for all equipment models in game."""
  # Which player owns the equipment.
  player = ndb.KeyProperty(kind=Player)

class Sword(Equipment):
  """Models a sword in the game."""
  # How much damage the sword does.
  power = ndb.IntegerProperty()

  # How likely the sword is to break after each attack.
  # This should be a number in range [0, 1].
  reliability = ndb.FloatProperty()

class Armor(Equipment):
  """Models an armor in the game."""
  # How much damage it absorbs for the user, as a percentage.
  # This should be a numebr in range [0, 1]. TODO: Make custom property.
  damage_reduction = ndb.FloatProperty()

  # How much more damage the armor can take before breaking.
  # Note: This is not max durability, it is current.
  durability = ndb.IntegerProperty()
