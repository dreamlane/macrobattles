## userhandlers.py Handles API calls involving users.
import logging

from google.appengine.api import users
from models import Player
from requestutils import ResponseBuilder

class UserLoginHandler():
  """ This is the handler for logging in users."""

  @staticmethod
  def handleLoginRequest(request):
    """Handles a login request."""
    username = request.get('username')
    password = request.get('password')

    error_message = 'Login fail.'
    query = Player.query(Player.username == username)
    if query.count() > 0:
      player = query.get()
      if player.password == password:
        return ResponseBuilder().setData
      else:
        error_message += ' Password incorrect.'
    else:
      error_message += ' Username not found.'
    return ResponseBuilder().setErrorMessage(error_message).build()

  @staticmethod
  def handleRegisterRequest(request):
    """Handles a Registeration request."""
    response = ResponseBuilder()
    username = request.get('username')
    password = request.get('password')

    if len(username) < 3:
      response.setErrorMessage('Username is too short.')
      return response.build()

    # TODO: add password length verification.

    # Check for username collision
    # TODO: Do a transaction here with username as part of the key.
    query = Player.query(Player.username == username)
    if query.count() > 0:
      response.setErrorMessage('The username is already in use.')
      return response.build()

    newPlayer = Player(
        username=username,
        password=password)
    newPlayer.put()
    player = {}
    player['username'] = username
    response.setData(player)
    logging.error(response.build())
    return response.build()
