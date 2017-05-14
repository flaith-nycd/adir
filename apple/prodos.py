# -*- coding: utf-8 -*-
# For the import method:
# https://www.python.org/dev/peps/pep-0008/#imports
from apple.disk import Disk, DiskfileError

__author__ = 'Nicolas Djurovic'
__version__ = '0.8'


class DiskProdos(Disk):
    __BLOCK_PER_TRACK = 8
    __MAX_TRACK = 280
    __SECTOR_SIZE = 256
    __BLOCK_SIZE = 512

    __BLOCK_SECTOR = [
        (0x00, 0x0E),
        (0x0D, 0x0C),
        (0x0B, 0x0A),
        (0x09, 0x08),
        (0x07, 0x06),
        (0x05, 0x04),
        (0x03, 0x02),
        (0x01, 0x0F)
    ]

    def __init__(self, diskname):
        # Init with the mother class
        Disk.__init__(self, diskname)
        # And check if the current disk image is a valid ProDOS disk
        if not self.check_disk_format():
            raise DiskfileError(diskname, 'is not a valid ProDOS disk')

    def convert_block_to_ts(self, block):
        # Convert the block number to a track number and 2 sectors

        # Block is from 0 to __MAX_TRACK?
        if block in range(0, self.__MAX_TRACK):
            # Block OK, now find the track
            # 1 Track = 8 blocks
            track = block // self.__BLOCK_PER_TRACK

            # Get the index from the __BLOCK_SECTOR to get the sectors
            index = block % self.__BLOCK_PER_TRACK

            return track, self.__BLOCK_SECTOR[index][0], self.__BLOCK_SECTOR[index][1]
        else:
            print('BlockError: Block', block, 'is not available (maximum=279)')
            exit()

    def read_block(self, block):
        # Read the block by using the convert block method
        track, sector1, sector2 = self.convert_block_to_ts(block)

        # Now read 2 times with read_ts method from main class Disk
        value_high = self.read_ts(track, sector1, self.__SECTOR_SIZE)
        value_low = self.read_ts(track, sector2, self.__SECTOR_SIZE)

        return value_high + value_low

    def check_disk_format(self):
        # Check if the loaded disk image is ProDOS

        # We need to read the block #2
        block_buffer = self.read_block(2)

        # $23 ENTRY_LENGTH: Length of each entry in the Volume Directory
        # in bytes (usually $27).
        entry_length = block_buffer[0x23]
        # $24 ENTRIES_PER_BLOCK: Number of entries in each block of the
        # Volume Directory (usually $OD). Note that the Volume Directory Header
        # is considered to be an entry.
        entries_per_block = block_buffer[0x24]

        # Part of the code used from Andy McFadden's CiderPress
        # ProDOS.cpp line 69, method TestImage
        # and Beneath Apple ProDOS p.26 - 4.9
        if (not (block_buffer[0x00] == 0 and block_buffer[0x01] == 0) or
                not ((block_buffer[0x04] & 0xf0) == 0xf0) or
                not ((block_buffer[0x04] & 0x0f) != 0) or
                not (entry_length * entries_per_block <= self.__BLOCK_SIZE) or
                not (ord('A') <= block_buffer[0x05] <= ord('Z')) or
                0):
            return False
        else:
            return True
