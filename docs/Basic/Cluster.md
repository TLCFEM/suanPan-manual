# Utilizing Distributed Memory Multi Node Cluster

The element state determination, as well as solving the global system, can be distributed over a process grid.
By enabling MPI, the application can be executed on clusters.
The architecture design is explained in [this](Architecture.md) page.

There are a few caveats.
Since the distributed solvers for linear systems rely on external libraries, typically an implementation of ScaLAPACK.
There are not many choices, one can use the reference implementation, which may not have a superb performance.
One can also use AMD's [implementation](https://github.com/amd/aocl-scalapack) or Intel's [implementation](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html).

## Prerequisites

Considering the procedure of manually compiling dependencies is cumbersome, we only support Intel's ecosystem for the moment.
That means, `MKL` must be enabled via the option `-DSP_ENABLE_MKL=ON`.
`MKL` can be installed a priori.

For example, according to the official documentation, with APT, it can be installed via the following commands.

```bash
sudo apt update
sudo apt install -y gpg-agent wget
wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list
sudo apt update
sudo apt install intel-oneapi-mkl-devel
```

It is likely that Intel's MPI library is also required, otherwise a working implementation shall be pre-installed.
Note, the MPI bundled by your distro may not work.

```bash
sudo apt install intel-oneapi-mpi-devel
```

## Configuration

The minimum configuration requires two flags: `-DSP_ENABLE_MKL=ON` and `-DSP_ENABLE_MPI=ON`.
`CMake` will try to locate the installation of `MKL` and automatically configure the project.
To ensure everything works as intended, it may be necessary to activate the `oneAPI` environment.

```bash
source /opt/intel/oneapi/setvars.sh
```

This can be done via, for example, `environment file` in the toolchain configuration in CLion, `environmentSetupScript` in [`cmake-kits.json`](https://vector-of-bool.github.io/docs/vscode-cmake-tools/kits.html) in VS Code.

By default, it will use Intel's MPI.
If another implementation, for example, MPICH and/or OpenMPI, is used, use `MPI_HOME` to override the path, for example, `-DMPI_HOME=~/Documents/OpenMPI`.

The project tries to automatically detect the vendor of MPI via its path, but it may fail.
You may need to set `MKL_MPI` to a proper value.
The available values can be found in `/opt/intel/oneapi/mkl/latest/lib/cmake/mkl/MKLConfig.cmake`.
For example, on my machine, there are

```
# MKL_MPI
#    Values:  intelmpi, mpich, openmpi, msmpi, mshpc
#    Default: intelmpi
```

!!! note
    If two different implementations of MPI are used, the compilation may succeed, the application can still crash on execution.

Typically, for problems that need to be run on clusters, the default 32-bit indexing is not sufficient.
The limit of a 32-bit integer is slightly above 2 billion, meaning that, if the global matrix is stored in dense full format, the maximum size is 46340.
If each node has 2 DoFs (2D node with translational DoFs only), this corresponds to 23170 nodes.
If each node has 6 DoFs (3D node with both translational and rotational DoFs), this corresponds to 7723 nodes.
But in the context of FEM, the full storage is rarely used, so this is the lower bound.
Considering the banded storage, typically the bandwidth is a small fraction of the global size, say, 1%, then the lower bound should be at least 800000 3D shell nodes.

If the problem is sizeable, it is possible to enable 64-bit indexing via `-DSP_ENABLE_64BIT_INDEXING=ON`.
This will link `ilp64` version of `MKL`, and compile all dependencies with the proper settings.
