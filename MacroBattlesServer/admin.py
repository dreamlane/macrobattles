## admin.py Handles routing for administrative URIs

import webapp2

from google.appengine.api import users
from turnhandlers import TurnHandler
from test_handlers import testGivePlayerEquipment
from test_handlers import testGivePlayerResource
from gamelogic import *

class AdminLoginHandler(webapp2.RequestHandler):
  def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                nickname, logout_url)
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)

        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))

class TestTurnHandler(webapp2.RequestHandler):
    def get(self):
        # TODO: make sure this is asyncronous, in case the calculations for a turn take a long time.
        TurnHandler.handleTurn();

class TestMapGeneration(webapp2.RequestHandler):
  def post(self):
    generateMapTiles()

class TestGivePlayerResource(webapp2.RequestHandler):
    def post(self):
        testGivePlayerResource(self.request.get('player_id'))

class TestGivePlayerEquipment(webapp2.RequestHandler):
    def post(self):
        testGivePlayerEquipment(self.request.get('player_id'))

app = webapp2.WSGIApplication([
    webapp2.Route(r'/admin/login', handler=AdminLoginHandler, name='admin-login'),
    webapp2.Route(r'/admin/turn', handler=TestTurnHandler, name='admin-turn'),
    webapp2.Route(r'/admin/make-map', handler=TestMapGeneration, name='admin-make-map'),
    webapp2.Route(r'/admin/give-player-resource-test', handler=TestGivePlayerResource, name='give-player-resource-test'), #TODO: remove
    webapp2.Route(r'/admin/give-player-equipment-test', handler=TestGivePlayerEquipment, name='give-player-equipment-test'), #TODO: remove
], debug=True)
