"""Client wrapper
"""

import requests


class Client(object):
    """Ceilometer client.
    """

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.version = 'v1'

    def _mk_url(self, path):
        return '/'.join([self.base_url,
                         self.version,
                         path.lstrip('/'),
                         ])

    def get_projects(self):
        """Returns list of project ids known to the server."""
        r = requests.get(self._mk_url('/projects'))
        return r.json.get('projects', [])

    def get_resources(self, project_id):
        """Returns details about the named project."""
        r = requests.get(self._mk_url('/projects/%s/resources' % project_id))
        if r.status_code == requests.codes.not_found:
            raise ValueError('Unknown project %r' % project_id)
        return r.json.get('resources', [])
