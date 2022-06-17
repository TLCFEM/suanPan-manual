# benchmark

The `benchmark` command can be used to benchmark the platform to provide a performance baseline.

The routine preallocates a square matrix of size 5120 and repeatedly solves it for 50 times. Unlike other approaches
that normally rely on `dgemm` subroutine, here `dgesv` subroutine is used as for FEM, the main operations are solving 
matrices rather than multiplying matrices.

## Syntax

```text
benchmark
```

## Notes

The basic idea of the benchmark resembles that of [linpack](http://www.netlib.org/utk/people/JackDongarra/faq-linpack.html),
but it is not intended to be as versatile as linpack. Thus, it does not provide any configurable options.

The theoretical maximum GFLOPS is not often achievable in practical applications. Modern hardware is often bounded 
by other factors such as memory bandwidth.

One can `perf` this benchmark to reveal the GFLOPS, for example,

```bash
echo "benchmark" >>b
echo "exit" >>b
perf stat -e fp_arith_inst_retired.128b_packed_double,fp_arith_inst_retired.256b_packed_double,fp_arith_inst_retired.512b_packed_double,fp_arith_inst_retired.scalar_double suanpan -f b
```

The corresponding result is

```text
+--------------------------------------------------+
|   __        __         suanPan is an open source |
|  /  \      |  \           FEM framework (64-bit) |
|  \__       |__/  __   __      Betelgeuse (2.4.0) |
|     \ |  | |    |  \ |  |      by tlc @ b3918adf |
|  \__/ |__| |    |__X |  |    all rights reserved |
|                           10.5281/zenodo.1285221 |
+--------------------------------------------------+
|  🧮 https://github.com/TLCFEM/suanPan            |
|  📚 https://github.com/TLCFEM/suanPan-manual     |
+--------------------------------------------------+
|  🔋 https://gitter.im/suanPan-dev/community      |
+--------------------------------------------------+

[==================================================]
Current platform rates (higher is better): 25.58.

Time Wasted: 39.3980 Seconds.

 Performance counter stats for 'suanpan -f b':

        17,075,053      fp_arith_inst_retired.128b_packed_double                                   
         3,849,289      fp_arith_inst_retired.256b_packed_double                                   
   563,539,901,688      fp_arith_inst_retired.512b_packed_double                                   
       122,202,329      fp_arith_inst_retired.scalar_double                                   

      39.428329959 seconds time elapsed

     130.321384000 seconds user
       3.369368000 seconds sys
```

This roughly gives 114 GFLOPS, which is around $$60\%$$ of the [theoretical](https://www.intel.com/content/dam/support/us/en/documents/processors/APP-for-Intel-Core-Processors.pdf)
maximum GFLOPS of a `i7-1185G7` processor. Of course, the actual performance depends on many other factors. Here the 
numbers are indicative. A rate of $$2n$$ means the platform is two times faster than a rate of $$n$$.

The practical FEM involves other processes such as updating elemental stiffness (small matrix manipulations) and 
assembling global stiffness (random memory accesses). As the result, the performance of analysis would further be a 
fraction of GFLOPS of this benchmark test.
