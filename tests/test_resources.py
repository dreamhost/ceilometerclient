
import unittest

import mock

import requests

from ceilometerclient import client


class ResourceTests(unittest.TestCase):

    def setUp(self):
        self.c = client.Client('http://localhost:9000')
        self.response = mock.Mock()

    def test_get_resources(self):
        self.response.json = {'resources': ['resource1', 'resource2']}
        with mock.patch('requests.get') as getter:
            getter.return_value = self.response
            rsrces = self.c.get_resources('project-id')
        self.assertEquals(rsrces, ['resource1', 'resource2'])


    def test_get_resources_not_found(self):
        self.response.status_code = requests.codes.not_found
        with mock.patch('requests.get') as getter:
            getter.return_value = self.response
            self.assertRaisesRegexp(ValueError, 'project-id',
                                    self.c.get_resources, 'project-id',
                                    )

