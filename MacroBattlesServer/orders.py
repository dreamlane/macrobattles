## orders.py Handles request routing for /orders/.* requests.

import logging
import webapp2

from orders_handlers import handleUnitMoveRequest
from requestutils import BaseHandler

class MoveUnitOrderHandler(BaseHandler):
  def post(self):
    # TODO: handle authentication/session
    unit_id = self.request.get('unit_id')
    target_tile_id = self.request.get('target_tile_id')
    #TODO: write response.
    handleUnitMoveRequest(unit_id, target_tile_id)

config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'r7ps9bd6daoc1984shmogogin'}
app = webapp2.WSGIApplication([
    webapp2.Route(r'/orders/move-unit', handler=MoveUnitOrderHandler, name='move-unit'),
], debug=True, config=config)
