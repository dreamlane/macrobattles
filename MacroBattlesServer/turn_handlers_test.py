## turn_handlers_test.py
import sys
import unittest
# TODO: This only works on Ben's PC, make this a configuration not in the repo.
sys.path.insert(1, 'D:/Cloud SDK/google-cloud-sdk/platform/google_appengine')
sys.path.insert(1, 'D:/Cloud SDK/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from turn_handlers import TurnHandler
# TODO Write unit tests for turn handlers.

