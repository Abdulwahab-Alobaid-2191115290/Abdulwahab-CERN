#include <cassert>
#include <cstdio>
#include <random>
#include <alpaka/alpaka.hpp>

#include <time.h>

#include "config.h"
#include "workdivision.h"

// returns raw accelerator name
std::string getAccName(std::string fullname){
	
	for(int c = 0; c < fullname.length(); c++){
		if(fullname[c] == '<'){
			return fullname.substr(0, c);
		}
	}
	return fullname;
}


// 2-dimensional and linearised buffer size
const int rows1 = 4096;	// # rows of array 1
const int rows2 = 4096;	// should match cols1
const int cols1 = 4096;	// # cols of array 1
const int cols2 = 4096;
const int rows3 = rows1;
const int cols3 = cols2;

constexpr Vec2D ndsize1 = {rows1, cols1}; 
constexpr Vec2D ndsize2 = {rows2, cols2}; 
constexpr Vec2D ndsize3 = {rows3, cols3}; 
constexpr size_t size1 = ndsize1.prod();	// used when accessing as 1D array
constexpr size_t size2 = ndsize2.prod();	
constexpr size_t size3 = ndsize3.prod();	

// threads and blocks
const int blocksX = 8;		// recall that each block resembles a kernel call
const int blocksY = 8;
const int threadsPerBlockX = 8;		// in cpu backend this will be "elements"
const int threadsPerBlockY = 8;

auto max(auto a, auto b){
	return a*(a>b) + b*(a<=b);
}


struct VectorMultKernel2D {
	template <typename TAcc, typename T>
	ALPAKA_FN_ACC void operator()(TAcc const& acc,T const* __restrict__ in1,T const* __restrict__ in2, T* __restrict__ out) const {
			
		/* following block replaced with stride function
		 * // x dim index is [1] and and y dim index is [0]
		 * auto const idx_r = alpaka::getIdx<alpaka::Grid, alpaka::Threads>(acc)[1];	// row idx (this can also be used alone if you want access asD
		 * auto const idx_c = alpaka::getIdx<alpaka::Grid, alpaka::Threads>(acc)[0];	// col idx
		
		 * auto const bid_x = alpaka::getIdx<alpaka::Grid, alpaka::Blocks>(acc)[1];
		 * auto const bid_y = alpaka::getIdx<alpaka::Grid, alpaka::Blocks>(acc)[0];

		 * // calculate 2D index in row major fasion
		 * auto index = idx_r*cols2 + idx_c;

		 * printf("block: %d x %d - thread %d x %d \n", bid_x, bid_y, idx_r, idx_c);
		 * printf("block: row %d col %d idx %d\n", idx_r, idx_c, index);
		*/
		
		//printf("\n ~~ start stride ~~ \n");
		for(auto dimensional_idx: elements_with_stride_nd(acc, ndsize3)){
			auto idx_r = dimensional_idx[0];	// x idx
			auto idx_c = dimensional_idx[1];	// y idx
			
			auto index = idx_r*cols2 + idx_c;

			
			//printf("row %d col %d idx %d\n", idx_r, idx_c, index);
				
			// formula for accessing 2D arrays using 1 index + the multiplication operation
			out[index] = 0;
			for(auto k = 0; k < cols1; k++){
				auto idx1 = idx_r*cols1 + k;
				auto idx2 = k*cols2 + idx_c;	
					
				out[index]+= in1[idx1] * in2[idx2];
			}
		}
		//printf("~~ end stride ~~ \n");

	} // end kernel

};

// function that verifies the matrix multiplication
void verify(auto a, auto b, auto result){
  	// Initialize the check array as a 1D array
	int check[rows3 * cols3];

	// Initialization of check array
	for (int r = 0; r < rows3; r++) {
		for (int c = 0; c < cols3; c++) {
         		int idx = r * cols3 + c;
            		check[idx] = 0; // Set all elements to 0
        	}
    	}

    	// Multiplication
    	for (int r = 0; r < rows1; r++) {
        	for (int c = 0; c < cols2; c++) {
            		for (int i = 0; i < cols1; i++) {
                	int idx = r * cols2 + c;
                	check[idx] += a[r * cols1 + i] * b[i * cols2 + c]; // Corrected indexing and multiplication
            		}
        	}
    	}

    	// Compare check with result
    	for (int r = 0; r < rows3; r++) {
        	for (int c = 0; c < cols3; c++) {
            		int idx = r * cols3 + c;
            		if (result[idx] != check[idx]) {
                		std::cout << "Error at [" << r << "][" << c << "]\nResult: Failure\n";
                		return;
            		}
        	}
    	}

    	std::cout << "\nResult: Success\n\n";	
}

