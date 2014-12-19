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
# Copyright 2014 Daniele Basile <asterix24@gmail.com>
#

import sys
import os

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--series", dest="series", default='e12', help="Resistor series.")
parser.add_option("-n", "--results", dest="n_results", default='5', help="Number of result to display.")

(options, args) = parser.parse_args()

E12 = [
    100.0,
    120.0,
    150.0, 
    180.0,
    220.0,
    270.0,
    330.0,
    390.0,
    470.0,
    560.0,
    680.0,
    820.0,
]

E24 = [
    100.0,
    110.0,
    120.0,
    130.0, 
    160.0,
    180.0,
    200.0,
    240.0,
    270.0,
    300.0,
    330.0,
    390.0,
    430.0,
    470.0,
    510.0,
    560.0,
    620.0,
    680.0,
    750.0,
    820.0,
    910.0,
]

MOLTIPLICATORE = [ 10, 100, 1000, 10000, 100000, 1000000, 10000000]

SERIES = E12
if options.series.lower() == 'e12':
    SERIES = E12
if options.series.lower() == 'e24':
    SERIES = E24

print args, options.series.upper()

req = float(args[0])
if not req:
    print "Resistenza è zero"
    sys.exit(0)

ireq = 1/req

r2_chose = 0
r_chose_diff = []


for r1 in SERIES:
    for m in MOLTIPLICATORE:
        r1 = r1 * m
        if r1 == req:
            print "%d  R1:%s R2:%s Req=%s <-> Reqref=%s diff:%s %s%%" % (1, int(r1), 'NP', req, req, 0, 0)
            sys.exit(0)

for r1 in SERIES:
    for m in MOLTIPLICATORE:
        r1 = r1 * m

        ir1 = 1/r1
        ir2 = ireq - ir1

        if not ir2:
            continue

        r2 = 1/ir2

        if r2 < 0:
            continue

        # Cerco il valore più vicino
        diff = []
        for l, x in enumerate(SERIES):
            diff.append((abs(r2 - (x * m)),l))

        d, index = min(diff, key=lambda v: v[0])
        r2_chose = SERIES[index]* m

        #Verifico il valore trovato
        ireq_v = (1/r2_chose) + (1/r1)
        req_v = 1/ireq_v

        r_chose_diff.append((r1, r2_chose, abs(req - req_v), req, req_v))
        

show_n = int(options.n_results)
for j in range(show_n):
    r1,r2,diff,r,rv = min(r_chose_diff, key=lambda v: v[2])
    rv = round(rv,3)
    d = round(diff,3)
    p = round(d / r * 100, 3)
    print "%d  R1:%s R2:%s Req=%s <-> Reqref=%s diff:%s %s%%" % (j, int(r1), int(r2), rv, r, d, p)

    for n, z in enumerate(r_chose_diff):
        if r1 == z[0] and r2 == z[1]:
            r_chose_diff.pop(n)

