"""
Apple II Disk Image Reader
Read CATALOG of a dsk

* Catalog Sector Format
00    - Not used
01    - Track number of next catalog sector (usually $11)
02    - Sector number of next catalog sector
03-0A - Not used
0B-2D - First File Description Entry
2E-50 - Second File Description Entry
51-73 - Third File Description Entry
74-96 - Fourth File Description Entry
97-B9 - Fifth File Description Entry
BA-DC - Sixth File Description Entry
DD-FF - Seventh File Description Entry

* File Descriptive Entry format
00    - Track of first track/sector list sector
        if this is a deleted file, the byte contains a hex
        $FF and the original track number is copied to the
        last byte of the file name field (Byte $20)
        If this byte contains a hex $00, the entry is assumed
        to never have been used and is available for use.
        (This means track $00 can never be used for data even
        if the DOS image is "wiped" from the diskette.)
01    - Sector of first track/sector list sector
02    - File Type and Flag :
            hex 80 + file type  -> file is locked
                00 + file type  -> file is not locked
                00 -> TEXT file
                01 -> INTEGER BASIC file
                02 -> APPLESOFT BASIC file
                04 -> BINARY file
                08 -> S type file
                10 -> RELOCATABLE object module file
                20 -> A type file
                40 -> B type file
            (thus, 84 is a locked BINARY file , and 90 is a
            locked R type file)
03-20 - File name (30 characters)
21-22 - Length of file in sectors (LO/HI format).
        The CATALOG command will only format the LO byte of
        this length giving 1-255 but a full 65535 may be
        stored here.
"""
from array import array
import os

__author__ = 'Nicolas Djurovic'
__version__ = '0.6'


class DiskfileError(Exception):
    """Exception constructor"""

    def __init__(self, diskfile, message):
        self._diskfile = diskfile
        self._message = message

    # Will be used when an exception will occur
    def __str__(self):
        return "The disk file \"{}\" {} !".format(self._diskfile, self._message)


