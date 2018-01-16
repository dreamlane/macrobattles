## userhandlers.py Handles API calls involving users.
import json
import logging

from google.appengine.api import users

from gamelogic import addPlayerToWorld
from models import Player
from requestutils import ResponseBuilder

class UserLoginHandler():
  """ This is the handler for logging in users."""

  @staticmethod
  def handleLoginRequest(request):
    """Handles a login request."""
    username = request.get('username')
    # TODO: Make passwords cryptographically secure.
    password = request.get('password')

    error_message = 'Login fail.'
    query = Player.query(Player.username == username)
    if query.count() > 0:
      player = query.get()
      if player.password == password:
        # Return the urlsafe player key to the client.
        # TODO: Figure out authentication.
        data = {'key': player.key.urlsafe()}
        return ResponseBuilder().setData(json.dumps(data)).build()
      else:
        error_message += ' Password incorrect.'
    else:
      logging.info('username is: ' + username)
      error_message += ' Username not found.'
    return ResponseBuilder().setErrorMessage(error_message).build()

  @staticmethod
  def handleRegisterRequest(request):
    """Handles a Registeration request."""
    response = ResponseBuilder()
    username = request.get('username')
    password = request.get('password')

    if len(username) < 3:
      logging.info('username is: ' + username)
      response.setErrorMessage('Username is too short.')
      return response.build()

    # TODO: add password length verification.

    # Check for username collision
    # TODO: Do a transaction here with username as part of the key.
    query = Player.query(Player.username == username)
    if query.count() > 0:
      response.setErrorMessage('The username is already in use.')
      return response.build()

    player_key = Player(
        username=username,
        password=password).put()

    # TODO: Figure out how to have players join the world in a better way.
    addPlayerToWorld({'player_id': player_key.urlsafe()})

    data = {'key': player_key.urlsafe()}
    return ResponseBuilder().setData(json.dumps(data)).build()
