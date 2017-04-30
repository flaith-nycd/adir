# Apple Disk Image Reader : CATALOG
Apple Disk Image Reader, get the CATALOG of DOS disk

```
python catalog.py adir_catalog.dsk
```
Result:
```
--- CATALOG OF adir_catalog.dsk ...
HELLO                            2 T:$13 S:0F TYPE:2
ADIR-CATALOG                     2 T:$14 S:0F TYPE:2
BY                               2 T:$15 S:0F TYPE:2
NICOLAS DJUROVIC                 2 T:$16 S:0F TYPE:2
--- Sectors Used: 8 (1%) --- Free: 552 ---
```

Show you the filename, its size, the first track/sector where starts the filename in the disk
and the type:
```
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
```
