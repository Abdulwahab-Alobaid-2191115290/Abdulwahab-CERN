#!/usr/bin/python3

import subprocess
import os
import sys
import re


# main

fs = [val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk('./src/alpaka/')] for val in sublist]

files = [ f for f in fs if "test" not in f]

for f in files:
    p = subprocess.Popen(['./parse.py', f])
    p.wait()


