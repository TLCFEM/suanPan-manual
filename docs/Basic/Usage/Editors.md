# Editor Setup

## VS Code

The VS Code extension is available [here](https://marketplace.visualstudio.com/items?itemName=tlc.suanpan).
It provides syntax highlighting and code completion.

The plugin also provides functionalities to invoke the analysis in docker containers.

![demo](https://github.com/TLCFEM/suanPan-vs/raw/master/images/example.gif)

## Sublime Text Workspace

I personally use [Sublime Text](https://www.sublimetext.com/) as my model editor.
Other tools like [VS Code](https://code.visualstudio.com/) can also be used.

### Syntax Highlighting

Create a new syntax file via `Tools -> Developer -> New Syntax...`, copy and paste the following sample content into the new file and save as `suanPan.sublime-syntax` under the default path.
It provides syntax highlighting for comments only.
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

A syntax file with (almost) all commands is provided as `suanPan.sublime-syntax` in the archive.
Please feel free to use/modify it.
It may be necessary to manually search for the file if the application is installed via some package manager.

### Autocomplete

All keywords used are stored in the JSON file `suanPan.sublime-completions`.
Place the file in the folder `~/.config/sublime-text-3/Packages/User/` (Linux) or `%appdata%\Sublime Text 3\Packages\User` (Windows) and you are good to go with the previous syntax file.
The new path has been changed to `~/.config/sublime-text/Packages/User/` (Linux) and `%appdata%\Sublime Text\Packages\User` (Windows) in `Sublime Text 4`.

### Build System

In order to render ANSI color codes correctly in Linux-like systems, you may wish to install the [ANSIescape](https://packagecontrol.io/packages/ANSIescape) package.
Now define a new build system via `Tools -> Build System -> New Build System...`, copy and paste the following contents in the file and save it as `suanPan.sublime-build`.
You may need to replace command `suanpan` with the full path of the executable.

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

To disable coloured output, use `-nc` (no colour) option such as

```bash
suanpan -nc -f model_file.supan
```

Continue with [Performance Tweaks](Performance.md).
