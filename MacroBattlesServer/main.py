## main.py Handles all of the request routing for the server.

import json
import logging
import webapp2
from userhandlers import UserLoginHandler
from requestutils import BaseHandler
from requestutils import areRequiredKeysPresent
from gamelogic import addPlayerToWorld
from gamelogic import craftItem
from gamelogic import sellResource
from gamelogic import hireUnit
from gamelogic import equipUnit

class LoginHandler(BaseHandler):
  def post(self):
    self.response.write(UserLoginHandler.handleLoginRequest(self.request))

class RegisterHandler(BaseHandler):
  def post(self):
    self.response.write(UserLoginHandler.handleRegisterRequest(self.request))

class JoinGameHandler(BaseHandler):
  def post(self):
    # TODO: Handle auth/session.
    required_keys = ['player_id']
    inputs = json.loads(self.request.body)
    if not areRequiredKeysPresent(required_keys, inputs):
      logging.error('The input for join-game is missing data.')
      # TODO: Write a failure response.
      return None
    inputs = json.loads(self.request.body)
    addPlayerToWorld(inputs)
    # Todo: write response

class SellResourceHandler(BaseHandler):
  def post(self):
    # TODO: Handle auth/session.
    required_keys = ['player_id', 'resource_id', 'quantity']
    inputs = json.loads(self.request.body)
    if not areRequiredKeysPresent(required_keys, inputs):
      logging.error('The input for sell-resource is missing data.')
      # TODO: Write a failure response.
      return None
    sellResource(inputs)
    # Todo: write response

class HireUnitHandler(BaseHandler):
  def post(self):
    # TODO: Handle auth/session.
    required_keys = ['player_id', 'unit_type_string']
    inputs = json.loads(self.request.body)
    if not areRequiredKeysPresent(required_keys, inputs):
      logging.error('The input for hire-unit is missing data.')
      # TODO: Write a failure response.
      return None
    hireUnit(inputs)
    # Todo: write response

class EquipUnitHandler(BaseHandler):
  def post(self):
    # TODO: Handle auth/session.
    required_keys = ['unit_id', 'equipment_id']
    inputs = json.loads(self.request.body)
    if not areRequiredKeysPresent(required_keys, inputs):
      logging.error('The input for equip-unit is missing data.')
      # TODO: Write a failure response.
      return None
    inputs = json.loads(self.request.body)
    equipUnit(inputs)
    # TODO: write response

class CraftEquipmentHandler(BaseHandler):
  def post(self):
    # TODO: handle auth/session.
    required_keys = ['player_id', 'equipment_template_key']
    inputs = json.loads(self.request.body)
    if not areRequiredKeysPresent(required_keys, inputs):
      logging.error('The input for craft-equipment is missing data.')
      # TODO: Write a failure response.
      return None
    inputs = json.loads(self.request.body)
    craftItem(inputs)
    # TODO: write response.

config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'r7ps9bd6daoc1984shmogogin'}
app = webapp2.WSGIApplication([
  webapp2.Route(r'/login', handler=LoginHandler, name='login'),
  webapp2.Route(r'/register', handler=RegisterHandler, name='register'),
  webapp2.Route(r'/join-game', handler=JoinGameHandler, name='join-game'),
  webapp2.Route(r'/sell-resource', handler=SellResourceHandler, name='sell-resource'),
  webapp2.Route(r'/hire-unit', handler=HireUnitHandler, name='hire-unit'),
  webapp2.Route(r'/equip-unit', handler=EquipUnitHandler, name='equip-unit'),
  webapp2.Route(r'/craft-equipment', handler=CraftEquipmentHandler, name='craft-equipment'),
], debug=True, config=config)
