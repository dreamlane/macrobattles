## main.py Handles all of the request routing for the server.

import logging
import webapp2
from userhandlers import UserLoginHandler
from requestutils import BaseHandler
from gamelogic import addPlayerToWorld
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
    # TODO, figure out authentication!
    addPlayerToWorld(self.request.get('player_id'))

class SellResourceHandler(BaseHandler):
  def post(self):
    player_id = self.request.get('player_id')
    resource_id = self.request.get('resource_id')
    quantity = self.request.get('quantity')
    sellResource(player_id, resource_id, quantity)

class HireUnitHandler(BaseHandler):
  def post(self):
    player_id = self.request.get('player_id')
    unit_type = self.request.get('unit_type')
    hireUnit(player_id, unit_type)
    # Todo: write response

class EquipUnitHandler(BaseHandler):
  def post(self):
    # TODO: Handle auth/session.
    unit_id = self.request.get('unit_id')
    equipment_id = self.request.get('equipment_id')
    # TODO: write response
    equipUnit(unit_id, equipment_id)

config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'r7ps9bd6daoc1984shmogogin'}
app = webapp2.WSGIApplication([
  webapp2.Route(r'/login', handler=LoginHandler, name='login'),
  webapp2.Route(r'/register', handler=RegisterHandler, name='register'),
  webapp2.Route(r'/join-game', handler=JoinGameHandler, name='join-game'),
  webapp2.Route(r'/sell-resource', handler=SellResourceHandler, name='sell-resource'),
  webapp2.Route(r'/hire-unit', handler=HireUnitHandler, name='hire-unit'),
  webapp2.Route(r'/equip-unit', handler=EquipUnitHandler, name='equip-unit'),
], debug=True, config=config)
