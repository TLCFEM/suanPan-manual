# ExpCC

Exponential Hardening Cam-Clay Model

This hardening law is identical to the one documented in ABAQUS manual (4.4.3).

## Hardening

The hardening function is defined as

$$
a=a_0\exp\left(\left(1+e_0\right)\dfrac{1-\alpha}{\lambda-\kappa\alpha}\right),
$$

where $$e_0$$ is the initial void ratio, $$\lambda$$ and $$\kappa$$ are material constants.

If experimental data is available, $$a_0$$ can be determined as

$$
a_0=\dfrac{1}{2}\exp\left(\dfrac{e_1-e_0-\kappa\ln{}p_0}{\lambda-\kappa}\right)
$$

where $$p_0$$ is the initial value of the equivalent pressure stress and $$e_1$$ is the intercept of the virgin
consolidation line with the void ratio axis in a plot of void ratio versus equivalent pressure stress.

## Syntax

```
material ExpCC (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) [11]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, poissons ratio
# (4) double, beta, controls compression side shape
# (5) double, m, slope of CSL
# (6) double, p_t, initial tension strength
# (7) double, a_0, initial a_0
# (8) double, e_0, initial void ratio
# (9) double, lambda
# (10) double, kappa
# [11] double, density, default: 0.0
```

## Usage
