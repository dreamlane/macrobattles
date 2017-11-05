## constants_weapons.py
""" This file defines all of the constant values for weapons. """

from constants_equipment import SWORD_TEMPLATE_KEY
from constants_equipment import AttributeFormula
from constants_resources import LEATHER_KEY
from constants_resources import METAL_KEY
from constants_resources import WOOD_KEY


""" The key to integer mapping for the Weapon type in ndb.Model. """
WEAPON_TYPE_INT_MAPPING = {
  SWORD_TEMPLATE_KEY: 0,
}

WEAPON_POWER_FORMULA = {
  SWORD_TEMPLATE_KEY: AttributeFormula(
      formula = '((mh*0.33334 + ml*0.33334 + md*0.33334)/50)',
      properties = {
        'mh': (METAL_KEY, 'metal_properties.hardness'),
        'ml': (METAL_KEY, 'metal_properties.lustre'),
        'md': (METAL_KEY, 'metal_properties.density')
      })
}

WEAPON_RELIABILITY_FORMULA = {
  SWORD_TEMPLATE_KEY: AttributeFormula(
    formula = '(1/(1001-(.33333*mh+.33333*lf+.33333*ww)))*(.995-.90)+.90',
    properties = {
      'mh': (METAL_KEY, 'metal_properties.hardness'),
      'lf': (LEATHER_KEY,'leather_properties.flexibility'),
      'ww': (WOOD_KEY, 'wood_properties.workability')
    }
  )
}
