# BilinearCC

Bilinear Hardening Modified Cam-Clay Model

## Theory

This model defines a bilinear hardening rule for $$a(\alpha)$$, which is a non-negative function.

$$
a(\alpha)=a_0+H\alpha\ge0,
$$

in which $$H$$ is the hardening modulus, note $$\alpha=\varepsilon_p=\varepsilon_1+\varepsilon_2+\varepsilon_3$$ is the
volumetric plastic strain.

The hardening modulus could be either positive or negative.

**This hardening rule does not imply any physical soil behavior.**

## Syntax

```
material BilinearCC (1) (2) (3) (4) (5) (6) (7) (8) [9]
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

## Iso-error Map

The following example iso-error maps are obtained via the following script.

```py
from plugins import ErrorMap
# note: the dependency `ErrorMap` can be found in the following link
# https://github.com/TLCFEM/suanPan-manual/blob/dev/plugins/scripts/ErrorMap.py

young_modulus = 1e5
yield_stress = 100.0
hardening_ratio = 0.05

with ErrorMap(
    f"material BilinearCC 1 {young_modulus} .4 .8 .8 {0.2 * yield_stress} {yield_stress} {hardening_ratio * young_modulus}",
    ref_strain=yield_stress / young_modulus,
    ref_stress=yield_stress,
    contour_samples=20,
) as error_map:
    error_map.contour("cam.clay.uniaxial", center=(-2, 0), size=1)
    error_map.contour("cam.clay.biaxial", center=(-2, -2), size=1)
```

![absolute error uniaxial](cam.clay.uniaxial.abs.error.svg)
![absolute error biaxial](cam.clay.biaxial.abs.error.svg)
