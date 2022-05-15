# ExpJ2

Exponential Isotropic Hardening J2 Model

The kinematic hardening is not defined in this model.

## Theory

The backbone function is defined as

$$
\sigma=\sigma_y\left(\left(1+a\right)e^{-b\varepsilon_p}-ae^{-2b\varepsilon_p}\right),
$$

where $$a$$ and $$b$$ are two constants that control the shape of the backbone. The initial stiffness $$\sigma'|_
{\varepsilon_p=0}=\sigma_y(a-1)b$$.

## Syntax

```
material ExpJ2 (1) (2) (3) (4) (5) (6) [7]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, poissons ratio
# (4) double, yield stress
# (5) double, a
# (6) double, b
# [7] double, density, default: 0.0
```