// function to run the kernel
void testVectorMultKernel2D(Host host, Device device) {
	
	srand(time(0));

	// allocate input and output host buffers in pinned memory accessible by the Platform devices
	auto in1_h = alpaka::allocMappedBuf<Platform, int, uint32_t>(host, Vec1D{size1});
	auto in2_h = alpaka::allocMappedBuf<Platform, int, uint32_t>(host, Vec1D{size2});
	auto out_h = alpaka::allocMappedBuf<Platform, int, uint32_t>(host, Vec1D{size3});
	

	// fill the input buffers with random data, and the output buffer with zeros
	for (size_t i = 0; i < size1; ++i) {
		in1_h[i] = rand();
	}

	for (size_t i = 0; i < size2; ++i) {
		in2_h[i] = rand();
	}

	for (size_t i = 0; i < size3; ++i) {
		out_h[i] = 0;
	}


	/*// print host buffer 1
	std::cout<<"\nhost 1: \n";
	for(auto r = 0; r < rows1; r++){
		for(auto c = 0; c < cols1; c++){
			int idx = r*cols1 + c;
			std::cout<<in1_h[idx]<<" ";
		}
		std::cout<<std::endl;
	}

	// print host buffer 2
	std::cout<<"\nhost 2: \n";
	for(auto r = 0; r < rows2; r++){
		for(auto c = 0; c < cols2; c++){
			int idx = r*cols2 + c;	
			std::cout<<in2_h[idx]<<" ";
		}
		std::cout<<std::endl;
	}
	*/
	
	// run the test the given device
	auto queue = Queue{device};

	// start memory clock
	auto start_mem_pre = std::chrono::high_resolution_clock::now();
	
	// allocate input and output buffers on the device
	auto in1_d = alpaka::allocAsyncBuf<int, uint32_t>(queue, Vec1D{size1});
	auto in2_d = alpaka::allocAsyncBuf<int, uint32_t>(queue, Vec1D{size2});
	auto out_d = alpaka::allocAsyncBuf<int, uint32_t>(queue, Vec1D{size3});

	// copy the input data to the device; the size is known from the buffer objects
	alpaka::memcpy(queue, in1_d, in1_h);
	alpaka::memcpy(queue, in2_d, in2_h);

	// fill the output buffer with zeros; the size is known from the buffer objects
	alpaka::memset(queue, out_d, 0x00);
	alpaka::wait(queue);	// for timing accuracy
	
	// end memory clock
	auto end_mem_pre = std::chrono::high_resolution_clock::now();
	
	// specified at the top instead
	/*
	 * const int blocksX = 4;	// recall that each block resembles a kernel call
	 * const int blocksY = 4;
	 * const int threadsPerBlockX = 8;		// in cpu backend this will be "elements"
	 * const int threadsPerBlockY = 8;
	*/
	// launch the 2-Dimensional kernel
	auto div = make_workdiv<Acc2D>({blocksX, blocksY}, {threadsPerBlockX, threadsPerBlockY});
	std::cout << "\nTesting VectorMultKernel2D with vector indices with a grid of "
		<< alpaka::getWorkDiv<alpaka::Grid, alpaka::Blocks>(div) << " blocks x "
		<< alpaka::getWorkDiv<alpaka::Block, alpaka::Threads>(div) << " threads x "
		<< alpaka::getWorkDiv<alpaka::Thread, alpaka::Elems>(div) << " elements...\n";
	
	auto start_kernel = std::chrono::high_resolution_clock::now();
	alpaka::exec<Acc2D>(
		queue, div, VectorMultKernel2D{}, in1_d.data(), in2_d.data(), out_d.data()
	);
	alpaka::wait(queue);	// for timing accuracy (regardless cpu/gpu backends)
	auto end_kernel = std::chrono::high_resolution_clock::now();
	

	auto start_mem_post = std::chrono::high_resolution_clock::now();
	// copy the results from the device to the host
	alpaka::memcpy(queue, out_h, out_d);
	alpaka::wait(queue);	// for timing accuracy
	auto end_mem_post = std::chrono::high_resolution_clock::now();
	
	// wait for all the operations to complete
	//alpaka::wait(queue);

	auto end = std::chrono::high_resolution_clock::now();
	
	// durations
	auto mem_pre_duration = std::chrono::duration_cast<std::chrono::microseconds>(end_mem_pre - start_mem_pre);
	auto kernel_duration = std::chrono::duration_cast<std::chrono::microseconds>(end_kernel - start_kernel);
	auto mem_post_duration = std::chrono::duration_cast<std::chrono::microseconds>(end_mem_post - start_mem_post);

	// write to file
	std::fstream file;
	std::string accName = getAccName(alpaka::getAccName<Acc2D>());
	auto filename = accName + "_" + std::to_string(rows1) +"x" + std::to_string(cols1)  + "_by_" + std::to_string(rows2) + "x" + std::to_string(cols2) + "_" + std::to_string(threadsPerBlockX) + ".txt";
	file.open(filename, std::ios::app);
	file << mem_pre_duration.count() << " " << kernel_duration.count() << " " << mem_post_duration.count() << "\n";
	file.close();

	
	// verify the results	
	verify(in1_h, in2_h, out_h); 

	/*// print Results
	std::cout<<"\nResult: \n";
	for(auto r = 0; r < rows1; r++){
		for(auto c = 0; c < cols1; c++){
			int idx = r*cols1 + c;
			std::cout<<out_h[idx]<<" ";
		}
		std::cout<<std::endl;
	}
	*/

}

int main() {
	// require at least one device
	std::size_t n = alpaka::getDevCount<Platform>();
	if (n == 0) {
		exit(EXIT_FAILURE);
	}

	// use the single host device
	Host host = alpaka::getDevByIdx<HostPlatform>(0u);
	std::cout << "Host:   " << alpaka::getName(host) << '\n';

	// use the first device
	Device device = alpaka::getDevByIdx<Platform>(0u);
	std::cout << "Device: " << alpaka::getName(device) << '\n';

	if(cols1 != rows2){
		printf("Multiplication not possible for %dx%d X %dx%d \n", rows1, cols1, rows2, cols2);
		return -1;
	}

	testVectorMultKernel2D(host, device);

	return 0;
}
