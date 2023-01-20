#!/usr/bin/python3
'''
    Script that reads stdin line by line and computes metrics
'''

import sys


def _print(file_size, status_dict):
    '''
        helper function to print the  results
    '''
    print("File size: {}".format(file_size))
    for key, value in sorted(status_dict.items()):
        if value > 0:
            print("{}: {}".format(key, value))


counter = 0
total_size = 0

status_stats = {'200': 0, '301': 0, '400': 0, '401': 0,
                '403': 0, '404': 0, '405': 0, '500': 0
                }

try:
    for line in sys.stdin:
        data = line.split()
        if len(data) < 9:
            continue
        code = data[7]
        status_stats[code] += 1
        total_size += int(data[8])

        counter += 1
        if counter == 10:
            _print(total_size, status_stats)
            counter = 0
finally:
    _print(total_size, status_stats)
