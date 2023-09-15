# ElasticOS

Isotropic Elastic Material For Open Sections

## Syntax

```
material ElasticOS (1) (2) (3) [4]
# (1) int, unique tag
# (2) double, elastic modulus
# (3) double, poissons ratio
# [4] double, density, default: 0.0
```

## Remarks

It has two DoFs. The elastic stiffness can be expressed as

$$
\mathbf{K}=\begin{bmatrix}
E&0\\
0&\dfrac{E}{2(1+\nu)}
\end{bmatrix}
$$
