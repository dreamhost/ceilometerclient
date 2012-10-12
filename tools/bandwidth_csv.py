"""Tool for dumping ceilometer data to a csv file
"""

import argparse
import csv
import datetime
import sys

import ceilometerclient

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
                    for valuetype in BANDWIDTH_VALUETYPES:
                        if row_dict.get(valuetype) is not None:
                            dumper.writerow(row_dict)
                            break

def main():
    parser = argparse.ArgumentParser(
        description='Dump ceilometer bandwidth data to a csv file.')
    parser.add_argument('clienturl', metavar='URL', type=str,
                        help='url for the ceilometer API endpoint')
    parser.add_argument('filename', metavar='FILE', type=str,
                        help='name of the output csv file')
    parser.add_argument('--days', metavar='N', type=int, default=1,
                        help='number of days to include in the csv')
    args = parser.parse_args()

    ceilometer = ceilometerclient.Client(args.clienturl)
    with open(args.filename, 'wb') as csvfile:
        dumper = csv.DictWriter(csvfile, BANDWIDTH_FIELDS)
        dumper.writeheader()
        dump_bandwidth(ceilometer, dumper, args.days)


if __name__ == '__main__':
    sys.exit(main())
