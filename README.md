## BlueTrack ##
BlueTrack is a bluetooth based tracking system. It does not require actively participating users to have their bluetooth in a discoverable state, although it does require some prior-setup from them.

----------

### Upcoming Developments ###

 - Easy to change MySQL and SQLite database driver.
 - GUI / CLI User interface for viewing logs and changing device data.

----------

### Requirements ###
BlueTrack requires a device with the following:

 - [The PyBluez Bluetooth Library by Karulis](https://github.com/karulis/pybluez)
 - The default Python SQLite3 library.

### Setup ###

Simply clone the system to your device, and edit the configuration.
```
git clone https://github.com/KiloSierraCharlie/BlueTrack.git
```

```
configuration = [

  # Polling time (How often, in seconds, do you want to check who is around?)
  
  3,
  
  # Polling timeout (How long do you want the script to wait before declaring a device out-of-area?)
  
  3,
  
  #The node ID of this device (If you have multiple devices polling the same network of devices.)
  
  1,
  
]
```

**Apart from that, have fun!**
