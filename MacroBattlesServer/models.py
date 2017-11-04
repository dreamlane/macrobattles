## models.py Holds all model information.

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from constants_armor import ARMOR_TYPE_INT_MAPPING
from constants_equipment import EQUIPMENT_TYPE_INT_MAPPING
from constants_orders import ORDER_TYPE_INT_MAPPING
from constants_structures import STRUCTURE_TYPE_INT_MAPPING
from weapon_constants import WEAPON_TYPE_INT_MAPPING

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
  resource_template = ndb.KeyProperty(kind='ResourceTemplate')

  # How much of the resource there is.
  saturation = ndb.IntegerProperty()

class Resource(ndb.Model):
  """Models a stack of resources in the game"""
  # The template describing the resource.
  resource_template = ndb.KeyProperty(kind='ResourceTemplate')

  # The amount of the resource held by the player.
  quantity = ndb.IntegerProperty()

class Player(ndb.Model):
  """Models an individual player of the game"""
  # The player's chosen name or gamertag.
  username = ndb.StringProperty()
  password = ndb.StringProperty(indexed=False)

  # The resources the player owns.
  resources = ndb.KeyProperty(kind='Resource', repeated=True)

  # The home tile for this player.
  home_tile = ndb.KeyProperty(kind='MapTile')

  # How much money the player has.
  money = ndb.IntegerProperty()

  # Units that this player controls.
  units = ndb.KeyProperty(kind='Unit', repeated=True)

  # Equipment that this player owns.
  equipment = ndb.KeyProperty(kind='Equipment', repeated=True)

class MapTile(ndb.Model):
  """Models a map tile in the game"""
  # The X and Y coordinates of the tile in the game map.
  coordinate_x = ndb.IntegerProperty()
  coordinate_y = ndb.IntegerProperty()

  # The Resources available to gather from the tile.
  resources = ndb.KeyProperty(kind='TileResource', repeated=True)

  # Whether or not this tile is a home tile for a player.
  is_home_tile = ndb.BooleanProperty()

  # Armies that are currently present on this tile.
  units_on_tile = ndb.KeyProperty(kind='Unit', repeated=True)

  # Whether or not the tile is contested.
  is_contested = ndb.BooleanProperty()

  # What structure is on the tile.
  structure = ndb.KeyProperty(kind='PlayerStructure')

class Unit(ndb.Model):
  """Models a player-owned unit in the game."""
  # What type of unit it is.
  # 0 = Worker
  # 1 = Soldier
  # See constants_units.py for mapping.
  unit_type = ndb.IntegerProperty()

  # Who owns this unit.
  unit_owner_key = ndb.KeyProperty(kind='Player')

  # How much health this unit has.
  health = ndb.IntegerProperty()

  # What equipment this unit is wearing.
  weapon = ndb.KeyProperty(kind='Equipment')
  armor = ndb.KeyProperty(kind='Equipment')

  # What tile this unit is currently standing on.
  location_tile = ndb.KeyProperty(kind="MapTile")


class Weapon(ndb.Model):
  """Models a weapon in the game."""
  # The type of weapon.
  # 0: Sword
  weapon_type = ndb.IntegerProperty(choices=WEAPON_TYPE_INT_MAPPING.values())

  # How much damage the weapon does.
  power = ndb.IntegerProperty()

  # How likely the weapon is to break after each attack.
  # This should be a number in range [0, 1].
  reliability = ndb.FloatProperty()


class Armor(ndb.Model):
  """Models an armor in the game."""
  # The type of armor.
  # 0: Plate
  armor_type = ndb.IntegerProperty(choices=ARMOR_TYPE_INT_MAPPING.values())

  # How much damage it absorbs for the user, as a percentage.
  # This should be a numebr in range [0, 1]. TODO: Make custom property.
  damage_reduction = ndb.FloatProperty()

  # How much more damage the armor can take before breaking.
  # Note: This is not max durability, it is current.
  durability = ndb.IntegerProperty()


class Equipment(ndb.Model):
  """The top level class for all equipment models in game."""
  # Which type of equipment this is.
  # 0: Weapon
  # 1: Armor
  equipment_type = ndb.IntegerProperty(
      choices=EQUIPMENT_TYPE_INT_MAPPING.values())

  # Which player owns the equipment.
  player = ndb.KeyProperty(kind='Player')

  # Weapon data.
  weapon_data = ndb.StructuredProperty(Weapon)

  # Armor data.
  armor_data = ndb.StructuredProperty(Armor)


class MoveOrder(ndb.Model):
  """Models a move order in the game."""
  # The unit to move.
  unit_key = ndb.KeyProperty(kind='Unit')

  # The tile to move the unit to.
  destination_map_tile_key = ndb.KeyProperty(kind='MapTile')

class BuildCampOrder(ndb.Model):
  """Models a build camp order in the game."""
  # The unit that will build the camp.
  unit_key = ndb.KeyProperty(kind='Unit')

  # The resource that the camp will harvest.
  tile_resource_key = ndb.KeyProperty(kind='TileResource')

class Order(ndb.Model):
  """Models an order in the game."""
  # The type of order
  # 0: Move
  # 1: Build Camp
  order_type = ndb.IntegerProperty(choices=ORDER_TYPE_INT_MAPPING.values())

  # TODO: Add player.

  # The data needed to peform a move order.
  move_order = ndb.StructuredProperty(MoveOrder)

  # The data needed to perform a build camp order.
  build_camp_order = ndb.StructuredProperty(BuildCampOrder)

class HarvestingCamp(ndb.Model):
  """Models a Harvesting Camp player structure."""
  # Which resource the camp is harvesting.
  tile_resource_key = ndb.KeyProperty(kind='TileResource')

class PlayerStructure(ndb.Model):
  """Models anything that a player can build in the world."""
  # Type of structure.
  # 0: Harvesting Camp
  structure_type = ndb.IntegerProperty(
      choices=STRUCTURE_TYPE_INT_MAPPING.values())

  # Which player owns this camp.
  owner_key = ndb.KeyProperty(kind='Player')

  # Harvesting camp data
  harvesting_camp_data = ndb.StructuredProperty(HarvestingCamp)

  # How much damage the structure must take before it is destroyed.
  health = ndb.IntegerProperty()

  # Where the structure is located on the map.
  location = ndb.KeyProperty(kind="MapTile")
