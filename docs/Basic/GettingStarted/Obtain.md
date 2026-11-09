# Obtain the Application

## Docker Image

A docker image is available at [Docker Hub](https://hub.docker.com/r/tlcfem/suanpan).
Both `amd64` and `arm64` architectures are available.
To use it, docker needs to be installed first.
See [this page](https://docs.docker.com/get-docker/) for details.

Once docker is installed, it is possible to pull the image via:

```bash
docker pull tlcfem/suanpan
```

Then it is possible to run the container in an interactive manner via:

```bash
docker run -it --rm tlcfem/suanpan
```

Within the container, one can use one of the following commands to invoke the application.

```bash
suanPan
suanpan
sp
```

One can also attach a volume to the container to access files in the host machine.
This may be the main use case.
Assume there is a model file under the path `/path/to/host/folder/example.model.sp`; to run the analysis under this folder, one can use the following command.

```bash
docker run --rm -v /path/to/host/folder:/dirty -w /dirty tlcfem/suanpan sp -f example.model.sp
```

The Docker image is convenient on machines with older kernels or limited by other factors that do not allow execution of precompiled binaries.

This is now supported by the [VS Code extension](https://marketplace.visualstudio.com/items?itemName=tlc.suanpan).

The following shall be noted.

1. For maximum compatibility, the image is compiled without AVX support.
2. On `amd64`, Intel MKL is used.
   On `arm64`, OpenBLAS is used.

If necessary, one can build images with different configurations to enable `AVX` and `AVX2` support and/or `AOCL` support on AMD platforms.

## Precompiled Binaries

The binaries are published on GitHub.
[https://github.com/TLCFEM/suanPan/releases](https://github.com/TLCFEM/suanPan/releases)

Binaries on Windows, Ubuntu and macOS are compiled and deployed automatically on the `master` branch.
The precompiled binaries are compiled on the following OS versions.

| Platform | Version             |
|----------|---------------------|
| Windows  | Windows Server 2025 |
| Linux    | Ubuntu 24.04        |
| macOS    | Sequoia 15          |

For older versions or other flavours of Linux, successful execution is not guaranteed.
Please consider compiling the binaries manually.

In order to enable `CUDA` backed solvers, the program shall be compiled locally with preinstalled external libraries.
See [this](../Building/Compile.md) page.

Currently, the following package managers can be used to install the program.

| Platform | Package Manager                                                      | Command                                            |
|----------|----------------------------------------------------------------------|----------------------------------------------------|
| Windows  | [Chocolatey](https://community.chocolatey.org/packages/suanpan)      | `choco install suanpan`                            |
| Windows  | [scoop](https://scoop.sh/)                                           | `scoop install suanpan`                            |
| Linux    | [snap](https://snapcraft.io/suanpan)                                 | `snap install suanpan`                             |
| Linux    | [flatpak](https://flathub.org/apps/details/io.github.tlcfem.suanPan) | `flatpak install flathub io.github.tlcfem.suanPan` |

The binaries are tested in standard environments: fresh new [Win10/11](https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/) images, docker images [Ubuntu](https://hub.docker.com/_/ubuntu) and [Fedora](https://hub.docker.com/_/fedora), and [macOS](https://github.com/actions/runner-images/blob/main/images/macos/macos-15-Readme.md) GitHub image.

### Chocolatey

[![asciicast](https://asciinema.org/a/684063.svg)](https://asciinema.org/a/684063)

### snap

[![asciicast](https://asciinema.org/a/684061.svg)](https://asciinema.org/a/684061)

### flatpak

To run the application, one shall use the following command in terminal.

```bash
flatpak run io.github.tlcfem.suanPan
```

Since no shim is created, it would be convenient to create an alias such that

```bash
echo "alias suanpan=\"flatpak run io.github.tlcfem.suanPan\"" >> ~/.bashrc
```

Then it is possible to use `suanpan` to invoke the application.

## Execute Program

By default, the `AVX2` support is turned on to utilize CPU capability.
For CPUs that do not support `AVX2`, the application **cannot** be successfully executed.
Users can either compile the program by themselves or request a specific version by filing an issue.

The name of the executable is `suanPan`; however, snap/chocolatey/scoop will create a shim executable named as `suanpan`.
Depending on how the application is installed, one may use `suanpan` or `suanPan` to invoke the application.

The parallelization is enabled mostly by the `TBB` library and `<execution>` header (C++17).
If the program is compiled with **SUANPAN_MT** macro, parallelization is used by default.
The **OpenMP** is enabled in several parts of the program; users can set the environment variable **OMP_NUM_THREADS** to customize some **OpenMP** based parallelization.
To do so, users can, for example, in Windows, use the following command.

```powershell
set OMP_NUM_THREADS=6
```

On Linux, the dynamic loading path needs to be set so that dynamic libraries such as `libtbb.so` can be successfully found.
If the application is installed via `snap`/`apt`/`dnf`, it is automatically done.

```bash
# current path contains suanPan
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/../lib
./suanPan
```

Alternatively, users can execute the program via the provided `suanPan.sh` script.

```bash
# create links to the executables
# the script assumes ~/.local/bin is in the path and creates a symbolic link to the executable
./suanPan.sh --create-link
# cd to other folders and execute the program
cd ~
suanpan
```

### CLI Mode

By running the program without any parameters, it enters CLI mode by default.
Users can create models in an interactive manner.

```
+--------------------------------------------------------+
|             ____             suanPan is an open source |
|   ___ _   _|  _ \ __ _ _ __     FEM framework (64-bit) |
|  / __| | | | |_) / _` | '_ \           Canopus (3.7.0) |
|  \__ \ |_| |  __/ (_| | | | |        by tlc @ 427eefcb |
|  |___/\__,_|_|   \__,_|_| |_|      all rights reserved |
|                                 10.5281/zenodo.1285221 |
+--------------------------------------------------------+
|  https://github.com/TLCFEM/suanPan                     |
|  https://tlcfem.github.io/suanPan-manual/latest        |
+--------------------------------------------------------+
|  https://bit.ly/vsc-sp                                 |
+--------------------------------------------------------+

suanPan ~<> 
```

A command named as `example` is available to automatically create an example model and perform the analysis.

```
+--------------------------------------------------------+
|             ____             suanPan is an open source |
|   ___ _   _|  _ \ __ _ _ __     FEM framework (64-bit) |
|  / __| | | | |_) / _` | '_ \           Canopus (3.7.0) |
|  \__ \ |_| |  __/ (_| | | | |        by tlc @ 427eefcb |
|  |___/\__,_|_|   \__,_|_| |_|      all rights reserved |
|                                 10.5281/zenodo.1285221 |
+--------------------------------------------------------+
|  https://github.com/TLCFEM/suanPan                     |
|  https://tlcfem.github.io/suanPan-manual/latest        |
+--------------------------------------------------------+
|  https://bit.ly/vsc-sp                                 |
+--------------------------------------------------------+

suanPan ~<> example
====================================================
-> A Minimum Example: Elastic Truss Under Tension <-
====================================================
--> create two nodes at (0,0) and (2,0):
        node 1 0 0
        node 2 2 0
--> create material model (elastic modulus 52):
        material Elastic1D 1 52
--> create a truss element connecting nodes 1 and 2:
        element T2D2 1 1 2 1 93
--> define boundary condition and load:
        fix 1 1 1
        fix 2 2 1 2
        displacement 1 0 1.4 1 2
--> define a static step:
        step static 1
--> perform the analysis:
        analyze
[WARNING] BandMat.hpp:62 ~> The storage requirement for the banded matrix is larger than that of a full matrix, consider using a full/sparse matrix instead.
>> Current Analysis Time: 1.00000.

--> check nodal force (P=UEA/L=1.4*52*93/2=3385.2):
        peek node 2
Node 2:
Coordinate:
  2.0000e+00  0.0000e+00
Displacement:
  1.4000e+00  0.0000e+00
Resistance:
  3.3852e+03  0.0000e+00

--> clean up and it's your turn!
====================================================
suanPan ~<> 
```

### Batch Mode

To analyze the model written in a model file named, for example, `example.supan`, the `-f` or `--file` parameter can be used.
First, we create the file `example.supan` with the `exit` command.

```bash
echo exit > example.supan
```

Then we can run it by the following command.

```bash
suanpan -f ./example.supan
```

Or on Windows,

```powershell
./suanPan.exe -f example.supan
```

If the model has been prechecked, it is possible to run the analysis without output.
It is known that printing strings to terminals slows down the analysis.
Users can use the `-np` or `--noprint` option to suppress output.

```powershell
./suanPan.exe -np -f example.supan
```

In the CLI mode, it is possible to use the `file` command to load the file.

```
+--------------------------------------------------+
|   __        __         suanPan is an open source |
|  /  \      |  \           FEM framework (64-bit) |
|  \__       |__/  __   __      Betelgeuse (2.3.0) |
|     \ |  | |    |  \ |  |      maintained by tlc |
|  \__/ |__| |    |__X |  |    all rights reserved |
|                           10.5281/zenodo.1285221 |
+--------------------------------------------------+
|  https://github.com/TLCFEM/suanPan               |
|  https://github.com/TLCFEM/suanPan-manual        |
+--------------------------------------------------+
|  https://gitter.im/suanPan-dev/community         |
+--------------------------------------------------+

suanPan ~<> file example.supan
```

Continue with [Your First Analysis](Analyze.md).
