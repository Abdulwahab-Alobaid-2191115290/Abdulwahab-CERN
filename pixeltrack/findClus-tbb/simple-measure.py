#!/usr/bin/python3
import statistics


import os

# Get the current directory
current_dir = os.getcwd()

output = {}

# Loop through each file in the current directory
for filename in os.listdir(current_dir):
    if filename.endswith(".txt"):  # Check if the file is a text file
        file_path = os.path.join(current_dir, filename)
        with open(file_path, 'r') as f:

            lines = f.readlines()
            
            sums = 0
            for l in lines:
                kernel, time = l.split()
                sums += float(time)

            avgs = sums/len(lines)

            output[filename[:filename.index(".")]] = avgs


sorted_dict = dict(sorted(output.items(), key=lambda item: item[1]))

for key in sorted_dict:
    print(f"{key}: {sorted_dict[key]}")




