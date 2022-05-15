# plot

The `plot` command can be used to plot and save visualization as `.vtk` file.

**Only binaries compiled with VTK libraries can use this command. Otherwise, it does nothing.**

Since `Paraview` can be used to perform all kinds of post-processing, the objective is not to implement a full-featured
visualisation support.

## Syntax

The `plot` command uses a different parsing mechanism.

```
plot [-keyword [-parameters]...]
```

Available keywords and corresponding parameters are listed as follows.

1. `scale` controls the scale of deformed configuration. A single double value is required as parameter. If `undeformed`
   is used, then `scale` will be set to zero. Example: `scale 2`
2. `deformed` sets deformed plot.
3. `undeformed` sets undeformed plot.
4. `type` controls which quantity shall be extracted and plotted. A single string is required as parameter. Available
   values can be seen in output types. Example: `type U1`
5. `fontsize` controls the font size of legend, title, etc. This has no effect if the plot is saved.
   Example: `fontsize 14`
6. `nobar` disables legend in plot window.
7. `material` filters the elements plotted based on material tag. A single unsigned integer is required as parameter.
   Example: `material 1`
8. `size` controls the size of plot window. Two double values are required. Examples: `size 300 400`
9. `save` indicates the file name. A string value with suffix of `.vtk` is required. Example: `save S11.vtk`
