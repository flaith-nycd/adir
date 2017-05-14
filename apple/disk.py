# -*- coding: utf-8 -*-
"""
Apple II Disk Image Reader

- Class Disk is the main class
- DiskBin: child class for disk without a VTOC and only used to read Track/Sector
- DiskDoss33: child class for Dos disk with a catalog 

TODO: - PRODOS
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

      - NIB format (http://boutillon.free.fr/Underground/Cours/Nibbles/Nibbles.html)
        Le .NIB permet de gérer ces disquettes au format non standardisé.

        Le .DSK est rangé bien proprement. Les secteurs se suivent dans l'ordre et tout est pour le mieux dans 
        le meilleur des mondes.
        Dans la pratique, sur un vrai Apple II, quand la tête de lecture commence à lire une piste concentrique, 
        elle peut tomber n'importe où. Par exemple sur le secteur $0D.
        De la même façon, le format .NIB n'impose pas d'ordre des secteurs.
        
        Il se contente en effet de définir pour chaque piste une taille identique de 6656 octets, soit $1A00 en hexa.
        Après on met ce qu'on veut dans chacun de ces espaces représentant une piste.
        
        Le .NIB est donc une succession d'espaces fixes de 6656 octets de long. Cette définition de taille fixe sert 
        surtout à ne pas rendre trop compliquée l'exploitation du .NIB en l'organisant un minimum (découpage piste).
        Comme un .NIB contient lui aussi 35 pistes et a donc 35*6656 = 232960 octets, soit une taille de 62,5% plus 
        importante que le .DSK.
        Note: si un jour vous rencontrez un .NIB de 266240 octets, il s'agit d'une image de 40 pistes.
        
        // Taille d'une piste du .nib
        static int TRACK_SIZE = 0x1a00;
        // Nombre de nibbles correspondant à 1 secteur complet du .dsk
        static int SECTOR_SIZE = 409;
"""
from array import array
import sys
import os

__author__ = 'Nicolas Djurovic'
__version__ = '0.14'


class DiskfileError(Exception):
    """Exception constructor"""

    def __init__(self, diskfile, message):
        self._diskfile = diskfile
        self._message = message

    # Will be used when an exception will occur
    def __str__(self):
        return "The disk file \"{}\" {} !".format(self._diskfile, self._message)


class Disk:
    # Disk File System Format
    __FS_UNKNOW = 0
    __FS_SEQUENTIAL = 1  # 256 bytes sector
    __FS_NIBBLE_6656 = 2  # 6656 bytes/track
    __FS_NIBBLE_6384 = 3  # 6384 bytes/track

    # Disk System Type
    __DSK_UNKNOW = 0
    __DSK_DOS = 1
    __DSK_PRODOS = 2
    __DSK_PASCAL = 3

    def __init__(self, diskname):
        # From sys, put this flag to remove Traceback display
        sys.tracebacklimit = None

        # Keep the name of our disk
        self._diskname = diskname

        # What kind of disk we're opening?
        self._dsk_format = self.__DSK_UNKNOW

        # and init its size to 0
        self._disksize_raw = 0

        # Init memory for the disk
        # the size will be given by the disk size
        self.memdisk = array('B')

        # Set a default track/sector, so we can return the values
        self.track = 0x00
        self.sector = 0x00

        # Number of tracks (usually 35)
        self._total_tracks = 35

        # Default sector size
        self._sector_size = 256

        # Default total sector per track
        self._sector_per_track = 16

        # Load our disk in memory and
        # check the disk format:
        # DOS, PRODOS, APPLE, ...
        self._load()

    # Return the real size of the file
    # to be used with the _load method
    def _get_file_size(self):
        try:
            return os.stat(self._diskname).st_size
        except:
            raise DiskfileError(self._diskname, 'not found !')

    # Load the disk file in the array
    def _load(self):
        with open(self._diskname, 'rb') as diskfile:
            # memdisk is an array, so we use array method 'fromfile'
            # to load and populate our array with the real size
            # of the file
            self._disksize_raw = self._get_file_size()
            self.memdisk.fromfile(diskfile, self._disksize_raw)

    # Get part of the memory corresponding of the
    # track/sector and how many byte to read
    def read_ts(self, track=0, sector=0, byte_to_read=None):
        result = []

        if byte_to_read is None:
            byte_to_read = self._sector_size

        # If there is no sector number
        # we're reading the whole track
        if sector is None:
            sector = 0  # But we need to give a number for the position
            byte_to_read = self._sector_size * self._sector_per_track

        position = (int(track) * self._sector_size * self._sector_per_track) + \
                   (int(sector) * self._sector_size)
        self.track = track
        self.sector = sector

        if position < self._disksize_raw:
            result = self.memdisk[position:position + int(byte_to_read)]
            return result

    # Convert byte to ascii
    # we don't use the object itself at all, so declare it as static
    @staticmethod
    def byte2ascii(data):
        result = []
        for char in data:
            if char in range(32, 128):  # Check from ascii code $20 to $7E
                result.append(chr(char))
            elif char in range(160, 255):  # if between $A0 to $FE
                result.append(chr(char - 128))  # Substract $80 to go back between $20 to $7E
            else:
                result.append('.')
        return result


class DiskBin(Disk):
    def __init__(self, diskname):
        # Init with the mother class
        Disk.__init__(self, diskname)
