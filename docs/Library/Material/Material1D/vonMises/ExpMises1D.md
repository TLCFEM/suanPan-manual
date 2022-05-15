# ExpMises1D

Exponential Isotropic Hardening Model

The kinematic hardening is not defined in this model.

## Theory

The isotropic hardening backbone function is defined as

$$
\sigma=\sigma_y+a-ae^{-b\varepsilon_p}+cE\varepsilon_p,
$$

where $$a$$, $$b$$ and $$c$$ are three constants that control the shape of the backbone. The stiffness at the beginning of yielding is $$\sigma'|_
{\varepsilon_p=0}=ab+cE$$.

## Syntax

```
material ExpMises1D (1) (2) (3) (4) (5) (6) [7]
# (1) int, unique tag
# (2) double, elastic modulus
# (3) double, yield stress
# (4) double, a
# (5) double, b
# (6) double, c
# [7] double, density, default: 0
```
