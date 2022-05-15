# Rebar2D

Orthotropic Material

## Syntax

```
material Rebar2D (1) (2) (3) (4) (5)
# (1) int, unique material tag
# (2) int, x direction steel material tag
# (3) int, y direction steel material tag
# (4) double, x direction reinforcement ratio
# (5) double, y direction reinforcement ratio
```

The uniform reinforcement is defined along global axes. To have arbitrarily aligned layout, users can wrap it into
a [`Rotation2D`](../Wrapper/Rotation2D.md) wrapper.
