.PHONY: all clean

TARGETS := vecMult_cpu vecMult_tbb vecMult_mt vecMult_cuda

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

# NVIDIA CUDA
CUDA_BASE   ?= /usr/local/cuda

# Boost C++ library
BOOST_BASE  ?= /usr

# Intel TBB library
TBB_BASE    ?= /usr

# Alpaka library
ALPAKA_BASE ?= /home/fwyzard/src/alpaka-group/alpaka

CXX  := g++
NVCC := $(CUDA_BASE)/bin/nvcc

CXXFLAGS       := -std=c++17 -O2 -g -I$(BOOST_BASE)/include -I$(ALPAKA_BASE)/include
CXX_HOST_FLAGS := -pthread
CXX_CUDA_FLAGS := --expt-relaxed-constexpr

%_cpu: %.cc
	$(CXX) $(CXXFLAGS) $(CXX_HOST_FLAGS) -DALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLED $< -o $@ 

%_mt: %.cc
	$(CXX) $(CXXFLAGS) $(CXX_HOST_FLAGS) -DALPAKA_ACC_CPU_B_SEQ_T_THREADS_ENABLED $< -o $@ 

%_tbb: %.cc
	$(CXX) $(CXXFLAGS) $(CXX_HOST_FLAGS) -I$(TBB_BASE)/include -DALPAKA_ACC_CPU_B_TBB_T_SEQ_ENABLED $< -L$(TBB_BASE)/lib -ltbb -o $@

%_cuda: %.cc
	$(NVCC) -x cu -ccbin $(CXX) $(CXXFLAGS) $(CXX_CUDA_FLAGS) -Xcompiler '$(CXX_HOST_FLAGS)' -DALPAKA_ACC_GPU_CUDA_ENABLED $< -o $@ 


mcuda:
	./measure.py cuda/cuda_128x128_by_128x128.txt 
	./measure.py cuda/cuda_512x512_by_512x512.txt 
	./measure.py cuda/cuda_1024x1024_by_1024x1024.txt 
mtbb:
	./measure.py tbb/tbb_128x128_by_128x128.txt 
	./measure.py tbb/tbb_512x512_by_512x512.txt 
	./measure.py tbb/tbb_1024x1024_by_1024x1024.txt 
	./measure.py tbb/tbb_4096x4096_by_4096x4096.txt 
mcpu:
	./measure.py cpu/cpu_128x128_by_128x128.txt 
	./measure.py cpu/cpu_512x512_by_512x512.txt 
	./measure.py cpu/cpu_1024x1024_by_1024x1024.txt 
	./measure.py cpu/cpu_4096x4096_by_4096x4096.txt 

mmt:
	./measure.py mt/mt_128x128_by_128x128.txt 
	./measure.py mt/mt_512x512_by_512x512.txt 
	./measure.py mt/mt_1024x1024_by_1024x1024.txt 


