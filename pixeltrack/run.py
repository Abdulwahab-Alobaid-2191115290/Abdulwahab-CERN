#!/usr/bin/python3

import subprocess
import os
import sys


program = "./alpaka"
backends = ["--serial", "--tbb", "--cuda"]
numberOfThreads = [32, 64, 128, 256, 512, 1024]
numberOfThreadsOption = "--numberOfThreads"
nprocs = 10

# for each backend
for backend in backends:
    # for each number of threads
    for nthreads in numberOfThreads:
        # run the program 10 times
        for i in range( nprocs ):
            print([ program, backend, numberOfThreadsOption, nthreads ])
            p = subprocess.Popen([ program, backend, numberOfThreadsOption, str(nthreads) ])
            p.wait()


# then produce the csv files using measure.py
measure = "./measure.py"
p = subprocess.Popen([ measure ])
p.wait()

