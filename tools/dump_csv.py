"""Tool for dumping ceilometer data to a csv file
"""

import argparse
import csv
import sys

import ceilometerclient


RESOURCE_FIELDS = ['project_id', 'resource_id', 'name', 'display_name',
                   'type', 'instance_flavor', 'network_id', 'cidr', 'mac',
                   'ips', 'first_seen', 'last_seen', 'duration', 'size']

def dump_resources(ceilometer, dumper):
    for project_id in ceilometer.get_projects():
        if project_id is None:
            continue  # for some reason we get None sometimes

        for resource in ceilometer.get_resources(project_id=project_id):
            resource_id = resource['resource_id']
            metadata = resource['metadata']
            meters = [item.get('counter_name') for item in resource['meter']]

            for meter in meters:
                type_ = None
                flavor = None
                size = metadata.get('size')

                network_id = None  # subnets and ports
                cidr = None        # subnets (only)
                mac = None         # ports (only)
                ips = None         # ports (only)

                if meter.startswith('instance:'):
                    type_ = 'instance'
                    flavor = meter.partition(':')[-1]
                elif meter == 'volume_size':
                    type_ = 'volume'
                    size = ceilometer.get_resource_volume_max(
                        resource_id=resource_id,
                        meter=meter,
                        )
                elif meter == 'image_size':
                    type_ = 'image'
                elif meter == 'network':
                    type_ = 'network'
                elif meter == 'subnet':
                    type_ = 'subnet'
                    network_id = metadata.get('network_id')
                    cidr = metadata.get('cidr')
                elif meter == 'port':
                    type_ = 'port'
                    network_id = metadata.get('network_id')
                    mac = metadata.get('mac_address')
                    ips = ','.join([item['ip_address']
                                    for item in metadata.get('fixed_ips', [])
                                    if 'ip_address' in item])

                if type_ is not None:
                    duration_info = ceilometer.get_resource_duration_info(
                        resource_id=resource_id,
                        meter=meter,
                        )

                    dumper.writerow(dict(
                        project_id=project_id,
                        resource_id=resource_id,
                        name=metadata.get('name'),
                        display_name=metadata.get('display_name'),
                        type=type_,
                        instance_flavor=flavor,
                        network_id=network_id,
                        cidr=cidr,
                        mac=mac,
                        ips=ips,
                        first_seen=duration_info.get('start_timestamp'),
                        last_seen=duration_info.get('end_timestamp'),
                        duration=duration_info.get('duration'),
                        size=size,
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
        dumper = csv.DictWriter(csvfile, RESOURCE_FIELDS)
        dumper.writeheader()
        dump_resources(ceilometer, dumper)


if __name__ == '__main__':
    sys.exit(main())
