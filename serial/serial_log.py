#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2014 Daniele Basile <asterix24@gmail.com>
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import serial.tools.list_ports
import sys
import datetime
import os

from optparse import OptionParser

FILE_NAME_FMT="serial_log_%Y%m%d-%H%M%S.log"

parser = OptionParser()
parser.add_option("-p", "--port", dest="port_name", default='/dev/ttyUSB0', help="Serial Port.")
parser.add_option("-b", "--baud", dest="port_baudrate", default='115200', help="Serial Port baudrate.")
parser.add_option("-l", "--list", action="store_true", dest="port_list", default=False, help="Show all connected serial port.")
parser.add_option("-a", "--append", action="store_true", dest="file_append", default=False, help="Append to log file.")
parser.add_option("-d", "--log-directory", dest="log_dir", default="/tmp", help="Directory where place log files.")
parser.add_option("-f", "--log-filename", dest="log_filename", default=datetime.datetime.today().strftime(FILE_NAME_FMT), help="File log name.")

(options, args) = parser.parse_args()

def fmt_line(line):
    pre = datetime.datetime.today().strftime("%a, %d %b %Y %H:%M:%S")
    line = "%s: %s" % (pre, line)
    return line

def std_print(line):
    sys.stdout.write(line)
    sys.stdout.flush()

if options.port_list:
    for i in serial.tools.list_ports.comports():
        std_print("%10s %20s %s\n" % (i[0], i[1], i[2]))
    sys.exit(0)

std_print("Open: %s" % options.port_name)

try:
    s = serial.Serial(
        port=options.port_name,
        baudrate=options.port_baudrate, # baudrate
        bytesize=8,                     # number of databits
        parity=serial.PARITY_NONE,
        stopbits=1,
        xonxoff=0,              # enable software flow control
        rtscts=0,               # disable RTS/CTS flow control
        timeout=5               # set a timeout value, None for waiting forever
        )

    s.setDTR(0) #disabilito reset
    s.setRTS(1) #disabilito boot0

    
    file = os.path.join(options.log_dir, options.log_filename)
    m = 'w'
    if options.file_append:
        m = 'w+'

    o = open(file, m)
    std_print("Log file: %s" % file)

    while 1:
        line = s.readline()
        if line:
            std_print(line)

            o.write(fmt_line(line))
            o.flush()


except KeyboardInterrupt:
    std_print('Close serial')
    s.flush()
    s.close()
    o.close()

