## requesthandler.py This is the base handler for all webapp2 requests.

import json
import webapp2

from webapp2_extras import sessions

class BaseHandler(webapp2.RequestHandler):
  """Base handler for all sessioned webapp2 requests."""

  def dispatch(self):
    ## Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)
    try:
    # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session(self):
    # Returns a session using the default cookie key.
    return self.session_store.get_session()

class ResponseBuilder():
  """Response class used to build responses to be sent to the clients."""

  # Constants for status. These should match client expectation.
  FAIL_STATUS = 'fail'
  SUCCESS_STATUS = 'success'

  def __init__(self):
    # Assume success, and set to failure for fails.
    self.status = self.SUCCESS_STATUS
    # This holds the error message that will be exposed on client.
    self.error = ''
    # This holds the data that will go to the client on a successful request.
    self.data = {}

  def setErrorMessage(self, errorMessage):
    # Anytime an error message is sent, the request must have failed.
    self.status = self.FAIL_STATUS
    self.error = errorMessage
    return self

  def setData(self, data):
    self.data = data
    return self

  def build(self):
    """Turns this object into a JSON string representation."""
    return json.dumps({
        'status' : self.status,
        'error' : self.error,
        'data' : self.data})
