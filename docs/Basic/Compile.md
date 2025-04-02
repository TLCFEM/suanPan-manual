# Compilation and Customisation

## With Docker

### Dev Environment Images

Two images are provided for development purposes.

```bash
# vtk+mkl+cuda
docker pull tlcfem/suanpan-env-cuda
# vtk+mkl
docker pull tlcfem/suanpan-env
```

They can be used as development containers.
VS Code and CLion can be configured to use these containers for development.
There is no need to install any dependencies on the host machine.

The `tlcfem/suanpan-env` image also supports `arm64`, in which `OpenBLAS` is used as the linear algebra driver.

On AMD platforms, it is known that `MKL` may throttle thus yields a poor performance, it may be necessary to use a specific version of `OpenBLAS` or [`AMD Optimizing CPU Libraries (AOCL)`](https://www.amd.com/en/developer/aocl.html) instead.

### Docker Images

It is possible to compile the project with Docker.
Check the provided [`Dockerfile`s](https://github.com/TLCFEM/suanPan/tree/dev/Script) for more information.
One can build the image using the example `Dockerfile` as it is.
For example,

```
# the current folder contains the file Rocky.Dockerfile
docker build -t suanpan -f ./Rocky.Dockerfile .
```

Once the image is built, run the container and use `sp`, `suanpan` or `suanPan` to invoke the program in the container.
Maybe it is necessary to map some folders to the container.

```bash
docker run -it --rm suanpan
# now in the container
suanpan -v
```

Docker files provide a standard reproducible environment and a reference configuration.
One can always introduce adaptions to cater various needs.

## Without Docker

The following is a general guide that covers three main operating systems.
It mainly targets the `amd64` architecture.

### Prerequisites

1.  To configure the source code, [CMake](https://cmake.org/download/) shall be available. Please install it
    before configuring the source code package.
2.  The linear algebra driver used is [OpenBLAS](https://github.com/xianyi/OpenBLAS). You may want to compile it with the
    optimal configuration based on the specific machine. Otherwise, precompiled binaries (dynamic platform) are available
    in this [repository](https://github.com/TLCFEM/prebuilds).
3.  It is strongly recommended installing Intel MKL for potentially better performance.
4.  Please be aware that MKL is throttled on AMD platforms. Performance comparisons can be seen for
    example [here](https://github.com/flame/blis/blob/master/docs/Performance.md). If you have AMD CPUs please collect
    more knowledge to determine which linear algebra library is more suitable.

### Toolsets

A number of new features from new standards are utilized. To compile the binary, a compiler that supports **C++20** is
required.

GCC 11, Clang 13, MSVC 14.3, Intel compilers and later version of those compilers are tested with the source code.

On Windows, Visual Studio with Intel oneAPI toolkit is recommended.
Alternatively, [WinLibs](http://winlibs.com/) can be used if GCC compilers are preferred.

On other platforms (Linux and macOS), simply use GCC which comes with a valid Fortran compiler.
Clang can also be used for C/CPP code, but since Clang and GCC have different supports for C++ new standards, successful
compilation is not guaranteed with Clang.

### Obtain Source Code

Download the source code archive from GitHub [Releases](https://github.com/TLCFEM/suanPan/releases) or the
latest [stable code](https://github.com/TLCFEM/suanPan/archive/master.zip).

### Configure and Compile

The manual compilation is not difficult in general.
The CI/CD configuration files can be referred to if you wish.
Please check [this](https://github.com/TLCFEM/suanPan/tree/dev/.github/workflows) page.
Here some general guidelines are given.

#### Windows (Visual Studio)

This is highly tailored to my own machine.
Thus, it is not recommended to use it directly.
Instead, use VS Code with CMake extension to automatically configure the project.

A solution file is provided under `MSVC/suanPan` folder. There are two configurations:

1.  `Debug`: Assume no available Fortran compiler, all Fortran related libraries are provided as precompiled DLLs. Use
    OpenBLAS for linear algebra. Multithreading disabled. Visualisation disabled. HDF5 support disabled.
2.  `Release`: Fortran libraries are configured with Intel compilers. Use MKL for linear algebra. Multithreading enabled.
    Visualisation enabled with VTK version 9.4. HDF5 support enabled. CUDA enabled.

This [repository](https://github.com/TLCFEM/prebuilds) contains some precompiled libraries used.

If VTK, Intel oneAPI Toolkit and CUDA are not installed, only the `Debug` configuration can be successfully compiled.
Simply open the solution and switch to Debug configuration, ignore all potential warnings and build the solution.

To compile `Release` version, please

1.  Make sure oneAPI both Base and HPC toolkits, as well as VS integration, are installed.
    The MKL is enabled via integrated option `<UseInteloneMKL>Parallel</UseInteloneMKL>`.

2.  Make sure CUDA is installed. The environment variable `$(CUDA_PATH)` is used to locate headers.

3.  Make sure VTK is available. Then define a system environment variable `$(VTK_DIR)`, which points
    to the root folder of VTK library. On my machine, it is

    ```powershell
    VTK_DIR=C:\Program Files\VTK\
    ```

    For versions other than 9.4, names of the linked libraries shall be manually changed as they contain version numbers.
    Thus, it is not a good idea to switch to a different version. Precompiled VTK library is also available in
    this [repository](https://github.com/TLCFEM/prebuilds).

4.  Make sure MAGMA is available. Then define a system environment variable `$(MAGMA_DIR)`, which points
    to the root folder of MAGMA library. On my machine, it is

    ```powershell
    MAGMA_DIR=C:\Program Files\MAGMA\
    ```

    You probably need to compile MAGMA yourself. You can manually remove all magma related settings in the solution file
    if you don't want to use it.

Alternatively, `CMake` can be used to generate solution files if some external packages are not available.

#### Windows (Visual Studio Code)

Open the source code folder with VS Code.
Whether you choose GCC or MSVC, the configuration is done by CMake automatically.

#### Ubuntu

The following instructions are based on Ubuntu 22.04.
[CMake](https://cmake.org/) is used to manage builds.
It is recommended to use **CMake** GUI if appropriate.

1.  Install necessary tools.

    ```bash
    sudo apt-get install gcc g++ gfortran git cmake libomp5 libglvnd-dev -y
    ```

2.  Clone the project.

    ```bash
    git clone -b master --depth 1 https://github.com/TLCFEM/suanPan.git
    ```

3.  Create build folder and configure via CMake. The default configuration disables parallelism `-DSP_BUILD_PARALLEL=OFF`
    and enables HDF5 via bundled library `-DSP_ENABLE_HDF5=ON`. Please
    check [`CMakeLists.txt`](https://github.com/TLCFEM/suanPan/blob/dev/CMakeLists.txt) file or use GUI for available
    options.

    ```bash
    cd suanPan && mkdir build && cd build
    cmake ../
    ```

4.  Invoke `make`.

    ```bash
    make -j"$(nproc)"
    ```

Check the following recording.

[![asciicast](https://asciinema.org/a/685434.svg)](https://asciinema.org/a/685434)

##### Install VTK

Ubuntu official repository does not (Fedora does!) contain the latest VTK library. It's better to compile it manually.

1.  Install OpenGL first, as well as compilers if necessary.

    ```bash
    sudo apt install gcc-10 g++-10 gfortran-10 libglvnd-dev
    ```

2.  Obtain VTK source code and unpack.

    ```bash
    wget https://www.vtk.org/files/release/9.1/VTK-9.1.0.tar.gz
    tar -xf VTK-9.1.0.tar.gz
    ```

3.  Create folder for building VTK.

    ```bash
    mkdir VTK-build && cd VTK-build
    ```

4.  Configure and compile VTK library. If necessary, installation destination can be modified. Here static libraries are
    built.

    ```bash
    cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=../VTK-out ../VTK-9.1.0
    make install -j4
    ```

5.  Now obtain `suanPan` source code and unpack it. To configure it with VTK support, users may use the following
    flag `-DSP_ENABLE_VTK=ON`. If `FindVTK` is presented and `VTK` is installed to default location, there is no need
    to provide the variable `VTK_DIR`, otherwise point it to the `lib/cmake/vtk-9.1` folder.

##### Install MKL

The provided CMake configuration covers both `oneMKL` and `Intel MKL 2020`. Please note MKL is included in oneAPI
toolkit starting from 2021, which has a different folder structure compared to Intel Parallel Studio.

The following guide is a manual installation is based on Ubuntu terminal using the official repository.
See [this page](https://www.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-linux/top/installation/install-using-package-managers/apt.html)
for details.

1.  Add repository. To summarise,

    ```bash
    wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
    sudo apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
    echo "deb https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list 
    ```

2.  Install the package.

    ```bash
    sudo apt update && sudo apt install intel-oneapi-mkl-devel -y
    ```

3.  Now compile `suanPan` by enabling MKL via option `-DSP_ENABLE_MKL=ON`. The corresponding `MKLROOT` shall be assigned, for
    example `-DMKLROOT=/opt/intel/oneapi/mkl/latest/`, depending on the installation location. The configuration used
    for snap is the following one.

    ```bash
    -DCMAKE_BUILD_TYPE=Release
    -DCMAKE_INSTALL_PREFIX=
    -DMKLROOT=/opt/intel/oneapi/mkl/latest
    -DSP_BUILD_PARALLEL=ON
    -DSP_ENABLE_HDF5=ON
    -DSP_ENABLE_IOMP=OFF
    -DSP_ENABLE_MKL=ON
    -DSP_ENABLE_SHARED_MKL=OFF
    -DSP_ENABLE_VTK=ON
    -DVTK_DIR=$CRAFT_PART_BUILD/lib/cmake/vtk-9.4/
    ```

#### Fedora

##### VTK

Fedora offers the latest VTK library, simply install it.

```bash
sudo dnf install vtk-devel
```

##### MKL

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

#### macOS

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
cmake -DCMAKE_BUILD_TYPE=Release -DSP_BUILD_PARALLEL=ON -DSP_ENABLE_HDF5=ON -DSP_ENABLE_VTK=ON -DVTK_DIR=../VTK-out/lib/cmake/vtk-9.1/ .
# compile
make -j4
```

### Linear Algebra Driver

Any standard BLAS and LAPACK implementation can be used as the linear algebra driver which the application itself and `Armadillo` rely on.
Currently, the following are supported and tested.

1. [`OpenBLAS`](http://www.openmathlib.org/OpenBLAS/)
2. [`Intel oneAPI MKL`](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html)
3. [`AMD Optimizing CPU Libraries (AOCL)`](https://www.amd.com/en/developer/aocl.html)

As a general guideline, when it comes to choose a proper implementation, the following points shall be considered.

1. From my very personal experience, `OpenBLAS` is okay for small matrices on a few cores, but could be slow when the size hits some threshold.
   This is also seen in this [benchmark](https://github.com/flame/blis/blob/master/docs/Performance.md).
2. `Intel oneAPI MKL` is exclusively optimised for Intel CPUs, and may throttle on other platforms.
   This [benchmark](https://github.com/flame/blis/blob/master/docs/Performance.md) show clear differences on AMD platforms.
3. `AMD Optimizing CPU Libraries (AOCL)` is optimised for AMD CPUs based on `BLIS` and `FLAME` libraries, it performance on both platforms (and others) is superb.

Thus, use `Intel oneAPI MKL` if it is preferred or an Intel platform is targeted.
The downside is that `Intel oneAPI MKL` is proprietary and the final binary may have a large size.
For other cases, use `AMD Optimizing CPU Libraries (AOCL)` when possible.
The downside it that it may need manual compilation of the libraries for the target OS.
`OpenBLAS` shall be deemed as the last resort and the usage is discouraged as of writing.

### Build Options

If CMake GUI is used to configure the project, the following options are available.

1. `BUILD_SHARED_LIBS`: If enabled, all libraries will be built as shared libraries.
2. `SP_BUILD_DLL_EXAMPLE`: If enabled, example element/material/section implemented as external libraries will be built.
3. `SP_BUILD_PARALLEL`: If enabled, `TBB` will be used for multithreading so that element update, global matrix
   assembly, etc., can be parallelized. `OpenMP` is not controlled by this option given that `OpenMP` support is
   available in major platforms. It will be used for low level parallelization such as linear algebra operations (which
   is controlled by `Armadillo`), matrix solving (which is controlled by various solvers). Thus, this flag only controls
   the `suanPan` application itself.
4. `SP_ENABLE_HDF5`: If enabled, `HDF5` will be used to provide support for [`hdf5recorder`](../Library/Recorder/Recorder.md).
5. `SP_ENABLE_VTK`: If enabled, `VTK` will be used to provide support for visualization. It will be useful to
   generate `.vtk` files that can be used in `Paraview` for post-processing. If enabled, `VTK_DIR` needs to be set to
   the path of `VTK` installation. For example, `VTK_DIR=/usr/local/opt/vtk/lib/cmake/vtk-9.1`.
6. `SP_ENABLE_CUDA`: `CUDA` needs to be installed manually by the user. If enabled, `CUDA` based solvers will be
   available. However, for dense matrix storage, only full matrix storage scheme is supported by `CUDA`. Note full
   matrix storage scheme is not favorable for FEM. It can, however, be used for sparse matrix solving and mixed
   precision solving.
7. `SP_ENABLE_MAGMA`: `MAGMA` needs to be installed manually by the user. If enabled, `MAGMA` based solvers will be
   available.
8. `SP_ENABLE_ASAN`: If enabled, address sanitizer will be enabled.
9. `SP_ENABLE_CODECOV`: If enabled, compile options will be enabled to support code coverage report.
10. `SP_ENABLE_AVX`: If enabled, compiler flags `-mavx` or `/arch:AVX` will be used. (~2011)
11. `SP_ENABLE_AVX2`: If enabled, compiler flags `-mavx2` or `/arch:AVX2` will be used. (~2013)
12. `SP_ENABLE_AVX512`: If enabled, compiler flags `-mavx512f` or `/arch:AVX512` will be used. (~2016)
13. `SP_ENABLE_TBB_ALLOC`: If enabled, the TBB's memory allocator will be used.
14. `SP_OPENBLAS_PATH`: If assigned, link the designated `OpenBLAS` library, otherwise the bundled version will be used.
15. `SP_ENABLE_AOCL`: If enabled, one can use the `AOCL` implementation via assigning library paths
    `AOCL_BLIS_PATH`, `AOCL_FLAME_PATH` and `AOCL_UTILS_PATH`.
16. `SP_ENABLE_MKL`: `MKL` needs to be installed manually by the user. If enabled, `MKL` will be used
    for linear algebra operations. If `SP_ENABLE_MKL` is enabled, the following
    additional options are available.
17. `SP_ENABLE_SHARED_MKL`: If enabled, dynamically linked `MKL` libraries will be used. Otherwise, statically linked `MKL`
    libraries will be used, leading to larger binary size but faster execution and fewer dependencies.
18. `SP_ENABLE_IOMP`: If enabled, Intel's OpenMP implementation will be used. Otherwise, Default ones (such as GNU OpenMP
    library) will be used.
19. `MKLROOT`: Set this path to the root directory of `MKL` installation. For
    example, `C:/Program Files (x86)/Intel/oneAPI/mkl/latest` or `/opt/intel/oneapi/mkl/latest`.

### Example Configuration

The following command is used to compile the program to be distributed via snap. See
this [file](https://github.com/TLCFEM/suanPan/blob/dev/snapcraft.yaml).

```bash
# assume current folder is suanPan/build
# the parent folder contains source code
cmake -DCMAKE_INSTALL_PREFIX= \
      -DCMAKE_BUILD_TYPE=Release \
      -DSP_BUILD_PARALLEL=ON \
      -DSP_ENABLE_HDF5=ON \
      -DSP_ENABLE_VTK=ON \
      -DVTK_DIR=$CRAFT_PART_BUILD/lib/cmake/vtk-9.4/ \
      -DSP_ENABLE_MKL=ON \
      -DMKLROOT=/opt/intel/oneapi/mkl/latest \
      -DSP_ENABLE_IOMP=OFF \
      -DSP_ENABLE_SHARED_MKL=OFF
```

### `aarch64` Architecture

The `aarch64` architecture is supported by the source code.
But one shall prepare the dependencies manually.
As MKL is not available for `aarch64`, one shall use `OpenBLAS` or `AOCL` only.

`OpenBLAS` is the only necessary dependency.
All other dependencies are optional.

To use `AOCL`, one shall manually compile the `blis` and `flame` libraries in advance.
