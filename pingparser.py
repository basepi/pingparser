'''
Parse through the contents of a file generated with this command:

    ping 8.8.8.8 | while read pong; do echo "$(date): $pong"; done > monitor.txt

Output a list of outages based on ping timeouts. Give start and end timestamps,
plus total time offline.

Note: Reads in the whole file, so make sure it's not too big.

You can also pass in a number after the filename, and the script will ignore
downtime if it's fewer than that number of packets.

For example:

    python3 pingparser.py ~/monitor.txt 2

The above command will only show downtime if it's at least two packets long.
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

    down_threshold = 1
    if len(sys.argv) > 2:
        down_threshold = int(sys.argv[2])

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
            if count < down_threshold:
                uptime += 1
            else:
                mins = uptime // 60
                uptime = uptime % 60
                hours = mins // 60
                mins = mins % 60
                dmins = count // 60
                dsecs = count % 60
                print('Down for {0:02d}:{1:02d} at {2} after {3:02d}:{4:02d}:{5:02d} uptime'
                      .format(dmins, dsecs, downtime, hours, mins, uptime))
                uptime = 0
                skipto = i + count
        else:
            # Good packet, increment uptime
            uptime += 1
    if uptime - 1 == i:
        mins = i // 60
        i = i % 60
        hours = mins // 60
        mins = mins % 60
        days = hours // 24
        hours = hours % 24
        print('No outages over {0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(days, hours, mins, i))
    else:
        mins = uptime // 60
        uptime = uptime % 60
        hours = mins // 60
        mins = mins % 60
        print('Ended with {0:02d}:{1:02d}:{2:02d} uptime.'.format(hours, mins, uptime))
        mins = i // 60
        i = i % 60
        hours = mins // 60
        mins = mins % 60
        days = hours // 24
        hours = hours % 24
        print('Total time: {0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(days, hours, mins, i))


if __name__ == '__main__':
    parse()
