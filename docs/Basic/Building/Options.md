# Build Options and Customisation

This page documents the main CMake options and customisation details.
For the general compilation guide, see [Compile the Application](Compile.md).

## Linear Algebra Driver

Any standard BLAS and LAPACK implementation can be used as the linear algebra driver which the application itself and `Armadillo` rely on.
Currently, the following are supported and tested.

1. [`OpenBLAS`](http://www.openmathlib.org/OpenBLAS/)
2. [`Intel oneAPI MKL`](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html)
3. [`AMD Optimizing CPU Libraries (AOCL)`](https://www.amd.com/en/developer/aocl.html)

As a general guideline, when it comes to choosing a proper implementation, the following points shall be considered.

1. From my very personal experience, `OpenBLAS` is okay for small matrices on a few cores, but could be slow when the size hits some threshold.
   This is also seen in this [benchmark](https://github.com/flame/blis/blob/master/docs/Performance.md).
2. `Intel oneAPI MKL` is exclusively optimised for Intel CPUs, and may throttle on other platforms.
   This [benchmark](https://github.com/flame/blis/blob/master/docs/Performance.md) shows clear differences on AMD platforms.
3. `AMD Optimizing CPU Libraries (AOCL)` is optimised for AMD CPUs based on `BLIS` and `FLAME` libraries; its performance on both platforms (and others) is superb.

Thus, use `Intel oneAPI MKL` if it is preferred or an Intel platform is targeted.
The downside is that `Intel oneAPI MKL` is proprietary and the final binary may have a large size.
For other cases, use `AMD Optimizing CPU Libraries (AOCL)` when possible.
The downside is that it may need manual compilation of the libraries for the target OS.
`OpenBLAS` shall be deemed as the last resort and the usage is discouraged as of writing.

## Build Options

If CMake GUI is used to configure the project, the following options are available.

1. `BUILD_SHARED_LIBS`: If enabled, all libraries will be built as shared libraries.
2. `SP_BUILD_DLL_EXAMPLE`: If enabled, example element/material/section implemented as external libraries will be built.
   This is not required for the successful build of the main application.
3. `SP_BUILD_PARALLEL`: If enabled, `TBB` will be used for multithreading so that element update, global matrix assembly, etc., can be parallelized.
   `OpenMP` is not controlled by this option given that `OpenMP` support is available in major platforms.
   It will be used for low level parallelization such as linear algebra operations (which is controlled by `Armadillo`), matrix solving (which is controlled by various solvers).
   Thus, this flag only controls the `suanPan` application itself.
4. `SP_ENABLE_HDF5`: If enabled, `HDF5` will be used to provide support for [`hdf5recorder`](../../Library/Recorder/Recorder.md).
5. `SP_ENABLE_VTK`: If enabled, `VTK` will be used to provide support for visualization.
   It will be useful to generate files that can be used in `Paraview` for post-processing.
   If enabled, `VTK_PATH` needs to be set to the path of `VTK` installation.
   For example, `VTK_PATH=/usr/local/opt/vtk/lib/cmake/vtk-9.1`.
6. `SP_ENABLE_CUDA`: `CUDA` needs to be installed manually by the user.
   If enabled, `CUDA` based solvers will be available.
   However, for dense matrix storage, only full matrix storage scheme is supported by `CUDA`.
   Note full matrix storage scheme is not favourable for FEM.
   It can, however, be used for sparse matrix solving and mixed precision solving.
7. `SP_ENABLE_MAGMA`: `MAGMA` needs to be installed manually by the user.
   If enabled, `MAGMA` based solvers will be available.
   The variable `MAGMA_PATH` needs to be set to find necessary files.
8. `SP_ENABLE_ASAN`: If enabled, address sanitizer will be enabled.
   This is useful for debugging purposes.
9.  `SP_ENABLE_CODECOV`: If enabled, compile options will be enabled to support code coverage report.
10. `SP_ENABLE_AVX`: If enabled, compiler flags `-mavx` or `/arch:AVX` will be used. (~2011)
11. `SP_ENABLE_AVX2`: If enabled, compiler flags `-mavx2` or `/arch:AVX2` will be used. (~2013)
12. `SP_ENABLE_AVX512`: If enabled, compiler flags `-mavx512f` or `/arch:AVX512` will be used. (~2016)
13. `SP_ENABLE_TBB_ALLOC`: If enabled, the TBB's memory allocator will be used.
14. `SP_OPENBLAS_PATH`: If assigned, link the designated `OpenBLAS` library, otherwise the bundled version will be used.
15. `SP_ENABLE_AOCL`: If enabled, one can use the `AOCL` implementation via assigning library path `SP_AOCL_PATH`.
16. `SP_ENABLE_MKL`: `MKL` needs to be installed manually by the user.
    If enabled, `MKL` will be used for linear algebra operations.
    If `SP_ENABLE_MKL` is enabled, set `MKL_PATH` to the root directory of `MKL` installation.
    For example, `C:/Program Files (x86)/Intel/oneAPI/mkl/latest` or `/opt/intel/oneapi/mkl/latest`, also the following additional options are available.
17. `SP_ENABLE_SHARED_MKL`: If enabled, dynamically linked `MKL` libraries will be used.
    Otherwise, statically linked `MKL` libraries will be used, leading to larger binary size but faster execution and fewer dependencies.
18. `SP_ENABLE_IOMP`: If enabled, Intel's OpenMP implementation will be used.
    Otherwise, Default ones (such as GNU OpenMP library) will be used.
19. `SP_ENABLE_MPI`: Enables cluster support via MPI.
20. `SP_ENABLE_64BIT_INDEXING`: Enables 64-bit integer for matrix indexing.

!!! warning "multiple runtimes"
    The `SP_ENABLE_IOMP` should be switched on/off based on the compilers used.
    In principle, there should be only one implementation of OpenMP.
    Thus, if the compilers used are `gcc/g++/gfortran`, `SP_ENABLE_IOMP=OFF`.
    If the compilers are `icx/icpx/ifx`, `SP_ENABLE_IOMP=ON`.
    The `Spike` solver also does not support mixing OpenMP implementations.
    Use with caution if two OpenMP implementations exist.

## Example Configuration

The following command is used to compile the program to be distributed via snap.
See this [file](https://github.com/TLCFEM/suanPan/blob/dev/snapcraft.yaml).

```bash
# assume current folder is suanPan/build
# the parent folder contains source code
cmake -DCMAKE_INSTALL_PREFIX= \
      -DCMAKE_BUILD_TYPE=Release \
      -DMKL_PATH=/opt/intel/oneapi/mkl/latest \
      -DSP_BUILD_PARALLEL=ON \
      -DSP_ENABLE_HDF5=ON \
      -DSP_ENABLE_IOMP=OFF \
      -DSP_ENABLE_MKL=ON \
      -DSP_ENABLE_SHARED_MKL=OFF \
      -DSP_ENABLE_VTK=ON \
      -DVTK_PATH=$CRAFT_PART_BUILD/lib/cmake/vtk-9.4/
```

## `aarch64` Architecture

The `aarch64` architecture is supported by the source code.
But one shall prepare the dependencies manually.
As MKL is not available for `aarch64`, one shall use `OpenBLAS` or `AOCL` only.

`OpenBLAS` is the only necessary dependency.
All other dependencies are optional.

To use `AOCL`, one shall manually compile the `blis` and `flame` libraries in advance.

## 64-bit Indexing

The FEM framework part itself uses `unsigned` 32-bit integer for indexing; this means it supports up to 4 billion objects, for example, nodes and elements.
This is sufficient at least for the coming years.
But the linear algebra driver may quickly hit the size limit.
For [`lp64`](https://en.wikipedia.org/wiki/64-bit_computing#64-bit_data_models) builds, the indexing capability of a default Fortran integer is around 2 billion.
If the problem is large enough, the global matrix may have more than 2 billion entries (either dense or sparse storage).
In this case, it is necessary to use 64-bit indexing; see the [`ilp64`](https://en.wikipedia.org/wiki/64-bit_computing#64-bit_data_models) model.

To do so, compile the application with the flag `-DSP_ENABLE_64BIT_INDEXING=ON`.

!!! note
    The bundled `OpenBLAS` binaries are built for `lp64` only.
    If one decides to use `OpenBLAS`, an `ilp64` version must be provided via `SP_OPENBLAS_PATH`.

!!! note
    If `SP_ENABLE_MPI=ON` is also enabled, one shall make sure the linked MPI is also compiled with 64-bit integer support.
    [MPICH](https://www.mpich.org/) is known to work well with either 32-bit or 64-bit integer size.

`MKL` provides both versions for `lp64` and `ilp64`; `CMake` will handle the linkage automatically.

Continue with [Build the Manual](Build.md).
