#!/usr/bin/python3

import statistics

from os import listdir
from os.path import isfile, join
import sys

def to_seconds(micro):
    return micro / 1000000

def file_dict():
    dirs = ["./tbb", "./cpu", "./mt", "./cuda"]

    f_dict = {}
    for d in dirs:
        txtfiles = [f for f in listdir(d) if ( isfile(join(d, f)) and f.endswith('.txt') ) ]
        f_dict[d] = txtfiles
        
    return f_dict

def avg_stdev(filename):

    # get readings of the file
    readings = open(filename).readlines()
    int_readings = []

    if len(readings) < 1:
        print("file should contain at least 1 reading")
        exit()
    
    pre = 0;
    ker = 0;
    pos = 0;
    for r in readings:
        arr = r.split()

        pre += int(arr[0])
        ker += int(arr[1])
        pos += int(arr[2])
        
        int_readings.append(int(arr[1]))



    avg_pre = (pre / len(readings)) 
    avg_ker = (ker / len(readings)) 
    avg_pos = (pos / len(readings))

    return [statistics.stdev(int_readings), avg_pre, avg_ker, avg_pos]

# read all files in each directory

files_d = file_dict()   # returns {"./cpu": [txt, files, in, the, cpu, directory], ..}

# for each file write to the csv size, time, standard deviation, backend

for key in files_d:
    
    backend = key[2:]
    csv = open(f"{backend}.csv", "w")
    csv.truncate()
    csv.write("size,time,stdev\n")

    for filename in files_d[key]:
        
        stats = avg_stdev(key + '/' + filename)
        time = stats[2]
        stdev = stats[0]
        size = filename[:filename.find("x")]

        line = f"{size},{time},{stdev}\n"
        csv.write(line)
    
    csv.close()


"""
print("\nmeasuring performance of: ", sys.argv[1], "\n")


print("Average Time: \n")

print("Memory Allocation (pre) : %.4f seconds" % to_seconds(avg_pre))
print("Memory Allocation (pre) : %.4f microseconds" % avg_pre)
print()

print("Kernel Execution        : %.4f seconds" % to_seconds(avg_ker))
print("Kernel Execution        : %.4f microseconds" % avg_ker)
print()

print("Memory Allocation (post): %.4f seconds" % to_seconds(avg_pos))
print("Memory Allocation (post): %.4f microseconds" % avg_pos)
print()
"""
