import unittest
import requests
from django.conf import settings

class SubjectTestCase(unittest.TestCase):

    def setUp(self):
        self.routes_to_test = [
            '',
            'list/',
            'browse/',
            'search/',
            'about/',
            'untl-bs.json',
            'admin/',
        ]

    def test_response_codes(self):
        for test_route in self.routes_to_test:
            response = requests.get('http://%s/subjects/%s' % (settings.DOMAIN, test_route))
            self.assertEqual(response.status_code, 200)
