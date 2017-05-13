# Apple Disk Image Reader
For now you can get the CATALOG of DOS disk

```
python catalog.py adir_catalog.dsk
```
Result:
```
DISK VOLUME 254

 A 002 HELLO
 A 002 ADIR-CATALOG
 A 002 BY
 A 002 NICOLAS DJUROVIC

Sectors free: 552
```

```
python catalog.py Merlin-8-2.48.dsk                           
```
Result:
```
DISK VOLUME 254                                                 
                                                                
 A 004 HELLO                                                    
 B 004 MERLIN                                                   
 B 017 ASM.1                                                    
 B 042 ASM.2                                                    
 B 015 ED.16                                                    
 B 015 ED                                                       
 B 008 XREF                                                     
 B 005 FORMATTER                                                
 B 008 XREF A                                                   
 B 025 KEYMAC.S                                                 
 B 004 KEYMAC                                                   
 T 008 T.MACRO LIBRARY                                          
 T 002 T.SENDMSG                                                
 T 005 T.FPMACROS                                               
 B 003 MON.65C02                                                
 B 018 SOURCEROR                                                
 B 010 LABELS.S                                                 
 B 006 LABELS                                                   
 B 019 PRINTFILER.S                                             
 B 003 PRINTFILER                                               
 B 014 PI.START.S                                               
 B 013 PI.MAIN.S                                                
 B 005 PI.LOOK.S                                                
 B 015 PI.DIV.S                                                 
 B 009 PI.ADD.S                                                 
 T 006 T.PI.MACS                                                
 B 004 PI.START                                                 
 B 003 PI.MAIN                                                  
 B 002 PI.LOOK                                                  
 B 003 PI.DIV                                                   
 B 003 PI.ADD                                                   
 B 007 APPLE PI                                                 
 T 002 PI.NAMES                                                 
 T 006 T.ROCKWELL MACROS                                        
 T 005 T.PRDEC                                                  
 T 004 T.OUTPUT                                                 
 B 025 CLOCK.S                                                  
 B 003 CLOCK.12                                                 
 B 003 CLOCK.24                                                 
 B 028 MAKE DUMP.S                                              
 B 004 MAKE DUMP                                                
 B 004 MERLIN.X                                                 
 B 005 MERLIN.CORVUS                                            
 B 004 MERLIN.CORVUS.X                                          
 B 020 EDMAC.S                                                  
 B 004 EDMAC                                                    
 A 002 SENDMSG.TEST.FP                                          
 T 005 SENDMSG.TEST.S                                           
 B 002 SENDMSG.TEST                                             
 A 004 MULTIPLY/DIVIDE DEMO                                     
 B 012 M/D RTNS FOR BASIC.S                                     
 B 002 M/D.OBJ                                                  
                                                                
Sectors free: 111                                               
```
