# Compiling on macOS

This page describes native compilation on macOS.
For the general prerequisites and source code instructions, see [Compile the Application](../Compile.md).

The following guide is based on macOS Big Sur (11).

Install tools.
`gfortran`, `llvm` and `libomp` are used for compiling the main program, `glfw` and `glew` are required for compiling `VTK`.
`VTK` does not compile with `GCC`.
Here, we use `Clang`.

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

`MKL` can be installed if necessary.
See this [page](https://software.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-macos/top.html).

Obtain the source code and configure.

```bash
# clone source code
git clone -b master https://github.com/TLCFEM/suanPan.git
# create build directory
mkdir suanpan-build && cd suanpan-build
# use clang, clang++ and gfortran
export CC=/usr/local/opt/llvm/bin/clang && export CXX=/usr/local/opt/llvm/bin/clang++ && export FC=gfortran-10
# configure project
cmake -DCMAKE_BUILD_TYPE=Release -DSP_BUILD_PARALLEL=ON -DSP_ENABLE_HDF5=ON -DSP_ENABLE_VTK=ON -DVTK_PATH=../VTK-out/lib/cmake/vtk-9.1/ .
# compile
make -j4
```
