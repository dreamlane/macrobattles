## main.py is Handles all of the request routing for the server.

import logging
import webapp2
from decisionhandlers import TownspersonHireHandler
from userhandlers import UserLoginHandler
from requestutils import BaseHandler

class LoginHandler(BaseHandler):
  def post(self):
    self.response.write(UserLoginHandler.handleLoginRequest(self.request))

class RegisterHandler(BaseHandler):
  def post(self):
    self.response.write(UserLoginHandler.handleRegisterRequest(self.request))

class TownspersonListHandler(BaseHandler):
  def get(self):
    self.session['townsperson'] = 'called'
    self.response.write(self.session)

class TownspersonHandler(BaseHandler):
  def get(self, tp_id):
    self.session['tp_id'] = tp_id
    self.response.write(self.session)

config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'r7ps9bd6daoc1984shmogogin'}
app = webapp2.WSGIApplication([
  webapp2.Route(r'/login', handler=LoginHandler, name='login'),
  webapp2.Route(r'/register', handler=RegisterHandler, name='register'),
  webapp2.Route(r'/townsperson', handler=TownspersonListHandler, name='tp-list'),
  webapp2.Route(r'/townsperson/<tp_id:\d+>', handler=TownspersonHandler, name='tp'),
], debug=True, config=config)
