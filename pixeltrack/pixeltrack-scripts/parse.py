#!/usr/bin/python3

# this script dynamically injects profiling code at kernel locations in alpaka src code

import subprocess
import os
import sys
import re

# if kernel name is within a namespace and/or template notation extract it alone
def extract_tl_function(single_function_string):
    if "::" in single_function_string:
        parts = single_function_string.split("::")
        function_name = parts[-1].strip()
    else:
        function_name = single_function_string.strip()

    if '<' in function_name and '>' in function_name:
        template_start_idx = function_name.index('<')
        template_end_idx = function_name.rindex('>')
        function_name = function_name[:template_start_idx] + function_name[template_end_idx + 1:]
    
    return function_name

# return idx of nth occurence of character
def nth_occ_idx(input_string, target_char, n):
    start_idx = -1
    for _ in range(n):
        start_idx = input_string.find(target_char, start_idx + 1)
        if start_idx == -1:
            return -1
    return start_idx


# returns line numbers that contain kernel calls
def get_lines(file):

    # if the file does not contain a kernel call skip it
    try:
        # in pixeltrack alpaka::enqueue() is used to launch kernels
        output = subprocess.check_output(['grep', '-n', 'alpaka::enqueue(', file])
    except:
        #print(file, "does not contain a kernel call, skipping file")
        exit()

    # extract line numbers from grep output
    regex = r"\d+:"
    instances = re.findall(regex, str(output))
    
    lines = [ ins[:-1] for ins in instances ]
   
    return lines

# returns string between two substrings
def get_str_between(sub1, sub2, content):


    # getting index of substrings
    idx1 = content.index(sub1)
    idx2 = content.index(sub2)

    # length of substring 1 is added to
    # get string from next character
    res = content[idx1 + len(sub1) + 1: idx2]
    
    return res

"""
alpaka::enqueue(
          queue,
          alpaka::createTaskKernel<TAcc>(workDiv, multiBlockPrefixScanFirstStep<uint32_t>(), poff, poff, num_items));
"""

# finds kernel name recursively when 1 alpaka::enqueue() is written in multiple lines <not used>
def find_kernel(contents, idx, comma, concat):
    print('~')
    line = contents[idx-1]
    for char in range(len(line)):
        if line[char] == ',':
            comma += 1
            continue
        elif comma == 2:
            print("concat: ", concat)
            print("kernel: ", concat[char: nth_occ_idx(concat, ',', 3)])
            return
        else:
            continue
    find_kernel(contents, idx + 1, comma, line + contents[idx])
 

# to extract kernel names with line numbers into a dictionary
def dictify(file, lines):
    
    f = open(file, "r")
    contents = f.readlines()

    kernels = {}


    print(file, ": \n")
    for l in lines:
        idx = int(l)
        line = contents[idx - 1]

        # as long as alpaka::enqueue(); is not in one line, keep adding trailing lines to construct the whole line and then extract kernel name
        while "));" not in line and ");" not in line:
            idx += 1
            line += contents[idx - 1]

        # suporting kernels that are explicitly called with alpaka::createTaskKernel
        if "alpaka::createTaskKernel" not in line:
            continue

        # remove \n and whitespace
        line = line.strip().replace('\n','').replace(' ','')
        # the kernel name is between the second and third comma    
        line = line[nth_occ_idx(line, ',', 2) + 1: nth_occ_idx(line, ',', 3)]
        # remove namepsaces and template notation from kernel name
        line = extract_tl_function(line)
        print(line) 
        print("~~~")
        
        # skip irregural kernel calls eg. enqueue(*(..), *(..)); // CachingAllocator.h 194
        #if "block.queue" in line or "[" in line or "*event_" in line or "*data.m_event" in line:
            #continue

        # tuple (start, end): start of the function, end of the function
        kernels[line] = (int(l), idx)

    return kernels



# main

if len(sys.argv) != 2:
    print('expected: ', sys.argv[0], ' <sourcefile>')
    exit()

file = sys.argv[1]


# get lines that have kernels e.g [31, 72, etc..]
lines = get_lines(file)

# returns {kernel_1: line #, kernel_2: line #, etc..}
kernels = dictify(file, lines)
done = []

# for each kernel call in the source file
for k in kernels:
    
    # line numbers change after adding extra lines, so we need to recalculate
    lines = get_lines(file)
    kernels = dictify(file, lines)

    # start by making the variables
    #print("variables phase")    

    # kernel name
    kernel = k[:-2] if ('<' not in k) else k[:nth_occ_idx(k, '<', 1)]

    # auto kernel_start = ...;
    start = "auto " + f"{kernel}_start" + " = std::chrono::high_resolution_clock::now();\n"

    # auto kernel_end = ...;
    end = "auto " + f"{kernel}_end" + " = std::chrono::high_resolution_clock::now();\n"
    
    # alpaka wait function
    wait = "alpaka::wait(queue);\n"

    # auto kernel_diff = ...;
    diff = "auto " + f"{kernel}_diff" + " = std::chrono::duration_cast<std::chrono::nanoseconds>(" + f"{kernel}_end - {kernel}_start" + ");\n"

    # open file and append kernel_diff.count()
    file_op  = f"std::fstream {kernel}_file;\n"
    file_op += f'{kernel}_file.open("kernels.txt", std::ios::app);\n'
    file_op += f"{kernel}_file << " + f'"{k} "' + " << " + f'{kernel}_diff.count()' + '<<' + "std::endl;\n" + f"\t{kernel}_file.close();\n"

    # write those variables to the file if the kernel is not parsed 
    if k in done:
        continue
    
    # which line has the kernel call
    start_idx, end_idx = kernels[k]
    
    with open(file, 'r') as f:
        lines = f.readlines()

    # if the kernel is called in one line
    if start_idx == end_idx:
        # insert profiling variables
        lines.insert(start_idx-1, start)
        lines.insert(start_idx-1, wait)
        lines.insert(start_idx + 2, wait)
        lines.insert(start_idx + 3, end)
        lines.insert(start_idx + 4, diff)
        lines.insert(start_idx + 5, file_op)
    else:
        lines.insert(start_idx-1, start)
        lines.insert(start_idx-1, wait)
        lines.insert(end_idx + 2, wait)
        lines.insert(end_idx + 3, end)
        lines.insert(end_idx + 4, diff)
        lines.insert(end_idx + 5, file_op)

    # write them to the actual file
    with open(file, 'w') as f:
        f.writelines(lines)

    # flag the kernel as done
    done.append(k)
