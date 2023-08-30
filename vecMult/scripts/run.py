#!/usr/bin/python3

import subprocess
import os
import sys

if len(sys.argv) != 3:
    print('expected, ', sys.argv[0], ' <executable> <number of processes>')
    exit()

procs = sys.argv[2]
program = "./" + sys.argv[1]

for i in range( int(sys.argv[2]) ):
    p = subprocess.Popen([program])
    p.wait()

