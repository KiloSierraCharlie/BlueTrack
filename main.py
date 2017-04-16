#!/usr/bin/python
from bluetooth import lookup_name
from time import strftime, time, sleep
import sqlite3 as sql
from sys import exit
from json import dumps
import deviceHunter
from threading import Thread
configuration = [

  # Polling time (How often, in seconds, do you want to check who is around?)
  
  3,
  
  # Polling timeout (How long do you want the script to wait before declaring a device out-of-area?)
  
  3,
  
  #The node ID of this device (If you have multiple devices polling the same network of devices.)
  
  1,
  
]

try:

  Database = sql.connect('database.sqlite')
  
  Cursor = Database.cursor()
  
except sql.Error as Err:

  print( "Error connecting to the databse!" )
  
  print( Err )
  
  exit( 1 )

Hunter = deviceHunter.DeviceHunter()
newDeviceThread = Thread( target=Hunter.hunt )

newDeviceThread.daemon = True

newDeviceThread.start()

while True:

    try:
    
      Cursor.execute( "SELECT `macaddr`,`fname`,`lname`,`devicename` FROM `devices` WHERE 1;" )
      
      Devices = Cursor.fetchall()
      
      if( len( Devices ) == 0 ):
      
        print( "No devices found, waiting", configuration[ 0 ], "seconds before trying again!" )
        
      else:
      
        for device in Devices:

          if( not lookup_name( device[ 0 ], timeout=configuration[ 1 ] ) == None ):

            try:
              
              jsonLog = dumps( [ time(), configuration[ 2 ] ] )             

              Cursor.execute( "UPDATE `devices` SET `lastseen`=? WHERE `macaddr`=?;", ( jsonLog, device[ 0 ], ) )
              
              Cursor.execute( "INSERT into `seenlog` ( `time`, `macaddr`, `nodeid` ) VALUES ( ?, ?, ? );", ( time(), device[ 0 ], configuration[ 2 ], ) )

              Database.commit()

              if( device[2][-1] == "s" ):

                  print( "%s %s' %s (%s) is in the local area!" % ( device[ 1 ], device[ 2 ], device[ 3 ], device[ 0 ] ) )

              else:

                  print( "%s %s's %s (%s) is in the local area!" % ( device[ 1 ], device[ 2 ], device[ 3 ], device[ 0 ] ) )

            except sql.Error as Err:
            
              print( "There was an error updating the device information!" )
              
              print( Err )
          
    except sql.Error as Err:
    
      print( "Error getting devices!" )
      
      print( Err )
      
      exit( 1 )

    sleep( configuration[ 0 ] )
