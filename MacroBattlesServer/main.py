## main.py is Handles all of the request routing for the server.

import logging
import webapp2
from userhandlers import UserLoginHandler
from requestutils import BaseHandler
from gamelogic import addPlayerToWorld
from gamelogic import sellResource

class LoginHandler(BaseHandler):
  def post(self):
    self.response.write(UserLoginHandler.handleLoginRequest(self.request))

class RegisterHandler(BaseHandler):
  def post(self):
    self.response.write(UserLoginHandler.handleRegisterRequest(self.request))

class JoinGameHandler(BaseHandler):
  def get(self):
    # TODO, figure out authentication!
    addPlayerToWorld(self.request.get('username'))

class SellResourceHandler(BaseHandler):
  def post(self):
    player_id = self.request.get('player_id')
    resource_id = self.request.get('resource_id')
    quantity = self.request.get('quantity')
    sellResource(player_id, resource_id, quantity)

config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'r7ps9bd6daoc1984shmogogin'}
app = webapp2.WSGIApplication([
  webapp2.Route(r'/login', handler=LoginHandler, name='login'),
  webapp2.Route(r'/register', handler=RegisterHandler, name='register'),
  webapp2.Route(r'/join-game', handler=JoinGameHandler, name='join-game'),
  webapp2.Route(r'/sell-resource', handler=SellResourceHandler, name='sell-resource'),
], debug=True, config=config)
