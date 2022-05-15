# Compile

## Prerequisites

1. To configure the source code, [CMake](https://cmake.org/download/) shall be available. Please download and install it
   before configuring the source code package.
2. The linear algebra driver used is [OpenBLAS](https://github.com/xianyi/OpenBLAS). You may want to compile it with the
   optimal configuration based on the specific machine. Otherwise, precompiled binaries (dynamic platform) are available
   in this [repository](https://github.com/TLCFEM/prebuilds).
3. It is strongly recommended installing Intel MKL for potentially better performance.
4. Please be aware that MKL is throttled on AMD platforms. Performance comparisons can be seen for
   example [here](https://github.com/flame/blis/blob/master/docs/Performance.md). If you have AMD CPUs please collect
   more knowledge to determine which linear algebra library is more suitable.

## Toolsets

A number of new features from new standards are utilized. To compile the binary, a compiler that supports **C++20** is
required.

GCC 10, Clang 13, MSVC 14.3 and Intel compilers are tested with the source code.

On Windows, Visual Studio 2022 with Intel oneAPI toolkit is recommended. Alternatively, [WinLibs](http://winlibs.com/)
can be used if GCC compilers are preferred.

On other platforms (Linux and macOS), simply use GCC (at least version 10.3.0) which comes with a valid Fortran
compiler. Clang can also be used for C/CPP code, but since Clang and GCC have different supports for C++20, successful
compilation is not guaranteed with Clang.

## Obtain Source Code

Download the source code archive from GitHub [Releases](https://github.com/TLCFEM/suanPan/releases) or the
latest [code](https://github.com/TLCFEM/suanPan/archive/master.zip).

## Configure and Compile

The manual compilation is not difficult in general. The CI/CD configuration files can be referred to if you wish. Please
check [this](https://github.com/TLCFEM/suanPan/tree/dev/.github/workflows) page. Here some general guidelines are given.

### Visual Studio

A solution file is provided under `MSVC/suanPan` folder. There are two configurations:

1. `Debug`: Assume no available Fortran compiler, all Fortran related libraries are provided as precompiled DLLs. Use
   OpenBLAS for linear algebra. Multithreading disabled. Visualisation disabled. HDF5 support disabled.
2. `Release`: Fortran libraries are configured with Intel compilers. Use MKL for linear algebra. Multithreading enabled.
   Visualisation enabled with VTK version 9.1. HDF5 support enabled. CUDA enabled.

This [repository](https://github.com/TLCFEM/prebuilds) contains some precompiled libraries used.

If Intel oneAPI Toolkit and CUDA are not installed, only the `Debug` configuration can be successfully compiled. Simply
open the solution and switch to Debug configuration, ignore all potential warnings and build the solution.

To compile `Release` version, please

1. Make sure oneAPI both base and HPC toolkits, as well as VS 2022 integration, are installed. The MKL is enabled via
   integrated option `<UseInteloneMKL>Parallel</UseInteloneMKL>`.

2. Make sure CUDA is installed. The environment variable `$(CUDA_PATH)` is used to locate headers.

3. Make sure VTK is available. Then define two system environment variables `$(VTK_INC)` and `$(VTK_LIB)`, which point
   to
   include and library folders. On my machine, they are

   ```powershell
   VTK_INC=C:\Program Files\VTK\include\vtk-9.1
   VTK_LIB=C:\Program Files\VTK\lib
   ```

   For versions other than 9.1, names of the linked libraries shall be manually changed as they contain version numbers.
   Thus, it is not a good idea to switch to a different version. Precompiled VTK library is also available in
   this [repository](https://github.com/TLCFEM/prebuilds)

Alternatively, `CMake` can be used to generate solution files if some external packages are not available.

### Ubuntu

The following instructions are based on Ubuntu 20.04. [CMake](https://cmake.org/) is used to manage builds. It is
recommended
to use **CMake** GUI if appropriate.

1. Install necessary tools.

   ```bash
   sudo apt-get install gcc-10 g++-10 gfortran-10 git cmake libomp5 -y
   ```

2. Clone the project.

   ```bash
   git clone -b master https://github.com/TLCFEM/suanPan.git
   ```

3. Create build folder and configure via CMake. The default configuration disables parallelism `-DBUILD_MULTITHREAD=OFF`
   and enables HDF5 via bundled library `-DUSE_HDF5=ON`. Please check [`Option.cmake`](https://github.com/TLCFEM/suanPan/blob/dev/Option.cmake) file or use GUI for available
   options.

   ```bash
   cd suanPan && mkdir build && cd build
   cmake ../
   ```

4. Invoke `make`.

   ```bash
   make -j4
   ```

Check the following recording.

[![asciicast](https://asciinema.org/a/418406.svg)](https://asciinema.org/a/418406)

#### Install VTK

Ubuntu official repository does not (Fedora does!) contain the latest VTK library. It's better to compile it manually.

1. Install OpenGL first, as well as compilers if necessary.

   ```bash
   sudo apt install gcc-10 g++-10 gfortran-10 libglu1-mesa-dev freeglut3-dev mesa-common-dev libglvnd-dev
   ```

2. Obtain VTK source code and unpack.

   ```bash
   wget https://www.vtk.org/files/release/9.1/VTK-9.1.0.tar.gz
   tar -xf VTK-9.1.0.tar.gz
   ```

3. Create folder for building VTK.

   ```bash
   mkdir VTK-build && cd VTK-build
   ```

4. Configure and compile VTK library. If necessary, installation destination can be modified. Here static libraries are
   built.

   ```bash
   cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=../VTK-out ../VTK-9.1.0
   make install -j4
   ```

5. Now obtain `suanPan` source code and unpack it. To configure it with VTK support, users may use the following
   flag `-DUSE_EXTERNAL_VTK=ON`. If `FindVTK` is presented and `VTK` is installed to default location, there is no need
   to provide the variable `VTK_DIR`, otherwise point it to the `lib/cmake/vtk-9.1` folder.

#### Install MKL

The provided CMake configuration covers both `oneMKL` and `Intel MKL 2020`. Please note MKL is included in oneAPI
toolkit starting from 2021, which has a different folder structure compared to Intel Parallel Studio.

The following guide is a manual installation is based on Ubuntu terminal using the official repository.
See [this page](https://www.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-linux/top/installation/install-using-package-managers/apt.html)
for details.

1. Add repository. To summarise,

   ```bash
   wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
   sudo apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
   echo "deb https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list 
   ```

2. Install the package.

   ```bash
   sudo apt update && sudo apt install intel-oneapi-mkl-devel -y
   ```

3. Now compile `suanPan` by enabling MKL via option `-DUSE_MKL=ON`. The corresponding `MKLROOT` shall be assigned, for
   example `-DMKLROOT=/opt/intel/oneapi/mkl/latest/`, depending on the installation location. The
   configuration used for snap is the following one.

   ```bash
   -DCMAKE_BUILD_TYPE=Release \
   -DBUILD_MULTITHREAD=ON \
   -DUSE_HDF5=ON \
   -DUSE_EXTERNAL_VTK=ON \
   -DVTK_DIR=$SNAPCRAFT_PART_BUILD/lib/cmake/vtk-9.1/ \
   -DUSE_MKL=ON \
   -DMKLROOT=/opt/intel/oneapi/mkl/latest \
   -DUSE_INTEL_OPENMP=OFF \
   -DLINK_DYNAMIC_MKL=OFF
   ```

### Fedora

#### VTK

Fedora offers the latest VTK library, simply install it.

```bash
sudo dnf install vtk-devel
```

#### MKL

Intel also provides a repository to install MKL via `dnf`.
See [this page](https://www.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-linux/top/installation/install-using-package-managers/yum-dnf-zypper.html)
for details.

First, create the `repo` file.

```bash
tee > /tmp/oneAPI.repo << EOF
[oneAPI]
name=Intel® oneAPI repository
baseurl=https://yum.repos.intel.com/oneapi
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://yum.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
EOF
```

Move it to the proper location.

```bash
sudo mv /tmp/oneAPI.repo /etc/yum.repos.d
```

Install MKL. You may perform a search `sudo dnf search intel-oneapi-mkl-devel` to find which package name is available
and install the specific version if necessary.

```bash
sudo dnf install intel-oneapi-mkl-devel
```

The source can be compiled with VTK and MKL enabled.

### macOS

The following guide is based on macOS Big Sur (11).

Install tools. `gfortran`, `llvm` and `libomp` are used for compiling the main program, `glfw` and `glew` are required
for compiling `VTK`. `VTK` does not compile with `GCC`. Here, we use `Clang`.

```bash
# install brew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# install necessary packages
brew install gcc@10 llvm@13 libomp glfw glew git cmake
```

Similar to Ubuntu, compile `VTK` if wanted.

```bash
wget https://www.vtk.org/files/release/9.1/VTK-9.1.0.tar.gz
tar xf VTK-9.1.0.tar.gz && rm VTK-9.1.0.tar.gz
mkdir VTK-build && cd VTK-build
cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=../VTK-out ../VTK-9.1.0
make install -j4
```

`MKL` can be installed if necessary. See
this [page](https://software.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-macos/top.html)
.

Obtain the source code and configure.

```bash
# clone source code
git clone -b master https://github.com/TLCFEM/suanPan.git
# create build directory
mkdir suanpan-build && cd suanpan-build
# use clang, clang++ and gfortran
export CC=/usr/local/opt/llvm/bin/clang && export CXX=/usr/local/opt/llvm/bin/clang++ && export FC=gfortran-10
# configure project
cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_MULTITHREAD=ON -DUSE_HDF5=ON -DUSE_EXTERNAL_VTK=ON -DVTK_DIR=../VTK-out/lib/cmake/vtk-9.1/ .
# compile
make -j4
```

### Build Options

If CMake GUI is used to configure the project, the following options are available.

1. `BUILD_DLL_EXAMPLE`: If enabled, example element/material/section implemented as external libraries will be built.
2. `BUILD_MULTITHREAD`: If enabled, `TBB` will be used for multithreading so that element update, global matrix
   assembly, etc., can be parallelized. `OpenMP` is not controlled by this option given that `OpenMP` support is
   available in major platforms. It will be used for low level parallelization such as linear algebra operations (
   controlled by `Armadillo`), matrix solving (controlled by various solvers).
3. `BUILD_SHARED`: If enabled, all libraries will be built as shared libraries.
4. `USE_SUPERLUMT`: If enabled, `SuperLU-MT` will be used, otherwise `SuperLU` will be used.
5. `USE_HDF5`: If enabled, `HDF5` will be used to provide support for [`hdf5recorder`](../Library/Recorder/Recorder.md).
6. `USE_EXTERNAL_VTK`: If enabled, `VTK` will be used to provide support for visualization. It will be useful to
   generate `.vtk` files that can be used in `Paraview` for post-processing. If enabled, `VTK_DIR` needs to be set to 
   the path of `VTK` installation. For example, `VTK_DIR=/usr/local/opt/vtk/lib/cmake/vtk-9.1`.
7. `USE_EXTERNAL_CUDA`: `CUDA` needs to be installed manually by the user. If enabled, `CUDA` based solvers will be
   available. However, for dense matrix storage, only full matrix storage scheme is supported by `CUDA`. Note full
   matrix storage scheme is not favorable for FEM. It can, however, be used for sparse matrix solving and mixed
   precision solving.
8. `USE_AVX`: If enabled, compiler flags `-mavx` or `/arch:AVX` will be used. (~2011)
9. `USE_AVX2`: If enabled, compiler flags `-mavx2` or `/arch:AVX2` will be used. (~2013)
10. `USE_AVX512`: If enabled, compiler flags `-mavx512f` or `/arch:AVX512` will be used. (~2016)
11. `USE_MKL`: `MKL` needs to be installed manually by the user. If enabled, the parallel version of `MKL` will be used
    for linear algebra operations. It is possible to manually modify the configuration to use cluster version (MPI).
    However, For the moment, the global matrix is still centralized in such a way that element updating will happen on a
    single node. The linear algebra operations may be offloaded to other nodes. If `USE_MKL` is enabled, the following
    additional options are available.

12. `LINK_DYNAMIC_MKL`: If enabled, dynamically linked `MKL` libraries will be used. Otherwise, statically
    linked `MKL` libraries will be used, leading to larger binary size but faster execution and fewer dependencies.
13. `MKLROOT`: Set this path to the root directory of `MKL` installation. For
    example, `C:/Program Files (x86)/Intel/oneAPI/mkl/latest` or `/opt/intel/oneapi/mkl/latest`.
14. `USE_INTEL_OPENMP`: If enabled, Intel OpenMP library will be used. Otherwise, Default ones (such as GNU OpenMP
    library) will be used.

### Example Configuration

The following command is used to compile the program to be distributed via snap. See
this [file](https://github.com/TLCFEM/suanPan/blob/dev/snapcraft.yaml).

```bash
# assume current folder is suanPan/build
# the parent folder contains source code
cmake -DCMAKE_INSTALL_PREFIX= \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_MULTITHREAD=ON \
      -DUSE_HDF5=ON \
      -DUSE_EXTERNAL_VTK=ON \
      -DVTK_DIR=$SNAPCRAFT_PART_BUILD/lib/cmake/vtk-9.1/ \
      -DUSE_MKL=ON \
      -DMKLROOT=/opt/intel/oneapi/mkl/latest \
      -DUSE_INTEL_OPENMP=OFF \
      -DLINK_DYNAMIC_MKL=OFF \
      -DCMAKE_C_COMPILER=gcc-10 \
      -DCMAKE_CXX_COMPILER=g++-10 \
      -DCMAKE_Fortran_COMPILER=gfortran-10 ..
```
