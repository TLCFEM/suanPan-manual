# ParabolicCC

Parabolic Hardening Modified Cam-Clay Model

## Theory

This model defines a parabolic hardening rule for $$a(\alpha)$$, which is a non-negative function.

$$
a(\alpha)=a_0+H\alpha^2\ge0,
$$

in which $$H$$ is the hardening modulus, note $$\alpha=\varepsilon_p=\varepsilon_1+\varepsilon_2+\varepsilon_3$$ is the
volumetric plastic strain.

The hardening modulus could be either positive or negative.

**This hardening rule does not imply any physical soil behavior.**

## Syntax

```
material ParabolicCC (1) (2) (3) (4) (5) (6) (7) (8) [9]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, poissons ratio
# (4) double, beta, controls compression side shape
# (5) double, m, slope of CSL
# (6) double, p_t, initial tension strength
# (7) double, a_0, initial a_0
# (8) double, H, slope of hardening function
# [9] double, density, default: 0.0
```
