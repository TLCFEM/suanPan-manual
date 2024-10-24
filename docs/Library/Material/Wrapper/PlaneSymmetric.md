# PlaneSymmetric

Plane Symmetric Wrapper

Wraps a 3D host material model into a 2D plane symmetric model that can be used with 2D membrane elements.

## Syntax

```
material PlaneSymmetric13 (1) (2)
material PlaneSymmetric23 (1) (2)
# (1) int, unique material tag
# (2) int, 3D reference material tag
```

## Remarks

1. The token `PlaneSymmetric13` indicates $$\sigma_{11}=\sigma_{33}$$ and $$\tau_{12}=\tau_{32}$$.
2. The token `PlaneSymmetric23` indicates $$\sigma_{22}=\sigma_{33}$$ and $$\tau_{12}=\tau_{31}$$.

