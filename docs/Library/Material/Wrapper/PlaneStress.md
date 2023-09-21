# PlaneStress

Plane Stress Wrapper

Wraps a 3D host material model into a 2D plane stress model that can be used with 2D membrane elements.

## Syntax

```
material PlaneStress (1) (2) [3]
# (1) int, unique tag
# (2) int, 3D material tag
# [3] int, maximum iteration, default: 1
```

The response of attached 3D material model will be output when recorded.

By default, a non-iterative algorithm is implemented.
If the strain increment is large, the algorithm may not converge.
In this case, the optional argument `[3]` can be used to activate local iterations.
If it is greater than one, the algorithm will perform local iteration up to `[3]` times.
