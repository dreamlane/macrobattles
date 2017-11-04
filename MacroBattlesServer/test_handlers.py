## test_handlers.py
## DELETE THIS CRAP EVENTUALLY, ONLY FOR TEMP TESTINGS!

from google.appengine.ext import ndb

from models import Armor
from models import Equipment
from models import HarvestingCamp
from models import MetalProperties
from models import LeatherProperties
from models import PlayerStructure
from models import Resource
from models import ResourceTemplate
from models import Weapon
from models import WoodProperties

def testGivePlayerResource(player_key_string):
  player = ndb.Key(urlsafe=player_key_string).get()
  player.resources.append(Resource(
        resource_template = ResourceTemplate(
            resource_type = 2,
            leather_properties = LeatherProperties(
                durability = 200,
                flexibility = 400,
                smoothness = 600,
            ),
            name = 'testLeather'
        ).put(),
        quantity = 150
    ).put())
  player.put()

def testGivePlayerEquipment(player_key_string):
  player = ndb.Key(urlsafe=player_key_string).get()
  player.equipment.append(Equipment(
    equipment_type = 1,
    armor_data = Armor(
    armor_type = 0,
    damage_reduction = 0.6,
    durability = 400),
  ).put())
  player.equipment.append(Equipment(
    equipment_type = 0,
    weapon_data = Weapon(
    weapon_type = 0,
    power = 20,
    reliability = 0.995),
  ).put())
  player.put()

def testPutCampOnSpot(
      player_key_string,
      map_tile_key_string,
      tile_resource_key_string):
  player_key = ndb.Key(urlsafe=player_key_string)
  map_tile_key = ndb.Key(urlsafe=map_tile_key_string)
  tile_resource_key = ndb.Key(urlsafe=tile_resource_key_string)
  strucutre_key = PlayerStructure(
    structure_type = 0,
    owner_key = player_key,
    harvesting_camp_data = HarvestingCamp(
      tile_resource_key = tile_resource_key
    ),
    health = 100,
    location = map_tile_key
  ).put()
