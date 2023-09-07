#!/usr/bin/python3
import statistics

# serial kernels
with open('serial-kernel-connect.txt') as f:

    lines = f.readlines()
    
    kernels = {}    # { "kernel_1": time_in_nanoseconds, etc.. }
    for l in lines:
        thresh, time = l.split()
        if thresh in kernels:
            kernels[thresh].append(int(time))
        else:
            kernels[thresh] = [int(time)]

    sums = {}   # { "kernel_1": sum_of_time_taken }
    for k in kernels:
       
        if k not in sums:
            sums[k] = 0
        
        for t in kernels[k]:
            sums[k] += t

    avgs = {}   # { "kernel_1": avg_of_time_taken }
    for k in kernels:
        avgs[k] = sums[k]/len(kernels[k])

    
    std = {}   # { "kernel_1": standard_deviation_of_time_taken }
    for k in kernels:
        std[k] = statistics.stdev(kernels[k])

    # write to file
    with open("serial-kernels.csv", "a") as sf:
        sf.write('thresh,time,stdev\n')
        for k in kernels:
            sf.write(f"{k},{avgs[k]},{std[k]}\n")

    print('the average of each kernel <serial> in ns: \n')
    for a in avgs:

        print(f'{a}: {avgs[a]}')


# tbb kernels
with open('tbb-kernel-connect.txt') as f:

    lines = f.readlines()
    
    kernels = {}    # { "kernel_1": time_in_nanoseconds, etc.. }
    for l in lines:
        thresh, time = l.split()
        if thresh in kernels:
            kernels[thresh].append(int(time))
        else:
            kernels[thresh] = [int(time)]

    sums = {}   # { "kernel_1": sum_of_time_taken }
    for k in kernels:
       
        if k not in sums:
            sums[k] = 0
        
        for t in kernels[k]:
            sums[k] += t

    avgs = {}   # { "kernel_1": avg_of_time_taken }
    for k in kernels:
        avgs[k] = sums[k]/len(kernels[k])

    # write to file
    with open("tbb-kernels.csv", "a") as sf:
        sf.write('thresh,time,stdev\n')
        for k in kernels:
            sf.write(f"{k},{avgs[k]},{std[k]}\n")

    print('\n\nthe average of each kernel <tbb> in ns: \n')
    for a in avgs:

        print(f'{a}: {avgs[a]}')

# cuda kernels
with open('cuda-kernel-connect.txt') as f:

    lines = f.readlines()
    
    kernels = {}    # { "kernel_1": time_in_nanoseconds, etc.. }
    for l in lines:
        thresh, time = l.split()
        if thresh in kernels:
            kernels[thresh].append(int(time))
        else:
            kernels[thresh] = [int(time)]

    sums = {}   # { "kernel_1": sum_of_time_taken }
    for k in kernels:
       
        if k not in sums:
            sums[k] = 0
        
        for t in kernels[k]:
            sums[k] += t

    avgs = {}   # { "kernel_1": avg_of_time_taken }
    for k in kernels:
        avgs[k] = sums[k]/len(kernels[k])

    
    std = {}   # { "kernel_1": standard_deviation_of_time_taken }
    for k in kernels:
        std[k] = statistics.stdev(kernels[k])

    # write to file
    with open("cuda-kernels.csv", "a") as sf:
        sf.write('thresh,time,stdev\n')
        for k in kernels:
            sf.write(f"{k},{avgs[k]},{std[k]}\n")

    print('the average of each kernel <cuda> in ns: \n')
    for a in avgs:

        print(f'{a}: {avgs[a]}')



