## resource_utils_test.py

import unittest

from context import models
from resource_utils import determineHarvestRate
class ResourceUtilsTest(unittest.TestCase):

	def testDetermineHarvestRate(self):
		testTileResource = models.TileResource(saturation = 1)
		self.assertEqual(0, determineHarvestRate(testTileResource))
		testTileResource = models.TileResource(saturation = 100)
		self.assertEqual(33, determineHarvestRate(testTileResource))
		testTileResource = models.TileResource(saturation = 0)
		self.assertEqual(0, determineHarvestRate(testTileResource))