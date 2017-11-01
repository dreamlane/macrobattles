## turnhandlers.py Handles API calls involving turns in the game.
## These should only be callable by admins, and cron jobs set to call them.
import logging
import random

from google.appengine.ext import ndb
from models import Player
from names import females
from names import males

class TurnHandler():
  """ This is the handler for making a turn happen. """

  @staticmethod
  def handleTurn():
    """ Makes a turn happen. """
    pass

