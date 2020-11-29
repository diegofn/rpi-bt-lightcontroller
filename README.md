**rpi-bt-lightcontroller**
======================

RaspberryPi light controller using bluetooth.
It was tested in RaspberryPi ZeroW.

# Requirements

On raspbian or raspberryos, install the required python bluetooth, bluez firmaware, bluetooth and GPIO python libraries:
```
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install bluetooth bluez
$ sudo apt install python-bluetooth
$ sudo apt install python-rpi.gpio
```

Install the bluetooth python packages
```
$ pip3 install PyBluez
```

Enable the serial port in bluetooth.
```bash
$ sudo vi /etc/systemd/system/dbus-org.bluez.service
```
Add the compatibily -C flag and the SP profile
```
ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP
```

Grant the pi user to use bluetooth service
```
$ sudo adduser pi bluetooth
$ sudo reboot
```



# Setup bluetooth 
1. Check the bluetooth service
```
$ bluetoothctl -v
$ sudo systemctl status blueto*
```

2. Open the bluethoothctl utility 
```
$ bluetoothctl

[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# discoverable on
[bluetooth]# pairable on
[bluetooth]# scan on
```

3. Please pair your raspberrypi with your smartphone.

# Android Bluetooth client

You can use the following Android Client to test the light control
https://github.com/diegofn/BTLightController

or test it with a bluetooth chatbot controller using
https://play.google.com/store/apps/details?id=com.electrotoolbox.bluetoothterminal


# Optional - Updating blueZ 
Some rasperrypios distribution does not support a bluetooth serial interface, you need to update the BlueZ with the following commands    
```
$ mkdir ~/Documents/bluez
$ cd ~/Documents/bluez
$ sudo apt update
$ sudo apt install libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
$ curl -L https://www.kernel.org/pub/linux/bluetooth/bluez-5.55.tar.gz > bluez-5.55.tar.gz
$ tar -zxvf bluez-5.55.tar.gz 
$ cd bluez-5.55/
$ ./configure --prefix=/usr --mandir=/usr/share/man --sysconfdir=/etc --localstatedir=/var --enable-experimental
$ sudo make install
```

Change the BlueZ policy
```
$ sudo cp /etc/dbus-1/system.d/bluetooth.conf /etc/dbus-1/system.d/bluetooth.conf.bak
$ sudo vi /etc/dbus-1/system.d/bluetooth.conf
```

Add the following lines
```
...
  <policy user="root">
    <allow own="org.bluez"/>
    <allow send_destination="org.bluez"/>
    <allow send_interface="org.bluez.Agent1"/>
    <allow send_interface="org.bluez.MediaEndpoint1"/>
    <allow send_interface="org.bluez.MediaPlayer1"/>
    <allow send_interface="org.bluez.Profile1"/>
    <allow send_interface="org.bluez.AlertAgent1"/>
    <allow send_interface="org.bluez.ThermometerWatcher1"/>
    <allow send_interface="org.bluez.HeartRateWatcher1"/>
    <allow send_interface="org.bluez.CyclingSpeedWatcher1"/>
    <allow send_interface="org.bluez.GattCharacteristic1"/>
    <allow send_interface="org.bluez.GattDescriptor1"/>
    <allow send_interface="org.bluez.LEAdvertisement1"/>
    <allow send_interface="org.freedesktop.DBus.ObjectManager"/>
    <allow send_interface="org.freedesktop.DBus.Properties"/>
  </policy>

  <!-- allow users of bluetooth group to communicate -->
  <policy group="bluetooth">
    <allow send_destination="org.bluez"/>
  </policy>

  <policy at_console="true">
    <allow send_destination="org.bluez"/>
  </policy>
```