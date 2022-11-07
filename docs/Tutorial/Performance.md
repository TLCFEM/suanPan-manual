# Performance Considerations

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

Nevertheless, experience has shown that the performance is generally good enough and for most cases. Users are 
encouraged to `perf` the performance of various analysis types.

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
