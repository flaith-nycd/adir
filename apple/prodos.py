# -*- coding: utf-8 -*-
"""
See Beneath Apple ProDOS - 3.17
Table 3.1 ProDOS Block Conversion Table for Diskettes
To convert from DOS, see the bottom information:
DOS 3.3 SECTOR
For example, block 000, read track 0 sectors 0 & E
For example, block 017, read track 2 sectors 1 & f

The first block (block 0) is always devoted to the image of the
bootstrap loader. (Block 1 is the SOS bootstrap loader.) Following
these, and always starting at block 2, is the Volume Directory.
The Volume Directory is the "anchor" of the entire volume. On any
diskette (or hard disk for that matter) for any version of ProDOS,
the first or "key" block of the Volume Directory is always in the
same place-block 2.

                    PHYSICAL SECTOR
BLOCKS      0&2 4&6 8&A C&E 1&3 5&7 9&B D&F
-------------------------------------------
TRACK 0     000 001 002 003 004 005 006 007
TRACK 1     008 009 00A 00B 00C 00D 00E 00F
TRACK 2     010 011 012 013 014 015 016 017
TRACK 3     018 019 01A 01B 01C 01D 01E 01F
TRACK 4     020 021 022 023 024 025 026 027
TRACK 5     028 029 02A 02B 02C 02D 02E 02F
TRACK 6     030 031 032 033 034 035 036 037
TRACK 7     038 039 03A 03B 03C 03D 03E 03F
TRACK 8     040 041 042 043 044 045 046 047
TRACK 9     048 049 04A 04B 04C 04D 04E 04F
TRACK A     050 051 052 053 054 055 056 057
TRACK B     058 059 05A 05B 05C 05D 05E 05F
TRACK C     060 061 062 063 064 065 066 067
TRACK D     068 069 06A 06B 06C 06D 06E 06F
TRACK E     070 071 072 073 074 075 076 077
TRACK F     078 079 07A 07B 07C 070 07E 07F 
TRACK 10    080 081 082 083 084 085 086 087
TRACK 11    088 089 08A 08D 08C 08D 08E 08F
TRACK 12    090 091 092 093 094 095 096 097
TRACK 13    098 099 09A 09B 09C 09D 09E 09F
TRACK 14    0A0 0A1 0A2 0A3 0A4 0A5 0A6 0A7
TRACK 15    0A8 0A9 0AA 0AB 0AC 0AD 0AE 0AF
TRACK 16    0B0 0B1 0B2 0B3 0B4 0B5 0B6 0B7
TRACK 17    0B8 0B9 0BA 0BB 0BC 0BD 0BE 0BF
TRACK 18    0C0 0C1 0C2 0C3 0C4 0C5 0C6 0C7
TRACK 19    0C8 0C9 0CA 0CB 0CC 0CD 0CE 0CF
TRACK 1A    0D0 0D1 0D2 0D3 0D4 0D5 0D6 0D7
TRACK 1B    0D8 0D9 0DA 0DB 0DC 0DD 0DE 0DF
TRACK 1C    0E0 0E1 0E2 0E3 0E4 0E5 0E6 0E7
TRACK 1D    0E8 0E9 0EA 0EB 0EC 0ED 0EE 0EF
TRACK 1E    0F0 0F1 0F2 0F3 0F4 0F5 0F6 0F7
TRACK 1F    0F8 0F9 0FA 0FB 0FC 0FD 0FE 0FF
TRACK 20    100 101 102 103 104 105 106 107
TRACK 21    108 109 10A 10B 10C 10D 10E 10F
TRACK 22    110 111 112 113 114 115 116 117
-------------------------------------------
            0&E D&C B&A 9&8 7&6 5&4 3&2 1&F
        0 14 13 12 11 10 9 8 7 6 5 4 3 2 1 15
                    DOS 3.3 SECTOR
"""

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
