# Compiling on Windows

This page describes native compilation on Windows.
For the general prerequisites and source code instructions, see [Compile the Application](../Compile.md).

## Visual Studio

This is highly tailored to my own machine.
Thus, it is not recommended to use it directly.
Instead, use VS Code with CMake extension to automatically configure the project.

A solution file is provided under `MSVC/suanPan` folder.
There are two configurations:

1.  `Debug`: Assumes no available Fortran compiler; all Fortran related libraries are provided as precompiled DLLs.
    Use OpenBLAS for linear algebra.
    Multithreading disabled.
    Visualisation disabled.
    HDF5 support disabled.
2.  `Release`: Fortran libraries are configured with Intel compilers.
    Use MKL for linear algebra.
    Multithreading enabled.
    Visualisation enabled with VTK version 9.5.
    HDF5 support enabled.
    CUDA enabled.

This [repository](https://github.com/TLCFEM/prebuilds) contains some precompiled libraries used.

If VTK, Intel oneAPI Toolkit and CUDA are not installed, only the `Debug` configuration can be successfully compiled.
Simply open the solution and switch to Debug configuration, ignore all potential warnings and build the solution.

To compile the `Release` version, please follow these steps.

1.  Make sure both oneAPI Base and HPC toolkits, as well as VS integration, are installed.
    The MKL is enabled via integrated option `<UseInteloneMKL>Parallel</UseInteloneMKL>`.

2.  Make sure CUDA is installed.
    The environment variable `$(CUDA_PATH)` is used to locate headers.

3.  Make sure VTK is available.
    Then define a system environment variable `$(VTK_DIR)`, which points to the root folder of VTK library.
    On my machine, it is

    ```powershell
    VTK_DIR=C:\Program Files\VTK\
    ```

    For versions other than 9.5, names of the linked libraries shall be manually changed as they contain version numbers.
    Thus, it is not a good idea to switch to a different version.
    Precompiled VTK library is also available in this [repository](https://github.com/TLCFEM/prebuilds).

Alternatively, `CMake` can be used to generate solution files if some external packages are not available.

## Visual Studio Code

Open the source code folder with VS Code.
Whether you choose GCC or MSVC, the configuration is done by CMake automatically.
