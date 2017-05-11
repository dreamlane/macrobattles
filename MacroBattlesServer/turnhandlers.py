## turnhandlers.py Handles API calls involving turns in the game.
## These should only be callable by admins, and cron jobs set to call them.
import logging
import random

from google.appengine.ext import ndb
from models import Player
from models import Townsperson
from names import females
from names import males

class TurnHandler():
  """ This is the handler for making a turn happen. """

  @staticmethod
  def handleTurn():
    """ Makes a turn happen. """
    generateTownspeople()

def generateTownspeople():
  """ Generates the townspeople for the next turn and saves them to the datastore. """
  # NOTE: This is prototype game design. Rules may change.
  # Get the list of players
  query = Player.query()
  townspeople = []
  for player in query.fetch():
    # Create 8 townspeople
    for i in xrange(8):
      townspeople.append(createTownsperson(player))
  ndb.put_multi(townspeople)



def createTownsperson(player):
  female = random.random() < 0.5
  name = ''
  if female:
    name = random.choice(females)
  else:
    name = random.choice(males)
  strength = random.randint(8,26)
  dexterity = random.randint(8,26)
  intelligence = random.randint(8,26)
  cost = strength + dexterity + intelligence + random.randint(0, 20)
  return Townsperson(
    player = player.key,
    name = name,
    cost = cost,
    strength = strength,
    dexterity = dexterity,
    intelligence = intelligence)
