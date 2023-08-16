# Axisymmetric

Axisymmetric Wrapper

Wraps a 3D host material model into a 2D axisymmetric model that can be used with 2D axisymmetric elements such as
[CAX4](../../Element/Membrane/Axisymmetric/CAX4.md) and [CAX8](../../Element/Membrane/Axisymmetric/CAX8.md).

## Syntax

```
material Axisymmetric (1) (2)
# (1) int, unique tag
# (2) int, 3D material tag
```

The response of attached 3D material model will be output when recorded.
