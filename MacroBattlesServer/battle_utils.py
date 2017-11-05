## battle_utils.py
import logging
import random

from constants_units import UNIT_BASE_DAMAGE
from constants_units import UNIT_TYPE_KEY_MAPPING

def getAttackPower(unit):
  power = UNIT_BASE_DAMAGE[UNIT_TYPE_KEY_MAPPING[unit.unit_type]]
  if unit.weapon:
    power += unit.weapon.get().weapon_data.power
  return power

def getDamageReduction(unit):
  if unit.armor:
    return 1.0 - unit.armor.get().armor_data.damage_reduction
  return 1.0

def resolveAttack(attacker, defender):
  # Code assumes that the attacker and defender are valid units.
  attacker_power = getAttackPower(attacker)
  defender_damage_reduction = getDamageReduction(defender)
  # We add one to the int value of the damage calculation to round it upwards.
  # The additional damage makes it impossible for an attack to do 0 damage.
  damage_to_defender = int(attacker_power*defender_damage_reduction) + 1
  # Any damage that the armor deflects form the unit is taken by the armor.
  damage_dealt_to_armor = attacker_power - damage_to_defender

  defender.health -= damage_to_defender

  # Deal damage to armor if present.
  if (defender.armor):
    armor = defender.armor.get()
    armor.armor_data.durability -= damage_dealt_to_armor
    # If the armor has no more durability, destroy it.
    if armor.armor_data.durability <= 0:
      logging.info('Armor durability depleted.')
      armor.key.delete()
      # TODO: determine if I need to update the defender.armor field.

  # Weapons have a random chance to break.
  if attacker.weapon:
    weapon = attacker.weapon.get()
    if random.random() > weapon.weapon_data.reliability:
      logging.info('Weapon destroyed')
      weapon.key.delete()
      # TODO: determine if I need to update the attacker.weapon field.

  defender.put()

