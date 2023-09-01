# Uniaxial

Uniaxial Wrapper

Wraps a 3D host material model into a 1D uniaxial model that can be used with 1D elements.

It is assumed that $$\sigma_{22}=\sigma_{33}=\tau_{12}=\tau_{23}=\tau_{31}=0$$.

```
material Uniaxial (1) (2) [3]
# (1) int, unique material tag
# (2) int, associated 3D material tag
# [3] int, maximum iteration allowed, default: 1
```

The response of attached 3D material models will be output when recorded.
