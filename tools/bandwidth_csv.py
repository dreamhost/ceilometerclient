"""Tool for dumping ceilometer data to a csv file
"""

import argparse
import csv
import datetime
import os
import sys
from urlparse import urlparse

import ceilometerclient
import keystoneclient.v2_0.client as ksclient

METER_FORMAT = 'akanda.bandwidth:%s.%s.%s'

BANDWIDTH_CATEGORIES = ['internal', 'external']
BANDWIDTH_TYPES = ['in', 'out']
BANDWIDTH_VALUETYPES = ['packets', 'bytes']

BANDWIDTH_FIELDS = ['project_id', 'date', 'category', 'type']
BANDWIDTH_FIELDS.extend(BANDWIDTH_VALUETYPES)


def dump_bandwidth(ceilometer, dumper, days):
    today = datetime.datetime.today().replace(hour=0,
                                              minute=0,
                                              second=0,
                                              microsecond=0,
                                              )

    for project_id in ceilometer.get_projects():
        if project_id is None:
            continue  # for some reason we get None sometimes

        for i in range(days):
            start_timestamp = today - datetime.timedelta(days=(i + 1))
            end_timestamp = today - datetime.timedelta(days=i)

            for category in BANDWIDTH_CATEGORIES:
                for type_ in BANDWIDTH_TYPES:
                    # row base fields
                    row_dict = dict(
                        project_id=project_id,
                        date=start_timestamp,
                        category=category,
                        type=type_,
                        )

                    # fill in values for the row
                    for valuetype in BANDWIDTH_VALUETYPES:
                        meter = METER_FORMAT % (category, type_, valuetype)
                        row_dict[valuetype] = ceilometer.get_project_volume_sum(
                            project_id,
                            meter,
                            start_timestamp=start_timestamp,
                            end_timestamp=end_timestamp,
                            )

                    # only write the row if we have data
                    if any((row_dict.get(valuetype) is not None)
                           for valuetype in BANDWIDTH_VALUETYPES):
                        dumper.writerow(row_dict)

def main():
    parser = argparse.ArgumentParser(
        description='Dump ceilometer data to a csv file.')
    parser.add_argument('--auth_url', metavar='URL',
                        default=os.environ.get('OS_AUTH_URL',
                                       'http://localhost:5000/v2.0'),
                        type=str, help='Keystone Authentication URL')
    parser.add_argument('--auth_username',
                        default=os.environ.get('OS_USERNAME', None),
                        type=str, help='Username for Keystone')
    parser.add_argument('--auth_password', default=os.environ.get("OS_PASSWORD"),
                        type=str, help='Password for Keystone')
    parser.add_argument('--auth_tenant_name', default=os.environ.get("OS_TENANT_NAME"),
                        type=str, help='Tenant name for Keystone')
    parser.add_argument('--base-url', default='http://localhost:9000',
                        type=str, help='Ceilometer URL')
    parser.add_argument('--days', metavar='N', type=int, default=1,
                        help='number of days to include in the csvt')
    parser.add_argument('filename', metavar='FILE', type=str,
                        help='name of the output csv file')
    args = parser.parse_args()

    if args.auth_username:
        scheme = urlparse(args.auth_url).scheme
        insecure = False if urlparse(args.auth_url).scheme == "https" else True

        keystone = ksclient.Client(username=args.auth_username,
                                   password=args.auth_password,
                                   tenant_name=args.auth_tenant_name,
                                   auth_url=args.auth_url,
                                   insecure=insecure)
        ceilometer = ceilometerclient.Client(keystone_client=keystone)
    else:
        ceilometer = ceilometerclient.Client(base_url=base_url)

    with open(args.filename, 'wb') as csvfile:
        dumper = csv.DictWriter(csvfile, BANDWIDTH_FIELDS)
        dumper.writeheader()
        dump_bandwidth(ceilometer, dumper, args.days)


if __name__ == '__main__':
    sys.exit(main())
