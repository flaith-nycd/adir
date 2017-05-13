# Apple Disk Image Reader
For now you can get the CATALOG of DOS disk

## ADDED to the CATALOG, the first track and sector list of the file
```
python catalog.py adir_catalog.dsk
```
Result:
```
DISK VOLUME 254

 A 002 HELLO                           [$13:$0F]
 A 002 ADIR-CATALOG                    [$14:$0F]
 A 002 BY                              [$15:$0F]
 A 002 NICOLAS DJUROVIC                [$16:$0F]

Sectors free: 552
```

```
python catalog.py Merlin-8-2.48.dsk                           
```
Result:
```
DISK VOLUME 254

 A 004 HELLO                           [$13:$0F]
 B 004 MERLIN                          [$19:$0B]
 B 017 ASM.1                           [$1B:$0F]
 B 042 ASM.2                           [$1F:$0F]
 B 015 ED.16                           [$1C:$0F]
 B 015 ED                              [$05:$0F]
 B 008 XREF                            [$20:$02]
 B 005 FORMATTER                       [$1A:$0F]
 B 008 XREF A                          [$0B:$09]
 B 025 KEYMAC.S                        [$06:$0F]
 B 004 KEYMAC                          [$19:$0F]
 T 008 T.MACRO LIBRARY                 [$03:$0F]
 T 002 T.SENDMSG                       [$15:$03]
 T 005 T.FPMACROS                      [$20:$0F]
 B 003 MON.65C02                       [$21:$0F]
 B 018 SOURCEROR                       [$14:$0F]
 B 010 LABELS.S                        [$10:$0F]
 B 006 LABELS                          [$0F:$0F]
 B 019 PRINTFILER.S                    [$0E:$0B]
 B 003 PRINTFILER                      [$12:$0F]
 B 014 PI.START.S                      [$13:$0B]
 B 013 PI.MAIN.S                       [$14:$0C]
 B 005 PI.LOOK.S                       [$19:$07]
 B 015 PI.DIV.S                        [$1A:$0A]
 B 009 PI.ADD.S                        [$1B:$08]
 T 006 T.PI.MACS                       [$1D:$0B]
 B 004 PI.START                        [$1E:$07]
 B 003 PI.MAIN                         [$1F:$0D]
 B 002 PI.LOOK                         [$20:$0A]
 B 003 PI.DIV                          [$21:$0C]
 B 003 PI.ADD                          [$10:$03]
 B 007 APPLE PI                        [$12:$0C]
 T 002 PI.NAMES                        [$19:$02]
 T 006 T.ROCKWELL MACROS               [$1D:$05]
 T 005 T.PRDEC                         [$21:$07]
 T 004 T.OUTPUT                        [$21:$02]
 B 025 CLOCK.S                         [$08:$0E]
 B 003 CLOCK.12                        [$07:$0D]
 B 003 CLOCK.24                        [$0B:$0F]
 B 028 MAKE DUMP.S                     [$0E:$0E]
 B 004 MAKE DUMP                       [$0A:$03]
 B 004 MERLIN.X                        [$03:$07]
 B 005 MERLIN.CORVUS                   [$12:$05]
 B 004 MERLIN.CORVUS.X                 [$16:$0E]
 B 020 EDMAC.S                         [$21:$09]
 B 004 EDMAC                           [$0A:$0F]
 A 002 SENDMSG.TEST.FP                 [$1F:$0A]
 T 005 SENDMSG.TEST.S                  [$18:$04]
 B 002 SENDMSG.TEST                    [$1F:$03]
 A 004 MULTIPLY/DIVIDE DEMO            [$1F:$01]
 B 012 M/D RTNS FOR BASIC.S            [$20:$06]
 B 002 M/D.OBJ                         [$0A:$04]

Sectors free: 111                                            
```
