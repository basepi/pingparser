'''
Parse through the contents of a file generated with this command:

    ping 8.8.8.8 | while read pong; do echo "$(date): $pong"; done > monitor.txt

Output a list of outages based on ping timeouts. Give start and end timestamps,
plus total time offline.

Reads in the whole file, so make sure it's not too enormous.
'''
from __future__ import absolute_import
from __future__ import print_function

import sys


def parse():
    '''
    Main function
    '''
    # Handle missing command line arg
    if not len(sys.argv) > 1:
        print('No file specificed.')
        return
    lines = []

    # Read in entire file
    with open(str(sys.argv[1]), 'r') as f:
        lines = f.readlines()

    # Remove the first line, which is not an actual result
    lines = lines[1:]

    uptime = 0
    skipto = 0
    for i, line in enumerate(lines):
        # If we've evaluated forward due to an outage, skip any already-
        # processed iterations
        if i < skipto:
            continue

        # Check for beginning of outage
        if 'Request timeout' in line:
            downtime = line[:28]
            count = 1
            # Process forward to check for length of outage
            while True:
                if i + count < len(lines) and 'Request timeout' in lines[i + count]:
                    count += 1
                    continue
                break
            print('Down for {0} seconds at {1} after {2} seconds of uptime'.format(count, downtime, uptime))
            uptime = 0
            skipto = i + count
        else:
            # Good packet, increment uptime
            uptime += 1
    if uptime - 1 == i:
        print('No outages detected over {0} seconds!'.format(uptime))


if __name__ == '__main__':
    parse()