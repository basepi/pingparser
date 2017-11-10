# pingparser

Simple tool for parsing a long-running ping process, showing outages

## Usage

Let ping run for awhile collecting data:

```
ping 8.8.8.8 | while read pong; do echo "$(date): $pong"; done > monitor.txt
```

Then analyze:

```
wget https://raw.githubusercontent.com/basepi/pingparser/master/pingparser.py
python3 pingparser.py monitor.txt
```

The script is python2/3 compatible.

This assumes your ping lines look like this:

```
Fri Nov 10 15:34:57 MST 2017: 64 bytes from 8.8.8.8: icmp_seq=1581 ttl=53 time=21.737 ms
Fri Nov 10 15:34:58 MST 2017: 64 bytes from 8.8.8.8: icmp_seq=1582 ttl=53 time=21.856 ms
Fri Nov 10 15:34:59 MST 2017: 64 bytes from 8.8.8.8: icmp_seq=1583 ttl=53 time=21.924 ms
Fri Nov 10 15:35:00 MST 2017: 64 bytes from 8.8.8.8: icmp_seq=1584 ttl=53 time=21.880 ms
Fri Nov 10 15:35:01 MST 2017: 64 bytes from 8.8.8.8: icmp_seq=1585 ttl=53 time=21.812 ms
Fri Nov 10 15:35:02 MST 2017: 64 bytes from 8.8.8.8: icmp_seq=1586 ttl=53 time=25.291 ms
Fri Nov 10 15:35:03 MST 2017: 64 bytes from 8.8.8.8: icmp_seq=1587 ttl=53 time=22.738 ms
Fri Nov 10 15:35:04 MST 2017: 64 bytes from 8.8.8.8: icmp_seq=1588 ttl=53 time=22.240 ms
```

Specifically, it assumes the output of `date` is 28 characters long. If it's
shorter, it should be fine, but it may cut off the end of the date, or have
some garbage output.

It also is hardcoded to assume the ping interval is one second.
