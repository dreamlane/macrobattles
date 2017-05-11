## models.py Holds all model information.

from google.appengine.ext import ndb

class Player(ndb.Model):
  """Models an individual player of the game"""
  # The player's chosen name or gamertag.
  username = ndb.StringProperty()
  password = ndb.StringProperty(indexed=False)

class Townsperson(ndb.Model):
  """Models a townsperson in the game"""
  # The name of the townsperson, randomly chosen from names.py
  name = ndb.StringProperty(indexed=False)
  # The player who is allowed to hire this individual.
  player = ndb.KeyProperty(kind=Player)
  # The cost to hire this townsperson.
  cost = ndb.IntegerProperty()
  strength = ndb.IntegerProperty()
  dexterity = ndb.IntegerProperty()
  intelligence = ndb.IntegerProperty()

