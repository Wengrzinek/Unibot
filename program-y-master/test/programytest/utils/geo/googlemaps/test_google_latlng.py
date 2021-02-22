import json
import os
import unittest

from programy.utils.geo.google import GoogleMaps, GoogleDistance, GoogleDirections
from programy.utils.geo.latlong import LatLong


#############################################################################
#

class MockGoogleMaps(GoogleMaps):

    def __init__(self, response):
        self._response = response

    def _get_response_as_json(self, url):
        return self._response


class GoogleLatLngTests(unittest.TestCase):

    def test_location(self):
        googlemaps = MockGoogleMaps(response={"results": [
                                                {
                                                  "address_components": [
                                                    {
                                                      "long_name": "KY3 9UR",
                                                      "short_name": "KY3 9UR",
                                                      "types": [
                                                        "postal_code"
                                                      ]
                                                    },
                                                    {
                                                      "long_name": "Glamis Road",
                                                      "short_name": "Glamis Rd",
                                                      "types": [
                                                        "route"
                                                      ]
                                                    },
                                                    {
                                                      "long_name": "Kinghorn",
                                                      "short_name": "Kinghorn",
                                                      "types": [
                                                        "locality",
                                                        "political"
                                                      ]
                                                    },
                                                    {
                                                      "long_name": "Burntisland",
                                                      "short_name": "Burntisland",
                                                      "types": [
                                                        "postal_town"
                                                      ]
                                                    },
                                                    {
                                                      "long_name": "Fife",
                                                      "short_name": "Fife",
                                                      "types": [
                                                        "administrative_area_level_2",
                                                        "political"
                                                      ]
                                                    },
                                                    {
                                                      "long_name": "Scotland",
                                                      "short_name": "Scotland",
                                                      "types": [
                                                        "administrative_area_level_1",
                                                        "political"
                                                      ]
                                                    },
                                                    {
                                                      "long_name": "United Kingdom",
                                                      "short_name": "GB",
                                                      "types": [
                                                        "country",
                                                        "political"
                                                      ]
                                                    }
                                                  ],
                                                  "formatted_address": "Glamis Rd, Kinghorn, Burntisland KY3 9UR, UK",
                                                  "geometry": {
                                                    "bounds": {
                                                      "northeast": {
                                                        "lat": 56.072498,
                                                        "lng": -3.1744103
                                                      },
                                                      "southwest": {
                                                        "lat": 56.071628,
                                                        "lng": -3.1757585
                                                      }
                                                    },
                                                    "location": {
                                                      "lat": 56.0720397,
                                                      "lng": -3.1752001
                                                    },
                                                    "location_type": "APPROXIMATE",
                                                    "viewport": {
                                                      "northeast": {
                                                        "lat": 56.0734119802915,
                                                        "lng": -3.173735419708498
                                                      },
                                                      "southwest": {
                                                        "lat": 56.0707140197085,
                                                        "lng": -3.176433380291502
                                                      }
                                                    }
                                                  },
                                                  "place_id": "ChIJT3l_Pwi2h0gRCp8egoK5hcU",
                                                  "types": [
                                                    "postal_code"
                                                  ]
                                                }
                                              ],
                                              "status": "OK"
                                            })
        self.assertIsNotNone(googlemaps)

        latlng = googlemaps.get_latlong_for_location("KY3 9UR")
        self.assertIsNotNone(latlng)
        self.assertIsInstance(latlng, LatLong)
        self.assertEqual(latlng.latitude, 56.0720397)
        self.assertEqual(latlng.longitude, -3.1752001)
