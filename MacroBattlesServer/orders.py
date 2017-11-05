## orders.py Handles request routing for /orders/.* requests.

import logging
import webapp2

from order_handlers import handleBuildCampOrderRequest
from order_handlers import handleUnitMoveRequest
from requestutils import BaseHandler

class MoveUnitOrderHandler(BaseHandler):
  def post(self):
    # TODO: handle authentication/session
    unit_id = self.request.get('unit_id')
    target_tile_id = self.request.get('target_tile_id')
    #TODO: write response.
    handleUnitMoveRequest(unit_id, target_tile_id)

class BuildCampOrderHandler(BaseHandler):
  def post(self):
    # TODO: handle auth/session
    unit_id = self.request.get('unit_id')
    tile_resource_id = self.request.get('tile_resource_id')
    # TODO: write response:
    handleBuildCampOrderRequest(unit_id, tile_resource_id)

config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'r7ps9bd6daoc1984shmogogin'}
app = webapp2.WSGIApplication([
    webapp2.Route(r'/orders/move-unit', handler=MoveUnitOrderHandler, name='move-unit'),
    webapp2.Route(r'/orders/build-camp', handler=BuildCampOrderHandler, name='build-camp')
], debug=True, config=config)
