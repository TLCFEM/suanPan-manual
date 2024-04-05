# DuncanSelig

Plane Strain Duncan-Selig Soil Model

## References

1. [10.3141/2511-07](https://doi.org/10.3141/2511-07)

## Syntax

```
material DuncanSelig (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) [11]
# (1) int, unique material tag
# (2) double, reference atmospheric pressure, postive, p_a
# (3) double, reference elatic modulus, E_r
# (4) double, elastic modulus exponent, n
# (5) double, reference bulk modulus, B_r
# (6) double, bulk modulus exponent, m
# (7) double, initial friction angle, \phi_i
# (8) double, friction angle slope, \Delta\phi
# (9) double, ratio of actual failure to ultimate failure, r_f
# (10) double, cohesion, c
# [11] double, density, default: 0.0
```

## Theory

The constitutive relationship can be expressed as

$$
\dot\sigma=\dfrac{3B}{9B-E}\begin{bmatrix}
3B+E&3B-E&0\\
3B-E&3B+E&0\\
0&0&E
\end{bmatrix}\dot\varepsilon.
$$

Note it is an incremental form of the constitutive relationship.
Symbols $$B$$ and $$E$$ denote bulk and elastic modulus, respectively.

The elastic modulus $$E$$ is a function of stress.

$$
E=E_i\left(1-\dfrac{\sigma_d}{\sigma_{d,max}}\right)^2,
$$

with

$$
E_i=E_r\left(\dfrac{\sigma_3}{p_a}\right)^n,\quad
\sigma_{d,max}=\dfrac{2}{r_f}\dfrac{c\cos\phi+\sigma_3\sin\phi}{1-\sin\phi}.
$$

The friction angle $$\phi$$ decreases with increasing $$\sigma_3$$.

$$
\phi=\phi_i-\Delta\psi\log_{10}\left(\dfrac{\sigma_3}{p_a}\right).
$$

The deviatoric stress $$\sigma_d$$ is the difference between the major and minor principal stresses.

$$
\sigma_d=\sigma_1-\sigma_3.
$$

The bulk modulus $$B$$ is a function of $$\sigma_3$$.

$$
B=B_r\left(\dfrac{\sigma_3}{p_a}\right)^m.
$$