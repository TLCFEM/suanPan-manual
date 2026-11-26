# Prerequisites

The linear algebra module is implemented by [Armadillo](http://arma.sourceforge.net/docs.html).
It is necessary to learn some basic syntax in order to work with the provided vector and matrix objects.
Armadillo provides complete support for linear algebra computation and has a syntax similar to Matlab.
Users who are familiar with Matlab can easily get started with Armadillo.

New standards (C++11, C++14 and C++17) are utilised to simplify development.
[cppreference](https://en.cppreference.com/w/) provides a complete reference to C++.

## Dependencies

The following third-party libraries are used by `suanPan`, as listed in the project README.
The versions shown are those the project is built and tested against.

- [AMD Optimizing CPU Libraries (AOCL)](https://www.amd.com/en/developer/aocl.html) 5.3
- [ARPACK](https://github.com/opencollab/arpack-ng)
- [Armadillo](http://arma.sourceforge.net/) 15.8.0
- [CUDA](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/) 12.9
- [Catch2](https://github.com/catchorg/Catch2) 3.16.1
- [FEAST](http://www.feast-solver.org/) 4.0
- [HDF5](https://www.hdfgroup.org/solutions/hdf5/) 2.2.0
- [MAGMA](https://icl.utk.edu/magma/) 2.10.0
- [OpenBLAS](https://github.com/xianyi/OpenBLAS) 0.3.34
- [SPIKE](http://www.spike-solver.org/) 1.0
- [SuperLU MT](https://portal.nersc.gov/project/sparse/superlu/) 4.0.0
- [SuperLU](https://portal.nersc.gov/project/sparse/superlu/) 7.0.1
- [TBB](https://github.com/oneapi-src/oneTBB) 2023.1.0
- [VTK](https://vtk.org/) 9.7.2
- [argparse](https://github.com/p-ranav/argparse)
- [cpp-linenoise](https://github.com/yhirose/cpp-linenoise)
- [exprtk](https://github.com/ArashPartow/exprtk) 0.0.3
- [ezp](https://github.com/TLCFEM/ezp)
- [fmt](https://github.com/fmtlib/fmt) 12.2.1
- [magic_enum](https://github.com/Neargye/magic_enum) 0.10.0
- [oneMKL](https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onemkl.html) 2026.2.0
- [whereami](https://github.com/gpakosz/whereami)
- `thread_pool`, an abridged version of [`thread-pool`](https://github.com/bshoshany/thread-pool)

Only 64-bit builds are provided and AVX2 support is assumed by default.
GPU-based solvers additionally require CUDA and/or MAGMA.

