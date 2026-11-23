# plot

The `plot` command plots and saves visualisations as files.

**Only binaries compiled with VTK libraries can use this command.**
**Otherwise, it does nothing.**

Since `Paraview` can perform all kinds of post-processing, the objective here is not to provide full-featured visualisation support.

## Syntax

The `plot` command uses a different parsing mechanism.

```text title="plot"
plot [-keyword [-parameters]...]
```

Available keywords and corresponding parameters are listed as follows.

1. `scale` controls the scale of the deformed configuration.
   A single double value is required as a parameter.
   The default is zero (undeformed).
   Example: `scale 2`
2. `type` controls which quantity is extracted and plotted.
   A single string is required as a parameter.
   The available values can be found in the output types.
   Example: `type U1`
3. `fontsize` controls the font size of the legend, title, etc.
   This has no effect if the plot is saved.
   Example: `fontsize 14`
4. `nobar` disables the legend in the plot window.
5. `size` controls the size of the plot window.
   Two double values are required.
   Example: `size 300 400`
6. `save` specifies the file name.
   A string value is required.
   The extension suffix is appended automatically.
   Example: `save S11`

## Remarks

Invoking this command with proper parameters spawns an interactive rendering window using VTK.
It offers a quick view of the model.
The window can be closed by pressing the `q` key.
The window does not block the application, so multiple quantities can be plotted at the same time.
However, a new analysis is not performed until all windows are closed.

## Example

![plot](https://raw.githubusercontent.com/flathub/io.github.tlcfem.suanPan/screenshot/plot.png)
