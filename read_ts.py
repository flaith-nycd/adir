#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Usage: python read_ts.py [FILENAME] [TRACK] [SECTOR] [SIZE]

Options:
    FILENAME:   Disk filename
    TRACK:      Which track (default = 17 - $11)        [optional]
    SECTOR:     Which sector (default = 0 - $00)        [optional]
    SIZE:       How many bytes to dump (default = 256)  [optional]

Examples:
  python read_ts.py adir_catalog.dsk
  python read_ts.py adir_catalog.dsk 17
  python read_ts.py adir_catalog.dsk 17 14
  python read_ts.py adir_catalog.dsk 17 14 512
"""
from sys import argv
from apple.dos import *
from apple.helpers import dump_dos

__author__ = 'Nicolas Djurovic'
__version__ = '0.7'


def dump_at_ts(params):
    if len(params) > 0:
        diskfile = params[0]
        # Inline if-else statement, works with all kind of iterables objects (list, dict, tuples, set)
        track = params[1] if params[1:] else 0x00
        # Can use None so we can read the whole track
        sector = params[2] if params[2:] else None  # 0x00
        byte_to_read = params[3] if params[3:] else None  # 256
    else:
        # print('Missing arguments')
        print(__doc__)
        exit()

    # Open our disk image
    dsk = DiskDos33(diskfile)

    # read at the selected track/sector
    value = dsk.read_ts(track, sector, byte_to_read)
    # Get the track and sector given by method 'read_ts'
    # to be able to print the result
    track = int(dsk.track)
    sector = int(dsk.sector)

    dump_dos(value, track, sector)


# If the code here is not imported then run
# The code within the 'if' block will be executed only when the code runs directly.
# Here 'directly' means 'not imported'
if __name__ == "__main__":
    dump_at_ts(argv[1:])
