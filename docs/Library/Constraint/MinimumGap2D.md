# MinimumGap2D

## Syntax

```text
constraint MinimumGap2D (1) (2) (3) (4)
# (1) int, unique constraint tag
# (2) int, node tag
# (3) int, node tag
# (4) double, gap
```

## Theory

This is a conditional constraint that limits the distance between two nodes, viz.,

$$
\left|\mathbf{d}_i+\mathbf{u}_i-\mathbf{d}_j-\mathbf{u}_j\right|\geq{}D_{min}.
$$

The participating DoFs are `1` and `2`.
