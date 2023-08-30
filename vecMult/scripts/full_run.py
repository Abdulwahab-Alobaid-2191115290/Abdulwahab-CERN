#!/usr/bin/python3

import subprocess
import os
import sys
from os import listdir
from os.path import isfile, join

run = "./run.py"
measure = "./measure.py"
times = "10"

targets = ["vecMult_tbb", "vecMult_cpu", "vecMult_mt", "vecMult_cuda"]
backends= ["tbb", "cpu", "mt", "cuda"]

for i in range(len(targets)):
   
    #print("\nRunning ", backends[i], " backend")
    p = subprocess.Popen([ run, targets[i], times])
    p.wait()
    #print(backends[i], " Done!")
    
    
    txtfile = [f for f in listdir("./") if ( isfile(join("./", f)) and f.endswith('.txt') ) ]
     
    p = subprocess.Popen([ "mv", txtfile[0], backends[i]])
    p.wait()
   

p = subprocess.Popen([ measure ])
p.wait() 

