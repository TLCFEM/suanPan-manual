# Rotation3D

3D Rotation Wrapper

Alters the inclination of the 3D host material model, it is typically used with anisotropic material models.

## Syntax

```
material Rotation3D (1) (2) (3...5)
# (1) int, unique material tag
# (2) int, associated material tag
# (3...5) double, three components of rotation vector
```

Rotations in 3D space may have different forms.
The [Euler vector](https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation) is used to represent the axis and
angle of rotation. Parameters `(3)` to `(5)` are three components of the vector $$\mathbf{\theta}$$.

The response of attached 3D material model will be output when recorded.
