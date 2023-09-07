# Performance Measurement of Alpaka in a Heterogenous Computing Environment



## Alpaka
The Alpaka library is a header-only C++17 abstraction library for accelerator development.
Its aim is to provide performance portability across accelerators through the abstraction of the underlying levels of parallelism. More information can be found at [alpaka-group](https://github.com/alpaka-group/alpaka) github page.

![alpaka](https://github.com/alpaka-group/alpaka/blob/develop/docs/logo/alpaka_401x135.png)

## Abstract
The work is focused on analyzing how different backends behave within Alpaka, with emphasis on cpu backends such as CpuSerial, MT and Intel TBB. Analysis was carried on matrix multiplication problem first to analyze how these backends behave differently. After that, the work has been extended on the standalone version of [Pixeltrack](https://github.com/cms-patatrack/pixeltrack-standalone) application to address irregularities in CpuSerial and Intel TBB backends behavior within different modules of the application.

## File Organization

1. [pixeltrack](pixeltrack)
	- [default-pixeltrack](pixeltrack/default-pixeltrack): Readings of 31 kernels of pixeltrack using `serial`, `tbb` and `cuda` backends along with `plot.py` which shows how these backends compare with respect to each kernel.
    - [kernel_connect](pixeltrack/kernel_connect): Readings of `kernel_connect()` kernel that include changing the block count threshold in non-decreasing sequence.
    	- [tbb-kernel-connect](pixeltrack/kernel_connect/tbb-kernel-connect): Further analysis focused on the `tbb` backend which involves changing `numberOfStreams` and `numberOfThreads` when executing the program hoping to see improvement in the performance.
   
    - [findClus-tbb](pixeltrack/findClus-tbb): Measurements taken on `findclus()` kernel after modifying some factors such as block size and number of threads used with `tbb` backend. This later showed that this is not feasible since the kernel correctness internally depends on some of these factors.
    
    - [pixeltrack-threads](pixeltrack/threads-pixeltrack): Tests carried on the backends while changing `numberOfThreads` only.
    
    - [pixeltrack-scripts](pixeltrack/pixeltrack-scripts): Scripts used while doing the analysis including `parse.py` which injects profiling code into the source code of pixeltrack.
  

2. [vecMult](vecMult)
	- Tests on different `blockcount` and `blocksize` schemes each within a separate directory along with scripts used.
    - The plot containing the comparisons is found at [vecMult/plots/plot.py](vecMult/plots/plot.py)
    - The `cpu/`, `tbb/`, `mt/` and `cuda/` contain output files used by `measure.py` to generate `csv` files.
      
    
3. [plots](plots)
	- All related plots are found in this directory for quick reference.
