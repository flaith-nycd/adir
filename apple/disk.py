# -*- coding: utf-8 -*-
"""
Apple II Disk Image Reader

- Class Disk is the main class
- DiskBin: child class for disk without a VTOC and only used to read Track/Sector
- DiskDoss33: child class for Dos disk with a catalog 
- DiskProdos: child class for ProDOS disk

    TODO:
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
