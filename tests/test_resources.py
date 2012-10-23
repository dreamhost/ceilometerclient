
import datetime
import unittest

import mock
import requests

from ceilometerclient import client

BASE_URL = u'http://localhost:9000'

class ResourceTests(unittest.TestCase):

    def setUp(self):
        ksclient = mock.Mock()
        ksclient.auth_token = "abc*token*abc"
        ksclient.service_catalog = mock.Mock()
        ksclient.service_catalog.get_endpoints = mock.Mock(
            return_value={u'metering':
                          [{u'adminURL': BASE_URL,
                            u'region': u'RegionOne',
                            u'id': u'8e88da8f3ca54ed8a1c4b56ccb39d2b6'}]})
        self.c = client.Client(ksclient)
        self.response = mock.Mock()

    def test_get_resources(self):
        self.response.json = {'resources': ['resource1', 'resource2']}
        with mock.patch('requests.get') as getter:
            getter.return_value = self.response
            rsrces = self.c.get_resources('project-id')
            getter.assert_called_once_with(
                '%s/v1/projects/project-id/resources' % BASE_URL,
                headers={'X-Auth-Token': self.c.ksclient.auth_token},
                params={},
                )
        self.assertEquals(rsrces, ['resource1', 'resource2'])


    def test_get_resources_not_found(self):
        self.response.status_code = requests.codes.not_found
        with mock.patch('requests.get') as getter:
            getter.return_value = self.response
            self.assertRaisesRegexp(ValueError, 'project-id',
                                    self.c.get_resources, 'project-id',
                                    )


    def test_get_resources_with_start_time(self):
        d = datetime.datetime.utcnow()
        self.response.json = {'resources': ['resource1', 'resource2']}
        with mock.patch('requests.get') as getter:
            getter.return_value = self.response
            rsrces = self.c.get_resources('project-id', start_timestamp=d)
            getter.assert_called_once_with(
                '%s/v1/projects/project-id/resources' % BASE_URL,
                headers={'X-Auth-Token': self.c.ksclient.auth_token},
                params={'start_timestamp': d.isoformat()},
                )
        self.assertEquals(rsrces, ['resource1', 'resource2'])


    def test_get_resources_with_end_time(self):
        d = datetime.datetime.utcnow()
        self.response.json = {'resources': ['resource1', 'resource2']}
        with mock.patch('requests.get') as getter:
            getter.return_value = self.response
            rsrces = self.c.get_resources('project-id', end_timestamp=d)
            getter.assert_called_once_with(
                '%s/v1/projects/project-id/resources' % BASE_URL,
                headers={'X-Auth-Token': self.c.ksclient.auth_token},
                params={'end_timestamp': d.isoformat()},
                )
        self.assertEquals(rsrces, ['resource1', 'resource2'])
