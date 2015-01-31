#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Copyright 2015 Daniele Basile <asterix24@gmail.com>
#

import fileinput
import datetime
import sys


if __name__ == '__main__':

    try:
        prev = None
        while 1:
            try:
                if prev is not None:
                    sys.stdout.write(">> ")
                else:
                    sys.stdout.write("> ")
                line = sys.stdin.readline()
                line = line.strip()
                if not line:
                    prev = None
                    continue

                if prev is not None:
                    minus = False
                    h = line.strip()
                    if '-' in h:
                        minus = True
                        h = h.replace('-','')
                    m = 0
                    if "." in h:
                        h, m = h.split(".")
                    elif "," in h:
                        h, m = h.split(",")

                    if minus:
                       tdelta = prev - datetime.timedelta(hours=int(h), minutes=int(m))
                       minus = False
                    else:
                       tdelta = prev + datetime.timedelta(hours=int(h), minutes=int(m))

                    print "%s" % tdelta
                else:
                    start, stop = line.strip().split("-")
                    if ":" in start:
                        start_FMT = '%H:%M'
                    elif "." in start:
                        start_FMT = '%H.%M'
                    elif "," in start:
                        start_FMT = '%H,%M'
                    else:
                        start_FMT = '%H'

                    if ":" in stop:
                        stop_FMT = '%H:%M'
                    elif "." in stop:
                        stop_FMT = '%H.%M'
                    elif "," in stop:
                        stop_FMT = '%H,%M'
                    else:
                        stop_FMT = '%H'

                    tdelta = datetime.datetime.strptime(stop, stop_FMT) - datetime.datetime.strptime(start, start_FMT)
                    print "%s - %s" % (start, stop)
                    sys.stdout.write("%s\n" % tdelta)

                prev = tdelta

            except ValueError:
                print "Formato errato!"
                continue

    except KeyboardInterrupt:
        sys.stdout.write("\n\nBye!\n")
        sys.exit(1)
