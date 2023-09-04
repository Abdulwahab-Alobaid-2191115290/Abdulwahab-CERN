#!/usr/bin/python3

# executes parse.py for the source files of alpaka located in src/alpaka/

import subprocess
import os
import sys
import re


# main

# all source files
fs = [val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk('./src/alpaka/')] for val in sublist]

# execluding files in the test directory
files = [ f for f in fs if "test" not in f]

# calling parse.py for each file
for f in files:
    p = subprocess.Popen(['./parse.py', f])
    p.wait()


