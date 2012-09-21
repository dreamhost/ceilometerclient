"""Tool for dumping ceilometer data to a csv file
"""

import argparse
import csv
import sys

import ceilometerclient


FIELD_NAMES = ['project_id', 'resource_id', 'instance_flavor',
               'first_seen', 'last_seen', 'duration']

def dump_instances(ceilometer, dumper):
    for project_id in ceilometer.get_projects():
        if project_id is None:
            continue  # for some reason we get None sometimes

        for resource in ceilometer.get_resources(project_id=project_id):
            resource_id = resource['resource_id']
            meters = [item.get('counter_name') for item in resource['meter']]

            for meter in meters:
                if meter.startswith('instance:'):
                    flavor = meter.partition(':')[-1]

                    duration_info = ceilometer.get_resource_duration_info(
                        resource_id=resource_id,
                        meter=meter,
                        )

                    dumper.writerow(dict(
                        project_id=project_id,
                        resource_id=resource_id,
                        instance_flavor=flavor,
                        first_seen=duration_info['start_timestamp'],
                        last_seen=duration_info['end_timestamp'],
                        duration=duration_info['duration'],
                        ))

def main():
    parser = argparse.ArgumentParser(
        description='Dump ceilometer data to a csv file.')
    parser.add_argument('clienturl', metavar='URL', type=str,
                        help='url for the ceilometer API endpoint')
    parser.add_argument('filename', metavar='FILE', type=str,
                        help='name of the output csv file')
    args = parser.parse_args()

    ceilometer = ceilometerclient.Client(args.clienturl)
    with open(args.filename, 'wb') as csvfile:
        dumper = csv.DictWriter(csvfile, FIELD_NAMES)
        dumper.writeheader()
        dump_instances(ceilometer, dumper)


if __name__ == '__main__':
    sys.exit(main())
