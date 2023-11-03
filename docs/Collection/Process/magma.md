# magma

The [MAGMA](https://icl.utk.edu/magma/) library provides a vast number of algorithms that can be used to solve sparse
linear systems on GPUs. To enable MAGMA solver, the valid CUDA installation must be present. The application should be
compiled with `-DUSE_CUDA=ON` and `-DUSE_MAGMA=ON` options.

## Compiling MAGMA

Please check MAGMA documentation for the compilation instructions. On Windows, the following options are used, tailored
for my specific platform only:

```json
{
  "cmake.configureSettings": {
    "LAPACK_LIBRARIES": [
      "C:/Program Files (x86)/Intel/oneAPI/mkl/2023.0.0/lib/intel64/mkl_intel_lp64.lib",
      "C:/Program Files (x86)/Intel/oneAPI/mkl/2023.0.0/lib/intel64/mkl_intel_thread.lib",
      "C:/Program Files (x86)/Intel/oneAPI/mkl/2023.0.0/lib/intel64/mkl_core.lib",
      "C:/Program Files (x86)/Intel/oneAPI/compiler/2023.0.0/windows/compiler/lib/intel64_win/libiomp5md.lib"
    ],
    "MKLROOT": "C:/Program Files (x86)/Intel/oneAPI/mkl/2023.0.0/",
    "GPU_TARGET": "Turing",
    "FORTRAN_CONVENTION": "-DADD_",
    "CMAKE_INSTALL_PREFIX": "magma-build"
  }
}
```

## Compiling `suanPan`

Once MAGMA is compiled, the application should be compiled with `-DUSE_CUDA=ON` and `-DUSE_MAGMA=ON` options.
An additional path shall be set to the MAGMA installation directory.

```json
{
  "cmake.configureSettings": {
    "USE_CUDA": "ON",
    "USE_MAGMA": "ON",
    "MAGMAROOT": "magma/installation/root"
  }
}
```

The following files shall be present: `${MAGMAROOT}/include/magma.h`, `${MAGMAROOT}/lib/libmagma.a`
and `${MAGMAROOT}/lib/libmagma_sparse.a`.

## Using MAGMA Solver

With MAGMA enabled, one can use the following to enable MAGMA solver:

```text
set sparse_mat true
set system_solver magma [(key value)...] 
```

The following key-value options are available to customise the solver:

| key           | value                                                                                       |
|---------------|---------------------------------------------------------------------------------------------|
| `--mscale`    | `NOSCALE`, `UNITDIAG`, `UNITROW`, `UNITCOL`, `UNITDIAGCOL`, `UNITROWCOL`                    |
| `--solver`    | `CG`, `PCG`, `BICG`, `PBICG`, `BICGSTAB`, `PBICGSTAB`, `QMR`, `PQMR`, `TFQMR`, `PTFQMR`     |
|               | `GMRES`, `PGMRES`, `LOBPCG`, `LSQR`, `JACOBI`, `BA`, `BAO`, `IDR`, `PIDR`, `CGS`, `PCGS`    |
|               | `BOMBARDMENT`, `ITERREF`, `PARDISO`                                                         |
| `--precond`   | `CG`, `PCG`, `BICGSTAB`, `QMR`, `TFQMR`, `PTFQMR`, `GMRES`, `PGMRES`, `LOBPCG`              |
|               | `JACOBI`, `BA`, `BAO`, `IDR`, `PIDR`, `CGS`, `PCGS`, `BOMBARDMENT`, `ITERREF`, `ILU`        |
|               | `IC`, `ILUT`, `ICT`, `PARILU`, `AIC`, `PARIC`, `PARICT`, `PARILUT`, `CUSTOMIC`, `CUSTOMILU` |
|               | `ISAI`, `NONE`                                                                              |
| `--trisolver` | `CG`, `BICGSTAB`, `QMR`, `TFQMR`, `GMRES`, `JACOBI`, `VBJACOBI`                             |
|               | `BA`, `BAO`, `IDR`, `CGS`, `CUSOLVE`, `SYNCFREESOLVE`, `ISAI`, `NONE`                       |
| `--basic`     | `0` or `1`                                                                                  |
| `--blocksize` | positive integer                                                                            |
| `--alignment` | positive integer                                                                            |
| `--restart`   | positive integer                                                                            |
| `--atol`      | positive float-point number                                                                 |
| `--rtol`      | positive float-point number                                                                 |
| `--maxiter`   | positive integer                                                                            |
| `--verbose`   | `0` or `1`                                                                                  |
| `--prestart`  | positive integer                                                                            |
| `--patol`     | positive float-point number                                                                 |
| `--prtol`     | positive float-point number                                                                 |
| `--piters`    | positive integer                                                                            |
| `--ppattern`  | positive integer                                                                            |
| `--psweeps`   | positive integer                                                                            |
| `--plevels`   | positive integer                                                                            |

One shall note that depending on the different systems, not all iterative solvers are stable and applicable.
