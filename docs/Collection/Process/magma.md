# magma

The [MAGMA](https://icl.utk.edu/magma/) library provides many algorithms for solving sparse linear systems on GPUs.
To enable the MAGMA solver, a valid CUDA installation must be present.
The application should be compiled with the `-DSP_ENABLE_CUDA=ON` and `-DSP_ENABLE_MAGMA=ON` options.

## Compiling MAGMA

Refer to the MAGMA documentation for compilation instructions.
On Windows, the following options are used, tailored for one specific platform:

```json
{
  "cmake.configureSettings": {
    "LAPACK_LIBRARIES": [
      "C:/Program Files (x86)/Intel/oneAPI/mkl/2023.0.0/lib/intel64/mkl_intel_lp64.lib",
      "C:/Program Files (x86)/Intel/oneAPI/mkl/2023.0.0/lib/intel64/mkl_intel_thread.lib",
      "C:/Program Files (x86)/Intel/oneAPI/mkl/2023.0.0/lib/intel64/mkl_core.lib",
      "C:/Program Files (x86)/Intel/oneAPI/compiler/2023.0.0/windows/compiler/lib/intel64_win/libiomp5md.lib"
    ],
    "MKL_ROOT": "C:/Program Files (x86)/Intel/oneAPI/mkl/2023.0.0/",
    "GPU_TARGET": "Turing",
    "FORTRAN_CONVENTION": "-DADD_",
    "CMAKE_INSTALL_PREFIX": "magma-build"
  }
}
```

## Compiling `suanPan`

Once MAGMA is compiled, the application should be compiled with the `-DSP_ENABLE_CUDA=ON` and `-DSP_ENABLE_MAGMA=ON` options.
An additional path must be set to the MAGMA installation directory.

```json
{
  "cmake.configureSettings": {
    "SP_ENABLE_CUDA": "ON",
    "SP_ENABLE_MAGMA": "ON",
    "MAGMA_PATH": "magma/installation/root"
  }
}
```

The following files must be present: `${MAGMA_PATH}/include/magma.h`, `${MAGMA_PATH}/lib/libmagma.a`
and `${MAGMA_PATH}/lib/libmagma_sparse.a`.

## Using MAGMA Solver

With MAGMA enabled, use the following to select the MAGMA solver:

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
| `--atol`      | positive floating-point number                                                              |
| `--rtol`      | positive floating-point number                                                              |
| `--maxiter`   | positive integer                                                                            |
| `--verbose`   | `0` or `1`                                                                                  |
| `--prestart`  | positive integer                                                                            |
| `--patol`     | positive floating-point number                                                                 |
| `--prtol`     | positive floating-point number                                                                 |
| `--piters`    | positive integer                                                                            |
| `--ppattern`  | positive integer                                                                            |
| `--psweeps`   | positive integer                                                                            |
| `--plevels`   | positive integer                                                                            |

Note that not all iterative solvers are stable and applicable on every system.
