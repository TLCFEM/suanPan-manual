# MaximumGap2D

## Syntax

```text
constraint MaximumGap2D (1) (2) (3) (4)
# (1) int, unique constraint tag
# (2) int, node tag
# (3) int, node tag
# (4) double, gap
```

## Theory

This is a conditional constraint that limits the distance between two nodes, viz.,

$$
\left|\mathbf{x}_i+\mathbf{u}_i\-\mathbf{x}_j-\mathbf{u}_j\right|\leq{}D_{max}.
$$

The participating DoFs are `1` and `2`.
