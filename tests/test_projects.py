
import unittest

import mock

import requests

from ceilometerclient import client


class ProjectTests(unittest.TestCase):

    def setUp(self):
        ksclient = mock.Mock()
        ksclient.auth_token = "abc*token*abc"
        ksclient.service_catalog = mock.Mock()
        ksclient.service_catalog.get_endpoints = mock.Mock(
            return_value={u'metering':
                          [{u'adminURL': u'http://localhost:9000/',
                            u'region': u'RegionOne',
                            u'id': u'8e88da8f3ca54ed8a1c4b56ccb39d2b6'}]})
        self.c = client.Client(ksclient)
        self.response = mock.Mock()

    def test_get_projects(self):
        self.response.json = {'projects': ['project1', 'project2']}
        with mock.patch('requests.get') as getter:
            getter.return_value = self.response
            prjs = self.c.get_projects()
        self.assertEquals(prjs, ['project1', 'project2'])

    def test_get_project_volume_max(self):
        self.response.json = {'volume': 123}
        with mock.patch('requests.get') as getter:
            getter.return_value = self.response
            volume = self.c.get_project_volume_max('project1', 'meter')
        self.assertEquals(volume, 123)

    def test_get_project_volume_sum(self):
        self.response.json = {'volume': 456}
        with mock.patch('requests.get') as getter:
            getter.return_value = self.response
            volume = self.c.get_project_volume_sum('project1', 'meter')
        self.assertEquals(volume, 456)
