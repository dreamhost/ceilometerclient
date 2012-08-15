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

    def _get(self, path, **kwds):
        r = requests.get(self._mk_url(path), params=kwds)
        return r.json

    def get_projects(self):
        """Returns list of project ids known to the server."""
        return self._get('/projects').get('projects', [])

