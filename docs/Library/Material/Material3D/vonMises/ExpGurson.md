# ExpGurson

See also the corresponding section in [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook/releases/download/latest/COOKBOOK.pdf).

## Syntax

```
material ExpGurson (1) (2) (3) (4) (5) [6] [7] [8] [9] [10] [11]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, poissons ratio
# (4) double, yield stress
# (5) double, n
# [6] double, q1, default: 1.0
# [7] double, q2, default: 1.0
# [8] double, fn, default: 0.0
# [9] double, sn, default: 1.0
# [10] double, en, default: 0.0
# [11] double, density, default: 0.0
```

## Remarks

Due to that the yield function has the quadratic term $$q^2$$, it shall be noted that the unit of the model shall be
selected carefully. For example, if the yield stress is $$1000~\mathrm{MPa}$$ and $$\mathrm{Pascal}$$ is used as the
unit for stress, then the input number is $$10^9$$, the square of which is greater than $$10^{16}$$ so that the yield
function likely overflows.

## Iso-error Map

The following example iso-error maps are obtained via the following script.

```py
from plugins import ErrorMap
# note: the dependency `ErrorMap` can be found in the following link
# https://github.com/TLCFEM/suanPan-manual/blob/dev/plugins/scripts/ErrorMap.py

young_modulus = 2e2
yield_stress = .4

with ErrorMap(
    f"material ExpGurson 1 {young_modulus} .3 {yield_stress} .2 1. 1. 0.3 1. 0.02",
    ref_strain=yield_stress / young_modulus,
    ref_stress=yield_stress,
    contour_samples=20,
) as error_map:
    error_map.contour("exp.gurson.uniaxial", center=(-2, 0), size=1)
    error_map.contour("exp.gurson.biaxial", center=(-2, -2), size=1)
```

![absolute error uniaxial](exp.gurson.uniaxial.abs.error.svg)
![absolute error biaxial](exp.gurson.biaxial.abs.error.svg)
