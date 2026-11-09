# Compile the Application

`suanPan` can be compiled with Docker or natively on the host system.
Docker provides a reproducible environment and is the recommended approach for development.
Native compilation gives full control over the build and is required for some platform-specific features.
If you only need a ready-to-run binary, see [Obtain the Application](../GettingStarted/Obtain.md).

## With Docker

### Dev Environment Images

Two images are provided for development purposes.

```bash
# vtk+mkl+cuda
docker pull tlcfem/suanpan-env:cuda
# vtk+mkl
docker pull tlcfem/suanpan-env
```

They can be used as development containers.
VS Code and CLion can be configured to use these containers for development.
There is no need to install any dependencies on the host machine.

The `tlcfem/suanpan-env` image also supports `arm64`, in which `OpenBLAS` is used as the linear algebra driver.

On AMD platforms, it is known that `MKL` may throttle and thus yield poor performance; it may be necessary to use a specific version of `OpenBLAS` or [`AMD Optimizing CPU Libraries (AOCL)`](https://www.amd.com/en/developer/aocl.html) instead.

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
It may be necessary to map some folders to the container.

```bash
docker run -it --rm suanpan
# now in the container
suanpan -v
```

Docker files provide a standard reproducible environment and a reference configuration.
One can always introduce adaptations to cater to various needs.

## Without Docker

The following is a general guide that covers three main operating systems.
It mainly targets the `amd64` architecture.

### Prerequisites

1.  To configure the source code, [CMake](https://cmake.org/download/) shall be available.
    Please install it before configuring the source code package.
2.  The linear algebra driver used is [OpenBLAS](https://github.com/xianyi/OpenBLAS).
    You may want to compile it with the optimal configuration based on the specific machine.
    Otherwise, precompiled binaries (dynamic platform) are available in this [repository](https://github.com/TLCFEM/prebuilds).
3.  It is strongly recommended to install Intel MKL for potentially better performance.
4.  Please be aware that MKL is throttled on AMD platforms.
    Performance comparisons can be seen for example [here](https://github.com/flame/blis/blob/master/docs/Performance.md).
    If you have AMD CPUs please collect more knowledge to determine which linear algebra library is more suitable.

### Toolsets

A number of new features from new standards are utilized.
To compile the binary, a compiler that supports **C++20** is required.

GCC 13, Clang 18, VS 2026, Intel compilers and later versions of those compilers are tested with the source code.

On Windows, Visual Studio with Intel oneAPI toolkit is recommended.
Alternatively, [WinLibs](http://winlibs.com/) can be used if GCC compilers are preferred.

On other platforms (Linux and macOS), simply use GCC which comes with a valid Fortran compiler.
Clang can also be used for C/CPP code, but since Clang and GCC have different support for new C++ standards, successful compilation is not guaranteed with Clang.

### Obtain Source Code

Download the source code archive from GitHub [Releases](https://github.com/TLCFEM/suanPan/releases) or the latest [stable code](https://github.com/TLCFEM/suanPan/archive/master.zip).
The archive is complete for non-MPI compilations.

To compile with MPI support, it is necessary to clone the dependencies as well.
This can be done via `git clone` such as

```bash
git clone --recurse-submodules https://github.com/TLCFEM/suanPan.git
```

### Configure and Compile

The manual compilation is not difficult in general.
The CI/CD configuration files can be referred to if you wish.
Please check [this](https://github.com/TLCFEM/suanPan/tree/dev/.github/workflows) page.

Choose the guide for your platform.

* [Windows](Platforms/Windows.md)
* [Linux](Platforms/Linux.md)
* [macOS](Platforms/MacOS.md)

After the project is configured, see [Build Options](Options.md) for the available CMake options and customisation details.

Continue with [Build Options](Options.md).
