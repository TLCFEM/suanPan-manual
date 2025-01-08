# BilinearDP

Bilinear Drucker-Prager Model

## Syntax

```
material BilinearDP (1) (2) (3) (4) (5) (6) (7) (8) [9]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, poissons ratio
# (4) double, \eta_y
# (5) double, \eta_f
# (6) double, \xi
# (7) double, initial cohesion, c_0
# (8) double, hardening ratio/modulus, H
# [9] double, density, default: 0.0
```

## Theory

See more details on the formulation in the parent [page](NonlinearDruckerPrager.md).

### Hardening Function

The cohesion develops linearly with the accumulated plastic strain,

$$
c=c_0+H\epsilon_p,
$$

in which $$c_0$$ is the initial cohesion (similar to the initial yield stress), $$H$$ is the hardening modulus, and $$\epsilon_p$$ is the accumulated plastic strain.

