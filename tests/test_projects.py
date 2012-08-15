
import unittest

import mock
import requests

from ceilometerclient import client


def test_get_projects():
    c = client.Client('http://localhost:9000')

    response = mock.Mock()
    response.json = {'projects': ['project1', 'project2']}

    with mock.patch('requests.get') as getter:
        getter.return_value = response

        prjs = c.get_projects()

    assert prjs == ['project1', 'project2']
