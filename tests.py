import unittest
import random
from time import sleep
import os

from mapquest import *

class MapQuestTestError(Exception):
    """MapQuest test exception"""

    def __init__(self, reason):
        self.reason = unicode(reason)

    def __str__(self):
        return self.reason

try:
    from test_settings import *
except ImportError:
    pass
    
class NominatimTests(unittest.TestCase):
    def setUp(self):
        self.api = API()

    def testBasicSearch(self):
        """Search for basic place. We'll do the Ferry Market"""
        ret = self.api.nominatim(q="Ferry Plaza, San Francisco, CA")
        self.assertNotEqual(ret, [])
        ret = ret[0]
    
        self.assertEqual(ret['lat'], '37.795556930015')
        self.assertEqual(ret['lon'], "-122.392124051039")
        
class DirectionsTests(unittest.TestCase):
    def setUp(self):
        self.api = API()
        
    def testBasicNav(self):
        # start - 717 Market St
        # end  - Ferry Plaza, San Francisco, CA
        
        # we shrunk the precision to match return values for easier comparison
        start_lat = "37.786861"
        start_lon = "-122.403689"
        end_lat = "37.795556"
        end_lon = "-122.392124"
        
        start = start_lat+","+start_lon
        end = end_lat+","+end_lon
        
        ret = self.api.directions(start=start, end=end)
        
        # verify start and end points are reflected in response
        self.assertNotEqual(ret, {})
        locations = ret['route']['locations']
        
        self.assertEqual(len(locations), 2)
        
        self.assertEqual(str(locations[0]['latLng']['lng']), start_lon)
        self.assertEqual(str(locations[0]['latLng']['lat']), start_lat)
        
        self.assertEqual(str(locations[1]['latLng']['lng']), end_lon)
        self.assertEqual(str(locations[1]['latLng']['lat']), end_lat)
        
    def testPedestrianNav(self):
        start_lat = "37.7868609332517"
        start_lon = "-122.403689949149"
        end_lat = "37.795556930015"
        end_lon = "-122.392124051039"

        start = start_lat+","+start_lon
        end = end_lat+","+end_lon

        ret = self.api.directions(start=start, end=end, routeType='pedestrian')
        self.assertNotEqual(ret, {})
        
        legs = ret['route']['legs']
        self.assertNotEqual(legs, [])
        
        legs = legs[0]
        
        maneuvers = legs['maneuvers']
        self.assertNotEqual(maneuvers, [])
        
        # skip the last step, as it doesn't have a transport Mode
        for m in maneuvers[:-1]:
            self.assertEqual(m['transportMode'], 'WALKING')
        
if __name__ == '__main__':
    unittest.main()