class DiskDos33:
    """Specified class for a DOS disk """

    # Create a dictionnary for the VTOC
    _vtoc = {}

    # Usual values used to read the VTOC
    _vtoc_track = 0x11
    _vtoc_sector = 0x00
    _vtoc_sector_size = 256
    _vtoc_total_sectors = 16

    def __init__(self, diskname):
        # Keep the name of our disk
        self._diskname = diskname

        # and init its size to 0
        self._disksize_raw = 0

        # Init memory for the disk
        # the size will be given by the disk size
        self._memdisk = array('B')

        # Load our disk in memory
        self._load()

        # To get our catalog, we will need to read the VTOC
        self._read_vtoc()

        # Our first Track/Sector of our catalog:
        self._first_catalog_track = self._vtoc['first_catalog_track']
        self._first_catalog_sector = self._vtoc['first_catalog_sector']

        # Number of tracks (usually 35)
        self._total_tracks = self._vtoc['total_tracks']
        # Number of sector per track (13 or 16)
        self._sector_per_track = self._vtoc['sector_per_track']
        # Size of one sector in byte
        self._sector_size = self._vtoc['sector_size']

        # Total should be 143360 bytes
        self._disksize = self._total_tracks * self._sector_per_track * self._sector_size

        # Check if the real (_disksize_raw) size of the file
        # is equal to the computed size (_disksize) returned from the VTOC
        if self._disksize_raw != self._disksize:
            raise DiskfileError(self._diskname, 'is not a valid disk, the size is {}'.format(self._disksize_raw))

    # Return the real size of the file
    # to be used with the _load method
    def _get_file_size(self):
        try:
            return os.stat(self._diskname).st_size
        except:
            raise DiskfileError(self._diskname, 'not found')

    # Load the disk file in the array
    def _load(self):
        with open(self._diskname, 'rb') as diskfile:
            # _memdisk is an array, so we use array method 'fromfile'
            # to load and populate our array with the real size
            # of the file
            self._disksize_raw = self._get_file_size()
            self._memdisk.fromfile(diskfile, self._disksize_raw)

    # This property is not used in the progra,m it's just here to see how to use array
    #
    # buffer_info() return a tuple (address, length) giving the current memory address and the length in elements of the
    # buffer used to hold array’s contents. The size of the memory buffer in bytes can be computed as
    # array.buffer_info()[1] * array.itemsize.
    #
    # This is occasionally useful when working with low-level (and inherently unsafe) I/O interfaces that require
    # memory addresses, such as certain ioctl() operations.
    # The returned numbers are valid as long as the array exists and no length-changing operations are applied to it.
    #
    # ex: print('Buffer info :', dsk.memdisk.buffer_info())
    @property
    def memsize(self):
        return self._memdisk.buffer_info()[1] * self._memdisk.itemsize

    # Convert byte to ascii
    # we don't use the object itself at all, so declare it as static
    @staticmethod
    def _byte2ascii(data):
        result = []
        for char in data:
            if char in range(32, 128):  # Check from ascii code $20 to $7E
                result.append(chr(char))
            elif char in range(160, 255):  # if between $A0 to $FE
                result.append(chr(char - 128))  # Substract $80 to go back between $20 to $7E
            else:
                result.append('.')
        return result

    # Get part of the memory corresponding of the
    # track/sector and how many byte to read
    def _read_ts(self, track=0, sector=0, byte_to_read=None):
        result = []

        if byte_to_read is None:
            byte_to_read = self._sector_size

        position = (track * self._sector_size * self._sector_per_track) + (sector * self._sector_size)

        if position < self._disksize:
            result = self._memdisk[position:position + byte_to_read]  # .tolist()
        return result

    def _read_vtoc(self):
        # Reading the VTOC will give us:
        # - First catalog track (first_catalog_track) byte $01
        # - First catalog sector (first_catalog_sector) byte $02
        # - Release number of DOS used to init this diskette (dos_release) byte $03
        # - Diskette volume number from 1 to 254 (disk_volume) byte $04
        # - Number of tracks per diskette, normally 35 => (total_tracks) byte $34
        # - Number of sectors per track, normally 16 => (sector_per_track) byte $35
        # - Number of byte per sector => (sector_size) byte $36-$37 (LO/HI)
        try:
            # Our first try to read track _vtoc_track and sector _vtoc_sector_size
            # we don't use the read_ts method because we don't know
            # yet all the info we need to read tracks and sectors
            # So we're using usual values
            position = (self._vtoc_track * self._vtoc_sector_size * self._vtoc_total_sectors) + \
                       (self._vtoc_sector * self._vtoc_sector_size)
            cat_vtoc = self._memdisk[position:position + self._vtoc_sector_size]

            self._vtoc['first_catalog_track'] = cat_vtoc[0x01]
            self._vtoc['first_catalog_sector'] = cat_vtoc[0x02]
            self._vtoc['dos_release'] = cat_vtoc[0x03]
            self._vtoc['disk_volume'] = cat_vtoc[0x04]
            self._vtoc['total_tracks'] = cat_vtoc[0x34]
            self._vtoc['sector_per_track'] = cat_vtoc[0x35]
            # Get LOW byte of the sector size
            sector_low = cat_vtoc[0x36]
            # and the HIGH byte
            sector_high = cat_vtoc[0x37]
            # Convert to one value
            sector = (sector_high << 8) + sector_low
            self._vtoc['sector_size'] = sector
        except:
            raise DiskfileError(self._diskname, 'cannot read VTOC, not a DOS disk !!!')

    def catalog(self):
        """
            00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
            -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        00: 00 11 07 00 00 00 00 00 00 00 00 FF 0B 02 D0 C9  ..............PI
        10: D8 DF D6 B2 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0  X_V2            
        20: A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 02 00 FF 09              ....
        30: 04 D3 C8 C5 D2 D7 CF CF C4 A0 A0 A0 A0 A0 A0 A0  .SHERWOOD       
        40: A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 21                 !
        50: 00 0C 09 04 CC CF C7 CF A0 A0 A0 A0 A0 A0 A0 A0  ....LOGO        
        60: A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0                  
                        +------- $FF, file is deleted
                        !        get the 29th byte to get
                        !        where was the previous
                        v        track (here it's [1D])
        70: A0 A0 21 00 FF 0C 04 D6 C9 C5 D7 AE D3 C5 C3 D4    !....VIEW.SECT
        80: CF D2 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0 A0  OR              
        90: A0 A0 A0 A0[1D]03 00 00 00 00 00 00 00 00 00 00      ............
        A0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
        B0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
        C0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
        D0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
        E0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
        F0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
        """

        # Get the first track and sector of our catalog
        next_track = self._first_catalog_track
        next_sector = self._first_catalog_sector

        # Create a new dictionnary of all the programs
        dict_program = {}
        dict_index = 0

        # Set total size of the programs
        total_used_sector = 0

        # Each filename has a length of 30 characters
        size_of_file = 0x23

        # Get the filenames from each sector and set the next sector
        while next_sector != 0x00:
            # Get a list from read_ts method
            cat_sector = self._read_ts(next_track, next_sector)

            # we only need the next sector, but maybe the track has been changed
            next_track = cat_sector[1]
            next_sector = cat_sector[2]

            # There is 7 programs listed in each sectors
            for index_file in range(7):
                # Extract each part where are the filenames
                # We start at offset $0B for the first
                # and we add the size of each filename
                index = 0x0B + (index_file * size_of_file)
                # Get info from File Descriptive Entry
                fde = cat_sector[index:index + size_of_file + 1]  # .tolist()

                # Get info about the file
                track_file = fde[0x00]
                sector_file = fde[0x01]
                type_file = fde[0x02]

                # Extract the filename
                filename = fde[0x03:0x21]

                # and its length
                file_length_low = fde[0x21]
                file_length_high = fde[0x22]
                file_length = (file_length_high << 8) + file_length_low

                # Add the size to the total size if the file is not deleted
                if track_file != 0xFF:
                    total_used_sector += file_length
                else:
                    # If it's a deleted file, change the byte
                    # at the 29th position to a space
                    filename[29] = 0xA0  # $A0 = 160 (128 + 32)

                # Generated the filename as a string from the list
                # Convert to ascii, join the list to a string and strip it
                fname = ''.join(self._byte2ascii(filename)).strip()

                # Add the infos extracted to our dictionnary
                dict_program[dict_index] = [fname, file_length, track_file, sector_file, type_file]

                # Increment our dictionnary index
                dict_index += 1

        # Read the ITEMS of the dictionnary to display the catalog
        for program in dict_program.items():
            # DON'T USE program[0], it's the index
            fname = program[1][0]
            file_length = program[1][1]
            track_file = program[1][2]
            sector_file = program[1][3]
            type_file = program[1][4]

            # if file_length <> 0, show catalog
            if file_length != 0:
                # If Track of the current file is equal to $FF
                if track_file == 0xFF:  # File is deleted
                    print('{:30} [deleted]'.format(fname))
                else:
                    print('{:30} {:3d} T:${:02X} S:{:02X} TYPE:{}'.format(
                        fname, file_length, track_file, sector_file, type_file
                    ))

        total_sectors = self._total_tracks * self._sector_per_track
        total_free_sector = total_sectors - total_used_sector
        # print('Total used:', total_used_sector)
        # print('Total free:', total_free_sector)
        percent = (total_used_sector / total_sectors) * 100
        # print('{}% used'.format(percent))
        print('--- Sectors Used: {} ({:.0f}%) --- Free: {} ---'.format(total_used_sector, percent, total_free_sector))
