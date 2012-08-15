
import unittest

import mock

import requests

from ceilometerclient import client


class ProjectTests(unittest.TestCase):

    def setUp(self):
        self.c = client.Client('http://localhost:9000')
        self.response = mock.Mock()

    def test_get_projects(self):
        self.response.json = {'projects': ['project1', 'project2']}
        with mock.patch('requests.get') as getter:
            getter.return_value = self.response
            prjs = self.c.get_projects()
        self.assertEquals(prjs, ['project1', 'project2'])

