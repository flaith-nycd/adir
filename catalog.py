#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from apple.disk import *
from sys import argv, exit


def show_catalog(diskfile):
    if not diskfile:
        print('Cannot execute without a disk filename !!!')
        exit()

    print('--- CATALOG OF {} ...'.format(diskfile))
    dsk = DiskDos33(diskfile)
    # dsk = DiskDos33('adir_nycd.dsk')
    # dsk = DiskDos33('dsk/nycd_sf.dsk')
    # dsk = DiskDos33('ll_6502.dsk')
    # dsk = DiskDos33('tb_6502.dsk')
    dsk.catalog()

if __name__ == "__main__":
    file = "".join(argv[1:])
    show_catalog(file)
