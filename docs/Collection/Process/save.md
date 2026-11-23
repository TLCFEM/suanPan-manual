# save

The `save` command saves data to disk.

## Syntax

```text title="save"
save recorder (1...)
# (1...) int, tags of recorders to be saved
```

The command can also save analysis data such as system matrices and the model itself.

```text title="save"
save stiffness [name]
save mass [name]
save damping [name]
save model [name]
# [name] optional string, output file name
```

The default file names are `K` for the stiffness matrix, `M` for the mass matrix, `C` for the damping matrix and `Model.h5` for the model.
