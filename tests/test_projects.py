
import unittest

import mock
from nose import tools

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


    def test_get_project(self):
        self.response.json = {'project': {'id': 'project-id'}}
        with mock.patch('requests.get') as getter:
            getter.return_value = self.response
            prj = self.c.get_project('project-id')
        self.assertEquals(prj, {'id': 'project-id'})


    def test_get_project_not_found(self):
        self.response.status_code = requests.codes.not_found
        with mock.patch('requests.get') as getter:
            getter.return_value = self.response
            self.assertRaisesRegexp(ValueError, 'project-id',
                                    self.c.get_project, 'project-id',
                                    )

