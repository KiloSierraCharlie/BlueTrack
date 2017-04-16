# Adapted from https://github.com/karulis/pybluez/blob/master/examples/simple/asynchronous-inquiry.py
#!/usr/bin/python
import sqlite3 as sql
import bluetooth

class DeviceHunter( bluetooth.DeviceDiscoverer ):
    
    def setDBDetails( self ):

        database = sql.connect('database.sqlite')
  
        cursor = database.cursor()

        self.__database = database
        self.__cursor = cursor

    def pre_inquiry( self ):
        self.done = False
    
    def device_discovered( self, macAddr, device_class, rssi, devName ):        
        major_classes = ( "Miscellaneous", 
                          "Computer", 
                          "Phone", 
                          "LAN/Network Access point", 
                          "Audio/Video", 
                          "Peripheral", 
                          "Imaging" )
        major_class = (device_class >> 8) & 0xf
        if major_class < 7:
            devClass = major_classes[major_class]
        else:
            devClass = "Uncategorized"

        self.handleUnknown( macAddr, devName, devClass )

    def inquiry_complete(self):
        self.done = True

    def handleUnknown( self, macAddr, devName="", devClass="Uncategorized" ):
        try:
            self.__cursor
            self.__database
        except AttributeError:
            self.setDBDetails()

        try:
            
            self.__cursor.execute( "SELECT `fname`, `lname`, `devicename`, `devicetype` FROM `devices` WHERE `macaddr`=?;", ( macAddr, ) )
           
            Device = self.__cursor.fetchone()
        
        except sql.Error as Err:
        
            print( "Something went wrong whilst checking a new device!" )
        
            print( Err )

        if( Device == None ):

            try:

                if( devName == None ):

                    self.__cursor.execute( "INSERT into `devices` ( `fname`, `lname`, `macaddr`, `devicetype` ) VALUES ( 'Someone', 'Unregistered', ?, ? );", ( macAddr, devClass, ) )

                else:

                    self.__cursor.execute( "INSERT into `devices` ( `fname`, `lname`, `devicename`, `devicetype`, `macaddr` ) VALUES ( 'Someone', 'Unregistered', ?, ?, ? );", ( devName, devClass, macAddr, ) )

                self.__database.commit()

            except sql.Error as Err:

                print( "There was an error inserting a new device to the system!" )

                print( Err )

        else:

            if( not Device[ 2 ] == devName ):

                self.__cursor.execute( "UPDATE `devices` SET `devicename`=? WHERE `macaddr`=?;", ( devName, macAddr, ) )

                self.__database.commit()

            if( not Device[ 3 ] == devClass ):

                self.__cursor.execute( "UPDATE `devices` SET `devicetype`=? WHERE `macaddr`=?;", ( devClass, macAddr, ) )

                self.__database.commit()

    def hunt( self ):
        self.find_devices( lookup_names = True )
        while True:
            self.process_event()
            if( self.done ): self.find_devices( lookup_names = True )
