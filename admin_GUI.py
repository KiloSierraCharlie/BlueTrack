#!/usr/bin/python
from tkinter import *
import sqlite3 as sql
from sys import exit
from time import strftime, localtime

deviceList = []

try:
    Database = sql.connect('database.sqlite') 
    Cursor = Database.cursor()

except sql.Error as Err:
    print( "Error connecting to the databse!" )
    print( Err )
    exit( 1 )


def inputDeviceList():
    global deviceList
    deviceListBox.delete(0,END)
    Cursor.execute("SELECT * FROM `devices` WHERE 1;")
    deviceList = Cursor.fetchall()
    if( len( deviceList ) == 0 ):
        messagebox.showinfo("No Devices!", "There are no devices on the system!\nLoad up your device in range of your system, and make it discover-able!")
    for device in deviceList:
        deviceListBox.insert( END, "%s | %s | %s %s (%s)" %( device[4], device[2], device[0], device[1], device[3] ) )
    deviceListBox.selection_set( first = 0 )
def removeDevice():
    global deviceList
    if( len( deviceList ) == 0 ):
        messagebox.showinfo("No Devices!", "There are no devices on the system!\nLoad up your device in range of your system, and make it discover-able!")
    if( deviceListBox.curselection() == () ):
        messagebox.showinfo("Select!", "You must select a device!")
        return
    Cursor.execute("DELETE FROM `devices` WHERE macaddr=?;", ( deviceList[ deviceListBox.curselection()[0] ][4], ) )
    Database.commit()
    inputDeviceList()

def changeOwnerDetails( window, fname, lname ):
    fname = fname.get()
    lname = lname.get()
    Cursor.execute("UPDATE `devices` SET `fname`=?,`lname`=? WHERE `macaddr`=?;", ( fname, lname, window.device[4], ) )
    Database.commit()
    window.destroy()
    inputDeviceList()

def setOwner():
    global deviceList
    if( len( deviceList ) == 0 ):
        messagebox.showinfo("No Devices!", "There are no devices on the system!\nLoad up your device in range of your system, and make it discover-able!")
    if( deviceListBox.curselection() == () ):
        messagebox.showinfo("Select!", "You must select a device!")
        return
    window = Toplevel( root )
    window.device = deviceList[ deviceListBox.curselection()[0] ]

    Label(window,text='Editing Device:\n%s (%s) - %s' % (window.device[2],window.device[4],window.device[3]) ).grid( column=0,row=0, columnspan=2 )

    Label(window,text='First Name:').grid( column=0,row=1, padx=(30,00), pady=(20,10) )
    fnameEntry = Entry(window, width=10)
    fnameEntry.grid( column=1,row=1, padx=(0,30), pady=(20,10), sticky="we" )

    Label(window,text='Last Name:').grid( column=0,row=2, padx=(30,00), pady=(0,10) )
    lnameEntry = Entry(window, width=10)
    lnameEntry.grid( column=1,row=2, padx=(0,30), pady=(0,10), sticky="we" )

    removeButton = Button( window, text="Set owner details", command=lambda: changeOwnerDetails( window, fnameEntry, lnameEntry ) )
    removeButton.grid( row=3, column=0, columnspan=2, padx=30, pady=10 )

def lastSeen():
    global deviceList
    if( len( deviceList ) == 0 ):
        messagebox.showinfo("No Devices!", "There are no devices on the system!\nLoad up your device in range of your system, and make it discover-able!")
    if( deviceListBox.curselection() == () ):
        messagebox.showinfo("Select!", "You must select a device!")
        return
    window = Toplevel( root )
    window.device = deviceList[ deviceListBox.curselection()[0] ]

    listbox = Listbox( window, height=20, width=60 )
    listbox.grid( row=1, column=1, columnspan=1)


    Cursor.execute("SELECT * FROM `seenlog` WHERE `macaddr`=?;", ( window.device[4], ))
    seenLog = Cursor.fetchall()

    if( seenLog == None ):
        messagebox.showinfo("No data!", "The device has not yet been seen by a node!")
        window.destroy()
        return
    else:
        for time, macaddr, nodeid in seenLog:
            listbox.insert( END, "Device was seen at %s by node ID %u" % ( strftime( "%X %x", localtime( time ) ), nodeid, ) )
    listbox_ScrollBar = Scrollbar(window, orient=VERTICAL, command=listbox.yview)
    listbox.configure(yscrollcommand=listbox_ScrollBar.set)
    listbox_ScrollBar.grid( row=1, column=2, sticky='ns' )

    
root = Tk()
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
titleLabel = Label( root, text="BlueTrack Menu", height=5, width=50 )
titleLabel.grid( row=0, column = 1, columnspan=3 )

setOwner = Button( root, text="Set Owner", height=3, width=15, command=setOwner )
setOwner.grid( row=1, column=1, padx=(12,0) )
lastSeenButton = Button( root, text="Last Seen", height=3, width=15, command=lastSeen )
lastSeenButton.grid( row=1, column=2 )
removeButton = Button( root, text="Remove Device", height=3, width=15, command=removeDevice )
removeButton.grid( row=1, column=3 )

deviceListBox = Listbox( root, height=20, width=60 )
deviceListBox.grid( row=2, column=1, columnspan=3, pady=(20,0))

deviceListBox_ScrollBar = Scrollbar(root, orient=VERTICAL, command=deviceListBox.yview)
deviceListBox.configure(yscrollcommand=deviceListBox_ScrollBar.set)
deviceListBox_ScrollBar.grid( row=2, column=4, pady=(20,0), sticky='ns' )


inputDeviceList()


root.mainloop()
 
