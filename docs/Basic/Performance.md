# Performance

`suanPan` prioritizes performance and designs the analysis logic in a parallel context.

Although the majority of the common analysis types can be parallelized, there are still some certain parts that have 
strong data dependencies that cannot be parallelized.
According to [Amdahl's law](https://en.wikipedia.org/wiki/Amdahl%27s_law), there would be an upper bound of the 
theoretical speedup.

For example, for a static analysis of a simple model with a sufficiently large number of elements, there is no local 
iteration required to update element status, the major tasks are to assemble global stiffness matrix and solve it. 
In such a case, the performance is likely governed by the CPU capacity and often a large value of GFLOPS can be 
achieved (close to practical limit).

However, if one choose to perform a dynamic analysis of the same model with a fairly sophisticated time integration 
algorithm, such as [GSSSS](../Library/Integrator/GSSSS.md), as the effective stiffness would be the summation of 
the scaled versions of several global matrices, the analysis may be blocked by memory operations, which eventually 
leads to a lower value of GFLOPS.

In the nonlinear context, it is even more complicated. Several additional factors, such as the complexity of the 
material models used, the use of constraints, the element type, can all affect the performance.

Nevertheless, experience has shown that the performance is generally good enough for most cases.
Users are encouraged to `perf` the performance of various analysis types.

## Analysis Configurations

Here are some tips that may improve the performance.

1. If the analysis is known to be linear elastic, use `set linear_system true` to skip convergence test and iteration.
   Note the analysis should be both material and geometric linear.
2. If the global system is known to be symmetric, use `set symm_mat true` to use a symmetric storage.
   Analyses involving 1D materials are mostly (**_not always_**) symmetric.
   Analyses involving 2D and 3D materials are mostly (**_not always_**) **_not_** symmetric.
3. Consider a proper stepping strategy. A fixed stepping size may be unnecessarily expensive.
   A proper adaptive stepping strategy can significantly improve the performance.
4. Prefer a dense solver over a sparse solver if the system is small.
   A dense solver is generally faster than a sparse solver for small systems.
5. Prefer a mixed-precision algorithm `set precision mixed` over a full-precision algorithm if the system is large.
   A mixed-precision algorithm is generally faster than a full-precision algorithm for large systems.
   See following for details.
6. The performance of various sparser solver can vary significantly.
   It is recommended to try different solvers to find the best one.

## Mixed-Precision Algorithm

On some platforms, the performance of the mixed-precision algorithm can be significantly better than the full-precision
algorithm.
The mixed-precision algorithm converts the full-precision matrix to a lower precision matrix, and then solves the system
using the lower precision matrix.
Typically, only two to three iterations are required as each iteration reduces the relative error by a factor around
machine epsilon of the lower precision.

The built-in tests consist of benchmarks for mixed-precision algorithms.
One can execute the following command to run the tests.

```bash
suanpan -ctest
```

One can find the following information.

```text
-------------------------------------------------------------------------------
Large Mixed Precision
-------------------------------------------------------------------------------

benchmark name                       samples       iterations    est run time
                                     mean          low mean      high mean
                                     std dev       low std dev   high std dev
-------------------------------------------------------------------------------
Band N=1024 NZ=3234 NE=10240 Full              100             1    39.4709 ms
                                        423.471 us    409.755 us    449.776 us
                                        93.2939 us     56.394 us    148.874 us

Band N=1024 NZ=3234 NE=10240 Mixed             100             1    11.4429 ms
                                        156.697 us    147.096 us    166.771 us
                                        50.2275 us    47.5325 us    54.2532 us
```

The mixed-precision algorithm is around three times faster than the full-precision algorithm.
Note the results are obtained with MKL on a platform with a 13-th generation Intel CPU.
For platforms that have a slow memory bandwidth, the performance gain may not be as significant.

One could always benchmark the platform to find the best algorithm.

## Tweaks

It is possible to tweak the performance in the following ways, which may or may not improve the performance.

### OpenMP Threads

OpenMP is used by MKL and OpenBLAS to parallelize the matrix operations, alongside with SIMD instructions. It is 
possible to manually set [OMP_NUM_THREADS](https://www.google.com/search?q=omp_num_threads) to control the number of 
threads used. Pay attention to over-subscription.

[OMP_DYNAMIC](https://www.google.com/search?q=omp_dynamic) may affect cache locality and thus the performance. For 
computation intensive tasks, it is recommended to set it to false.

### Affinity

CPU affinity can also affect the performance.
Tweaking affinity, for example, with [KMP_AFFINITY](https://www.google.com/search?q=KMP_AFFINITY), can improve 
performance.

### Memory Allocation

Memory fragmentation may downgrade analysis performance, especially for finite element analysis, in which there are 
a large number of small matrices and vectors. It is recommended to use a performant memory allocator, for example, a 
general purpose allocator like [mimalloc](https://github.com/microsoft/mimalloc).

On Linux, it is fairly easy to replace the default memory allocator. For example,

```bash
LD_PRELOAD=/path/to/libmimalloc.so  suanpan -f input.sp
```
