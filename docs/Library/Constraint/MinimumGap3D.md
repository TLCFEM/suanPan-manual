# MinimumGap3D

## Syntax

```text
constraint MinimumGap3D (1) (2) (3) (4)
# (1) int, unique constraint tag
# (2) int, node tag
# (3) int, node tag
# (4) double, gap
```

## Theory

This is a conditional constraint that limits the distance between two nodes, viz.,

$$
\left|\mathbf{x}_i+\mathbf{u}_i\-\mathbf{x}_j-\mathbf{u}_j\right|\geq{}D_{min}.
$$

The participating DoFs are `1`, `2`, and `3`.
