#!/usr/bin/python3
import statistics

# serial kernels
with open('serial-kernels.txt') as f:

    lines = f.readlines()
    
    kernels = {}    # { "kernel_1": time_in_nanoseconds, etc.. }
    for l in lines:
        kernel, time = l.split()
        if kernel in kernels:
            kernels[kernel].append(int(time))
        else:
            kernels[kernel] = [int(time)]

    sums = {}   # { "kernel_1": sum_of_time_taken }
    for k in kernels:
       
        if k not in sums:
            sums[k] = 0
        
        for i in kernels[k]:
            sums[k] += i

    avgs = {}   # { "kernel_1": avg_of_time_taken }
    for k in kernels:
        avgs[k] = sums[k]/len(kernels[k])

    
    std = {}   # { "kernel_1": standard_deviation_of_time_taken }
    for k in kernels:
        std[k] = statistics.stdev(kernels[k])

    # write to file
    with open("serial-kernels.csv", "w") as sf:
        sf.write('kernel,time,stdev\n')
        for k in kernels:
            sf.write(f"{k},{avgs[k]},{std[k]}\n")

    print('the average of each kernel <serial> in ns: \n')
    for a in avgs:

        print(f'{a}: {avgs[a]}')


# tbb kernels
with open('tbb-kernels.txt') as f:

    lines = f.readlines()
    
    kernels = {}    # { "kernel_1": time_in_nanoseconds, etc.. }
    for l in lines:
        kernel, time = l.split()
        if kernel in kernels:
            kernels[kernel].append(int(time))
        else:
            kernels[kernel] = [int(time)]

    sums = {}   # { "kernel_1": sum_of_time_taken }
    for k in kernels:
       
        if k not in sums:
            sums[k] = 0
        
        for i in kernels[k]:
            sums[k] += i

    avgs = {}   # { "kernel_1": avg_of_time_taken }
    for k in kernels:
        avgs[k] = sums[k]/len(kernels[k])

    # write to file
    with open("tbb-kernels.csv", "w") as sf:
        sf.write('kernel,time,stdev\n')
        for k in kernels:
            sf.write(f"{k},{avgs[k]},{std[k]}\n")

    print('\n\nthe average of each kernel <tbb> in ns: \n')
    for a in avgs:

        print(f'{a}: {avgs[a]}')


# cuda kernels
with open('cuda-kernels.txt') as f:

    lines = f.readlines()
    
    kernels = {}    # { "kernel_1": time_in_nanoseconds, etc.. }
    for l in lines:
        kernel, time = l.split()
        if kernel in kernels:
            kernels[kernel].append(int(time))
        else:
            kernels[kernel] = [int(time)]

    sums = {}   # { "kernel_1": sum_of_time_taken }
    for k in kernels:
       
        if k not in sums:
            sums[k] = 0
        
        for i in kernels[k]:
            sums[k] += i

    avgs = {}   # { "kernel_1": avg_of_time_taken }
    for k in kernels:
        avgs[k] = sums[k]/len(kernels[k])

    # write to file
    with open("cuda-kernels.csv", "w") as sf:
        sf.write('kernel,time,stdev\n')
        for k in kernels:
            sf.write(f"{k},{avgs[k]},{std[k]}\n")

    print('\n\nthe average of each kernel <tbb> in ns: \n')
    for a in avgs:

        print(f'{a}: {avgs[a]}')


