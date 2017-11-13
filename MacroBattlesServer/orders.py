## orders.py Handles request routing for /orders/.* requests.

import json
import logging
import webapp2

from order_handlers import handleBuildCampOrderRequest
from order_handlers import handleUnitMoveRequest
from requestutils import BaseHandler
from requestutils import areRequiredKeysPresent

class MoveUnitOrderHandler(BaseHandler):
  def post(self):
    # TODO: handle authentication/session
    required_keys = ['unit_id', 'target_tile_id']
    inputs = json.loads(self.request.body)
    if not areRequiredKeysPresent(required_keys, inputs):
      logging.error('The input for orders/move-unit is missing data.')
      # TODO: Write a failure response.
      return None
    #TODO: write response.
    handleUnitMoveRequest(inputs)

class BuildCampOrderHandler(BaseHandler):
  def post(self):
    # TODO: handle auth/session
    required_keys = ['unit_id', 'tile_resource_id']
    inputs = json.loads(self.request.body)
    if not areRequiredKeysPresent(required_keys, inputs):
      logging.error('The input for orders/build-camp is missing data.')
      # TODO: Write a failure response.
      return None
    # TODO: write response:
    handleBuildCampOrderRequest(inputs)

config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'r7ps9bd6daoc1984shmogogin'}
app = webapp2.WSGIApplication([
    webapp2.Route(r'/orders/move-unit', handler=MoveUnitOrderHandler, name='move-unit'),
    webapp2.Route(r'/orders/build-camp', handler=BuildCampOrderHandler, name='build-camp')
], debug=True, config=config)
