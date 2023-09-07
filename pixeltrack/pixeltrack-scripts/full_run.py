#!/usr/bin/python3

import subprocess
import os
import sys
from os import listdir
from os.path import isfile, join

./alpaka --serial --numberOfThreads 64

alpaka = "./alpaka"
measure = "./measure.py"
times = "10"
threads = 

backends= ["--tbb", "--serial", "--cuda"]

for b in backends:
   
    #print("\nRunning ", backends[i], " backend")
    p = subprocess.Popen([ "./alpaka", b, "--numberOfThreads", ])
    p.wait()
    #print(backends[i], " Done!")
    
    
    txtfile = [f for f in listdir("./") if ( isfile(join("./", f)) and f.endswith('.txt') ) ]
     
    p = subprocess.Popen([ "mv", txtfile[0], backends[i]])
    p.wait()
   

p = subprocess.Popen([ measure ])
p.wait() 

