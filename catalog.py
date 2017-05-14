#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv, exit
from apple.dos import *

__author__ = 'Nicolas Djurovic'
__version__ = '0.7'


def show_catalog(diskfile):
    if not diskfile:
        print('Cannot execute without a disk filename !!!')
        exit()

    # Load our diskfile
    dsk = DiskDos33(diskfile)
    # Display our Dos33 catalog
    dsk.catalog()

if __name__ == "__main__":
    # 'join' our arguments to avoid:
    # TypeError: expected str, bytes or os.PathLike object, not list
    file = "".join(argv[1:])
    show_catalog(file)
