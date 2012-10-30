"""Client wrapper
"""

import copy

import requests


class Client(object):
    """Ceilometer client.
    """

    def __init__(self, keystone_client=None,
                 base_url="http://localhost:9000",
                 service_type="metering",
                 endpoint_type="adminURL"):
        self.keystone_client = keystone_client
        if keystone_client:
            base_url = keystone_client.service_catalog.get_endpoints(
                service_type=service_type,
                endpoint_type=endpoint_type)
            self.base_url = base_url[service_type][0][endpoint_type].rstrip("/")
        else:
            self.base_url = base_url
        self.version = 'v1'

    def get(self, url, **kwargs):
        """Emit a get request with the Keystone authentication token set in
        headers.

        """
        if self.keystone_client:
            if 'headers' in kwargs:
                kwargs['headers']['X-Auth-Token'] = self.keystone_client.auth_token
            else:
                kwargs['headers'] = {'X-Auth-Token': self.keystone_client.auth_token}

        return requests.get('/'.join([self.base_url,
                                      self.version,
                                      url.lstrip('/'),
                                  ]),
                            **kwargs)

    def get_projects(self):
        """Returns list of project ids known to the server."""
        r = self.get('/projects')
        return r.json.get('projects', [])

    def get_resources(self, project_id, start_timestamp=None,
                      end_timestamp=None):
        """Returns details about the named project."""
        args = {}
        if start_timestamp:
            args['start_timestamp'] = start_timestamp.isoformat()
        if end_timestamp:
            args['end_timestamp'] = end_timestamp.isoformat()

        r = self.get('/projects/%s/resources' % project_id,
                     params=args)
        if r.status_code == requests.codes.not_found:
            raise ValueError('Unknown project %r' % project_id)
        return r.json.get('resources', [])

    def get_events(self, resource_id, meter, start_timestamp=None,
                      end_timestamp=None):
        """Returns events about the resource in the time range."""
        args = {}
        if start_timestamp:
            args['start_timestamp'] = start_timestamp.isoformat()
        if end_timestamp:
            args['end_timestamp'] = end_timestamp.isoformat()

        r = self.get('/resources/%s/meters/%s' % (resource_id, meter),
                     params=args)
        if r.status_code == requests.codes.not_found:
            raise ValueError('Unknown resource %r' % resource_id)
        return r.json.get('events', [])

    def get_resource_duration_info(self, resource_id, meter,
            start_timestamp=None, end_timestamp=None,
            search_offset=0,
            ):
        """Returns duration, min, and max timestamp of the resource
        for the given meter within the time range.
        """
        args = {'search_offset': search_offset,
                }
        if start_timestamp:
            args['start_timestamp'] = start_timestamp.isoformat()
        if end_timestamp:
            args['end_timestamp'] = end_timestamp.isoformat()

        r = self.get('/resources/%s/meters/%s/duration' % (resource_id, meter),
                     params=args)
        if r.status_code == requests.codes.not_found:
            raise ValueError('Unknown resource %r' % resource_id)
        return copy.copy(r.json)

    def _get_project_sum_or_max(self, sum_or_max, project_id, meter,
            start_timestamp=None, end_timestamp=None, search_offset=0):
        """Returns the total or max volume for the specified meter for a
        project within the time range.
        """
        args = {'search_offset': search_offset,
                }
        if start_timestamp:
            args['start_timestamp'] = start_timestamp.isoformat()
        if end_timestamp:
            args['end_timestamp'] = end_timestamp.isoformat()

        r = self.get(('/projects/%s/meters/%s/volume/%s' %
                      (project_id, meter, sum_or_max)),
                     params=args)
        return r.json.get('volume')

    def get_project_volume_max(self, project_id, meter,
            start_timestamp=None, end_timestamp=None, search_offset=0):
        """Returns the max volume for the specified meter for a project
        within the time range.
        """
        return self._get_project_sum_or_max('max',
                                            project_id,
                                            meter,
                                            start_timestamp,
                                            end_timestamp,
                                            search_offset,
                                            )

    def get_project_volume_sum(self, project_id, meter,
            start_timestamp=None, end_timestamp=None, search_offset=0):
        """Returns the total volume for the specified meter for a project
        within the time range.
        """
        return self._get_project_sum_or_max('sum',
                                            project_id,
                                            meter,
                                            start_timestamp,
                                            end_timestamp,
                                            search_offset,
                                            )

    def _get_resource_sum_or_max(self, sum_or_max, resource_id, meter,
            start_timestamp=None, end_timestamp=None,
            search_offset=0,
            ):
        """Returns the total or max volume for the specified meter for
        a resource within the time range.
        """
        args = {'search_offset': search_offset,
                }
        if start_timestamp:
            args['start_timestamp'] = start_timestamp.isoformat()
        if end_timestamp:
            args['end_timestamp'] = end_timestamp.isoformat()

        r = self.get('/resources/%s/meters/%s/volume/%s' %
                     (resource_id, meter, sum_or_max),
                     params=args)
        return r.json.get('volume')

    def get_resource_volume_max(self, resource_id, meter,
            start_timestamp=None, end_timestamp=None,
            search_offset=0,
            ):
        return self._get_resource_sum_or_max('max',
                                             resource_id,
                                             meter,
                                             start_timestamp,
                                             end_timestamp,
                                             search_offset,
                                             )

    def get_resource_volume_sum(self, resource_id, meter,
            start_timestamp=None, end_timestamp=None,
            search_offset=0,
            ):
        """Returns the total volume for the specified meter for a resource
        within the time range.
        """
        return self._get_resource_sum_or_max('sum',
                                             resource_id,
                                             meter,
                                             start_timestamp,
                                             end_timestamp,
                                             search_offset,
                                             )
