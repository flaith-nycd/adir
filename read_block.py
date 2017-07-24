#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Usage: python read_block.py [FILENAME] [BLOCK]

Options:
    FILENAME:   Disk filename
    BLOCK:      Which block (default = 00)        [optional]

Examples:
  python read_block.py adir_prodos.dsk
  python read_block.py adir_prodos.dsk 2
"""
from sys import argv
from apple.prodos import *
from apple.helpers import dump_prodos

__author__ = 'Nicolas Djurovic'
__version__ = '0.7'


def dump_at_block(params):
    if len(params) > 0:
        diskfile = params[0]
        block = params[1] if params[1:] else 0x00
    else:
        print(__doc__)
        exit()

    # Open our disk image
    dsk_prodos = DiskProdos(diskfile)

    # Need to convert to an integer
    # before reading
    block = int(block)

    # Read our block to dump
    value = dsk_prodos.read_block(block)

    # Use the function from the module dump_format
    dump_prodos(value, block)


# If the code here is not imported then run
# The code within the 'if' block will be executed only when the code runs directly.
# Here 'directly' means 'not imported'
if __name__ == "__main__":
    dump_at_block(argv[1:])
