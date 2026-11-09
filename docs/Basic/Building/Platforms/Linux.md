# Compiling on Linux

This page describes native compilation on Linux.
For the general prerequisites and source code instructions, see [Compile the Application](../Compile.md).

## Ubuntu

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

3.  Create build folder and configure via CMake.
    The default configuration disables parallelism `-DSP_BUILD_PARALLEL=OFF` and enables HDF5 via bundled library `-DSP_ENABLE_HDF5=ON`.
    Please check [`CMakeLists.txt`](https://github.com/TLCFEM/suanPan/blob/dev/CMakeLists.txt) file or use GUI for available options.

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

### Install VTK

The Ubuntu official repository does not (Fedora does!) contain the latest VTK library.
It's better to compile it manually.

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

4.  Configure and compile VTK library.
    If necessary, installation destination can be modified.
    Here static libraries are built.

    ```bash
    cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=../VTK-out ../VTK-9.1.0
    make install -j4
    ```

5.  Now obtain `suanPan` source code and unpack it.
    To configure it with VTK support, users may use the following flag `-DSP_ENABLE_VTK=ON`.
    If `FindVTK` is present and `VTK` is installed to default location, there is no need to provide the variable `VTK_PATH`, otherwise point it to the `lib/cmake/vtk-9.1` folder.

### Install MKL

The provided CMake configuration covers both `oneMKL` and `Intel MKL 2020`.
Please note MKL is included in oneAPI toolkit starting from 2021, which has a different folder structure compared to Intel Parallel Studio.

The following guide is a manual installation based on the Ubuntu terminal using the official repository.
See [this page](https://www.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-linux/top/installation/install-using-package-managers/apt.html) for details.

1.  Add repository.
    To summarise,

    ```bash
    wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
    sudo apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
    echo "deb https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list 
    ```

2.  Install the package.

    ```bash
    sudo apt update && sudo apt install intel-oneapi-mkl-devel -y
    ```

3.  Now compile `suanPan` by enabling MKL via option `-DSP_ENABLE_MKL=ON`.
    The corresponding `MKL_PATH` shall be assigned, for example `-DMKL_PATH=/opt/intel/oneapi/mkl/latest/`, depending on the installation location.
    The configuration used for snap is the following one.

    ```bash
    -DCMAKE_BUILD_TYPE=Release
    -DCMAKE_INSTALL_PREFIX=
    -DMKL_PATH=/opt/intel/oneapi/mkl/latest
    -DSP_BUILD_PARALLEL=ON
    -DSP_ENABLE_HDF5=ON
    -DSP_ENABLE_IOMP=OFF
    -DSP_ENABLE_MKL=ON
    -DSP_ENABLE_SHARED_MKL=OFF
    -DSP_ENABLE_VTK=ON
    -DVTK_PATH=$CRAFT_PART_BUILD/lib/cmake/vtk-9.4/
    ```

## Fedora

### VTK

Fedora offers the latest VTK library, simply install it.

```bash
sudo dnf install vtk-devel
```

### MKL

Intel also provides a repository to install MKL via `dnf`.
See [this page](https://www.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-linux/top/installation/install-using-package-managers/yum-dnf-zypper.html) for details.

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

Install MKL.
You may perform a search `sudo dnf search intel-oneapi-mkl-devel` to find which package name is available and install the specific version if necessary.

```bash
sudo dnf install intel-oneapi-mkl-devel
```

The source can be compiled with VTK and MKL enabled.
