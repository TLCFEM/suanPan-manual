# Automation and System Integration

## Windows

A batch file named as `AddAssociation.bat` is provided in the archive.
It associates `*.sp` and `*.supan` files with the program and copies configuration files to the default folder if Sublime Text is installed.
If the package is installed via package managers, please manually search for and execute this file.

Admin privileges are required.

## Linux

A bash script named as `suanPan.sh` is provided in the archive to set up the above configurations automatically.
The script can be used to both execute the program and create symbolic links.

For first-time use, the following commands create a soft link under `$HOME/.local/bin` so that users can execute the program anywhere by invoking the command `suanpan` in any folder.
The Sublime Text configuration files are copied to the default folder if Sublime Text is installed.

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

1.  If the [`terminal`](../../Collection/Process/terminal.md) command is used, one can change files in the file system.
2.  If one decides to download new versions via the bundled updater, the archive is downloaded to the current working directory.
    The updater is not always bundled.

The script `suanPan.sh` writes the following files to the system.

1.  `$HOME/.local/share/applications/suanPan.desktop`
2.  `$HOME/.local/bin/suanpan`
3.  `$HOME/.config/sublime-text/Packages/User/suanPan.sublime-build`
4.  `$HOME/.config/sublime-text/Packages/User/suanPan.sublime-completions`
5.  `$HOME/.config/sublime-text/Packages/User/suanPan.sublime-syntax`

The script `AddAssociation.bat` changes the following settings.

1.  Associate `*.sp` and `*.supan` files with the program.
2.  Copy configuration files to default folder if Sublime Text is installed.

Continue with [Compile the Application](../Building/Compile.md).
