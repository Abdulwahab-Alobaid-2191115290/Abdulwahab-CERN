#!/usr/bin/python3

import statistics

from os import listdir
from os.path import isfile, join
import sys

# returns string between two characters used for `
def get_str_between(string, first_char, second_char):
  """Returns the string between the two specified characters in the given string.

  Args:
    string: The string to search.
    first_char: The first character to search for.
    second_char: The second character to search for.

  Returns:
    The string between the two specified characters in the given string.
  """

  start_index = string.find(first_char)
  end_index = string.find(second_char, start_index + 1)
  if start_index == -1 or end_index == -1:
    return ""
  return string[start_index + 1:end_index]

# returns avg and stdev for cpu utilization and throughput
def get_stats(filename):

    # get readings of the file
    readings = open(filename).readlines()
    int_readings = []

    if len(readings) < 1:
        print("file should contain at least 1 reading")
        exit()
    
    throughput  = 0;
    utilization = 0;
    
    readings_t = []
    readings_u = []

    # for each line on the form "<throughput> <utilization>"
    for r in readings:
        arr = r.split()

        throughput  += float(arr[0])
        utilization += float(arr[1])
        
        readings_t.append(float(arr[0]))
        readings_u.append(float(arr[1]))

    # avg and stdev for throughput
    avg_t = (throughput / len(readings)) 
    stdev_t = statistics.stdev(readings_t)
    
    # avg and stdev for utilization  
    avg_u = (utilization / len(readings)) 
    stdev_u = statistics.stdev(readings_u)

    # return (avg_t, avg_u, stdev_t, stdev_u)
    return (avg_t, avg_u, stdev_t, stdev_u)


backends = ["serial", "tbb", "cuda", "hip"]
txtfiles = [f for f in listdir('./') if ( isfile(join('./', f)) and f.endswith('.txt') ) ]

# create and setup csv files
for b in backends:
    csv = open(f"{b}.csv", "w")
    csv.truncate()
    csv.write("threads,avg_t,avg_u,stdev_t,stdev_u\n")
    csv.close()


lines = {"serial": [], "tbb": [], "cuda": []}
# txtfiles e.g: serial_x32_threads.txt, serial_x64_threads.txt, tbb_x32_threads.txt, tbb_x64_threads.txt
for f in txtfiles:

    # extract backend and threads
    backend = f[:f.find("_")]
    threads = get_str_between(f, "x", "_")
    
    # get stats
    avg_t, avg_u, stdev_t, stdev_u = get_stats(f)

    #csv = open(f"{backend}.csv", "a")

    #csv.write(f"{threads},{avg_t},{avg_u},{stdev_t},{stdev_u}\n")

    #csv.close()

    lines[backend].append((threads, f"{threads},{avg_t},{avg_u},{stdev_t},{stdev_u}\n"))

print(lines)

# as extra sort lines before writing to csv
def sort_lines(lines):
    pass



