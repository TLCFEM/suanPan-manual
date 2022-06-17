# Rebar3D

Orthotropic Material

## Syntax

```text
material Rebar3D (1) (2) (3) (4) (5) (6) (7)
# (1) int, unique material tag
# (2) int, x direction steel material tag
# (3) int, y direction steel material tag
# (4) int, z direction steel material tag
# (5) double, x direction reinforcement ratio
# (6) double, y direction reinforcement ratio
# (7) double, z direction reinforcement ratio
```

The uniform reinforcement is defined along global axes. To have arbitrarily aligned layout, users can wrap it into
a [`Rotation3D`](../../Wrapper/Rotation3D.md) wrapper.
