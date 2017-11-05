## constants_units.py
""" This file defines all of the constant values for units."""

WORKER_KEY = "WORKER"
SOLDIER_KEY = "SOLDIER"

""" The key-value pairs for types of resources."""
UNIT_TYPE_INT_MAPPING = {
  WORKER_KEY: 0,
  SOLDIER_KEY: 1
}

UNIT_TYPE_KEY_MAPPING = {
  UNIT_TYPE_INT_MAPPING[WORKER_KEY]: WORKER_KEY,
  UNIT_TYPE_INT_MAPPING[SOLDIER_KEY]: SOLDIER_KEY
}

UNIT_COSTS = {
  WORKER_KEY: 100,
  SOLDIER_KEY: 100,
}

UNIT_BASE_HEALTH = {
  WORKER_KEY: 26,
  SOLDIER_KEY: 75,
}

UNIT_BASE_DAMAGE = {
  WORKER_KEY: 2,
  SOLDIER_KEY: 6,
}
