Misc Tools
==========

Collection of utility for various daily problems.

Serial monitoring
-----------------

This simple utility log serial output to stdout and on a file. You could pass variuos parametiter to set the port name, baudrate, log file name, etc.

```
$ python serial/serial_log.py -p /dev/ttyUSB1
```

There are alse a simple switch that show the list of serial port avaible on your machine.

```
$ python serial/serial_log.py -l
/dev/cu.usbserial USB-Serial Controller USB VID:PID=67b:2303 SNR=None
/dev/cu.usbserial-FTG6PM4N ChiPi USB <-> Serial USB VID:PID=403:6001 SNR=FTG6PM4N
/dev/cu.Bluetooth-PDA-Sync                  n/a n/a
/dev/cu.Bluetooth-Modem                  n/a n/a

```

#### Requirement

The only package that you need is pyserial (http://pyserial.sourceforge.net/), also avaible via pip.

```
$ pip install pyserial
```
