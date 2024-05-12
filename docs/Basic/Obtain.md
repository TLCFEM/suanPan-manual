# Obtain

## Docker Image

A docker image is available at [Docker Hub](https://hub.docker.com/r/tlcfem/suanpan). To use it, 
docker needs to be installed first. See [this page](https://docs.docker.com/get-docker/) for details.

Once docker is installed, it is possible to pull the image via:

```bash
docker pull tlcfem/suanpan
```

Then it is possible to run the container in an interactive manner via:

```bash
docker run -it --rm tlcfem/suanpan
```

Within the container, one can use one of the following commands to run the program.

```bash
suanPan
suanpan
sp
```

One can also attach volume to the container to access the files in the host machine.
This may be the main use case.
And then run the file inside the container.

```bash
docker run -it --rm -v /path/to/host/folder:/path/to/container/folder tlcfem/suanpan
cd /path/to/container/folder
suanpan -f example.model.sp
```

Docker image is convenient on machines with older kernels or limited by other factors that does not allow 
execution of precompiled binaries.

## Precompiled Binaries

The binaries are published on
GitHub. [https://github.com/TLCFEM/suanPan/releases](https://github.com/TLCFEM/suanPan/releases)

Binaries on Windows, Ubuntu and macOS are compiled and deployed automatically on the `master` branch. The 
precompiled binaries are compiled on the following OS versions.

| Platform | Version             |
|----------|---------------------|
| Windows  | Windows Server 2022 |
| Linux    | Ubuntu 22.04        |
| macOS    | Ventura 13          |

For older versions or other flavours of Linux, successful execution is not guaranteed.
Please consider compiling the binaries manually.

In order to enable `CUDA` backed solvers, the program shall be compiled locally with preinstalled external libraries.
See this page [Compile](Compile.md).

Currently, the following package managers can be used to install the program.

| Platform | Package Manager                                                      | Command                                            |
|----------|----------------------------------------------------------------------|----------------------------------------------------|
| Windows  | [Chocolatey](https://community.chocolatey.org/packages/suanpan)      | `choco install suanpan`                            |
| Windows  | [scoop](https://scoop.sh/)                                           | `scoop install suanpan`                            |
| Linux    | [snap](https://snapcraft.io/suanpan)                                 | `snap install suanpan`                             |
| Linux    | [flatpak](https://flathub.org/apps/details/io.github.tlcfem.suanPan) | `flatpak install flathub io.github.tlcfem.suanPan` |

The binaries are tested in standard environments: fresh new
[Win10/11](https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/) images,
docker images [Ubuntu](https://hub.docker.com/_/ubuntu) and [Fedora](https://hub.docker.com/_/fedora),
and [macOS](https://github.com/actions/runner-images/blob/main/images/macos/macos-13-Readme.md) GitHub image.

### Chocolatey

[![asciicast](https://asciinema.org/a/491350.svg)](https://asciinema.org/a/491350)

### snap

[![asciicast](https://asciinema.org/a/lWRm5eV4gQtQ8rPX7NOdPZCyr.svg)](https://asciinema.org/a/lWRm5eV4gQtQ8rPX7NOdPZCyr)

### flatpak

To run the application, one shall use the following command in terminal.

```bash
flatpak run io.github.tlcfem.suanPan
```

Since no shim is created, it would be convenient to create alias such that

```bash
echo "alias suanpan=\"flatpak run io.github.tlcfem.suanPan\"" >> ~/.bashrc
```

Then it is possible to use `suanpan` to invoke the application.

## Execute Program

By default, the `AVX` support is turned on to utilize CPU capability. For CPUs that do not support `AVX`, the
application **cannot** be successfully executed. Users can either compile the program by themselves or request a
specific version by filing an issue. Processors that do not support `AVX` may be too slow to perform HPC based
simulations.

The name of the executable is `suanPan`, however, snap/chocolatey/scoop will create shim executable named as 
`suanpan`. Depending on how the application is installed, one may use `suanpan` or `suanPan` to invoke the application.

The parallelization is enabled mostly by the `TBB` library and `<execution>` header (C++17). If the program is compiled
with **SUANPAN_MT** macro, parallelization is used by default. The **OpenMP** is enabled in several parts of the
program, users can set environment variable **OMP_NUM_THREADS** to customize some **OpenMP** based parallelization. To
do so, users can, for example, in Windows, use the following command.

```powershell
set OMP_NUM_THREADS=6
```

On Linux, the dynamic loading path need to be set so that dynamic libraries such as `libtbb.so` can be successfully
found. If the application is installed via snap/apt/dnf, it is automatically done.

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

By running the program without any parameters, it enters CLI mode by default. Users can create models in an interactive
manner.

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

suanPan ~<>
```

A command named as `example` is available to automatically create an example model and perform the analysis.

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
current analysis time: 1.00000.
--> check nodal force (P=UEA/L=1.4*52*93/2=3385.2):
        peek node 2
Node 2:
   2.0000        0
Displacement:
   1.4000        0
Resistance:
   3.3852e+03            0

--> clean up and it's your turn!
====================================================
suanPan ~<>
```

### Batch Mode

To analyze the model written in a model file named as for example `example.supan`, the `-f` or `--file` parameter can be
used. First we create the file `example.supan` with `exit` command.

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

If the model has been prechecked, it is possible to run the analysis without output. It is known that printing strings
to terminals slows down the analysis. Users can use the `-np` or `--noprint` option to suppress output.

```powershell
./suanPan.exe -np -f example.supan
```

In the CLI mode, it is possible to use `file` command to load the file.

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

## VS Code

The VS Code extension is available [here](https://marketplace.visualstudio.com/items?itemName=tlc.suanpan).
It provides syntax highlighting and code completion.

![demo](https://github.com/TLCFEM/suanPan-vs/raw/master/images/example.gif)

## Sublime Text Workspace

I personally use [Sublime Text](https://www.sublimetext.com/) as my model editor. Other tools
like [Atom](https://atom.io/) and [VS Code](https://code.visualstudio.com/) can also be used.

### Syntax Highlighting

Create a new syntax file via `Tools -> Developer -> New Syntax...`, copy and paste the following sample content into the
new file and save as `suanPan.sublime-syntax` under the default path. It provides syntax highlighting for comments only.
Other components can be added accordingly.

```yaml
%YAML 1.2
---
file_extensions:
  - supan
  - sp
scope: source.supan
contexts:
  main:
    - match: '^[#!].*'
      scope: comment.line
    - match: '!.*'
      scope: comment.line
```

A syntax file with (almost) all commands is provided as `suanPan.sublime-syntax` in the archive. Please feel free to
use/modify it. It may be necessary to manually search for the file if the application is installed via some package manager.

### Autocomplete

All keywords used are stored in the JSON file `suanPan.sublime-completions`. Place the file in
folder `~/.config/sublime-text-3/Packages/User/` (Linux) or `%appdata%\Sublime Text 3\Packages\User` (Windows) and you
are good to go with the previous syntax file. The new path has been changed to `~/.config/sublime-text/Packages/User/` (
Linux) and `%appdata%\Sublime Text\Packages\User` (Windows) in `Sublime Text 4`.

### Build System

In order to render ANSI color codes correctly in Linux like systems, you may wish to
install [ANSIescape](https://packagecontrol.io/packages/ANSIescape) package. Now define a new build system
via `Tools -> Build System -> New Build System...`, copy and paste the following contents in the file and save it
as `suanPan.sublime-build`. You may need to replace command `suanpan` with the full path of the executable.

```json
{
  "cmd": [
    "suanpan",
    "-f",
    "$file"
  ],
  "selector": "source.supan",
  "file_patterns": [
    "*.supan",
    "*.sp"
  ],
  "target": "ansi_color_build",
  "syntax": "Packages/ANSIescape/ANSI.sublime-syntax"
}
```

Now models can be run in Sublime Text via the shortcut `Ctrl+B`.

To disable colored output, use `-nc` option such as

```bash
suanpan -nc -f model_file.supan
```

## Automation

### Windows

A batch file named as `AddAssociation.bat` is provided in the archive. It associates `*.sp` and `*.supan` files with the
program and copies configuration files to default folder if Sublime Text is installed. If the package is installed via
package managers, pleas manually search for and execute this file.

Admin privilege is required.

### Linux

A bash script named as `suanPan.sh` is provided in the archive to set up the above configurations automatically. The
script can be used to both execute the program and create symbolic links.

For the first time use, the following commands create a soft link under `$HOME/.local/bin` so that users can execute the
program anywhere by invoking command `suanpan` in any folder. The Sublime Text configuration files are copied to the
default folder if Sublime Text is installed.

```bash
# current path contains suanPan
chmod +x suanPan.sh
./suanPan.sh --create-link
# cd to other places such as folders that contain models
# now invoke the program
suanpan
```

Check the following recording.

[![asciicast](https://asciinema.org/a/418408.svg)](https://asciinema.org/a/418408)

## Changes Made to the System

The application itself does **not** write any files to folders other than the current working directory.

There are some exceptions though.

1. If the [`terminal`](../Collection/Process/terminal.md) command is used, one can change files in the file system.
2. If one decides to download new versions via the bundled updater, the archive is downloaded to the current working
   directory. The updater is not always bundled.

The script `suanPan.sh` writes the following files to the system.

1. `$HOME/.local/share/applications/suanPan.desktop`
2. `$HOME/.local/bin/suanpan`
3. `$HOME/.config/sublime-text/Packages/User/suanPan.sublime-build`
4. `$HOME/.config/sublime-text/Packages/User/suanPan.sublime-completions`
5. `$HOME/.config/sublime-text/Packages/User/suanPan.sublime-syntax`

The script `AddAssociation.bat` changes the following settings.

1. Associate `*.sp` and `*.supan` files with the program.
2. Copy configuration files to default folder if Sublime Text is installed.
