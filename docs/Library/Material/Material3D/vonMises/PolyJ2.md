# PolyJ2

Polynomial Hardening J2 Model

The `PolyJ2` defines a J2 material with isotropic hardening. The isotropic hardening is controlled by a polynomial. The
kinematic hardening is disabled.

## Syntax

```
material PolyJ2 (1) (2) (3) (4) [(5)...]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, poisson's ratio
# (4) double, density
# [(5)...] double, parameters in polynomial
```

## Example

The isotropic hardening function is defined to be a polynomial function of equivalent plastic strain.

$$
\sigma_y(\bar\varepsilon_p)=a_0+a_1\bar\varepsilon_p+a_2\bar\varepsilon_p^2+\cdots+a_n\bar\varepsilon_p^n.
$$

Clearly, $$a_0$$ is the initial yielding stress.

To define, for example, the following hardening

$$
\sigma_y(\bar\varepsilon_p)=100+4000\bar\varepsilon_p+80000\bar\varepsilon_p^3
$$

with $$E=200000$$ and $$\nu=0.3$$, the following command can be used.

```
material PolyJ2 1 2E5 .3 .0 1E2 4E3 0. 8E4
```
