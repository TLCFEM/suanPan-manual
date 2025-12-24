# Balloon

Balloon Model

The Balloon-v1 model is an advanced model for metals with enhanced cyclic behaviour.

## Syntax

```text
material Balloon ${1:(1)} ${2:(2)} ${3:(3)} ${4:(4)} ${5:(5)} ${6:(6 7 8 9)} ${7:(10 11 12 13)} ${8:(14 15 16 17)} ${9:(18 19 20 21)} ${10:(22 23 24 25)} ${11:(26)} ${12:[(27) (28) (29)...]}
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, poisson's ratio
# (4) double, k_r
# (5) double, load reversal memory size
# (6 7 8 9) double, u bound, initial, linear, saturation, rate
# (10 11 12 13) double, fm bound, initial, linear, saturation, rate
# (14 15 16 17) double, fc bound, initial, linear, saturation, rate
# (18 19 20 21) double, back stress bound, initial, linear, saturation, rate
# (22 23 24 25) double, similarity bound, initial, linear, saturation, rate
# (26) double, density
# (27) string, token, one of '-fc', '-ac', '-na', '-nd'
# (28 29) double, saturation, rate
```

## Iso-error Map

The Balloon-v1 model extends the subloading surface model and behaves in a similar way under monotonic loading.
The iso-error maps are thus similar to that of the subloading surface model.

The following example iso-error maps are obtained via the following script.

```py
from plugins import ErrorMap

# note: the dependency `ErrorMap` can be found in the following link
# https://github.com/TLCFEM/suanPan-manual/blob/dev/plugins/scripts/ErrorMap.py

young_modulus = 200
yield_stress = .24

with ErrorMap(
        fr'''
material Balloon 1 \
{young_modulus} .2 1e2 2 \
4E3 0 -3.6E3 5e2 \ ! u
{yield_stress} 0 0 0 \ ! hfm
0 0 .1 2e2 \ ! hfc
.02 0 0 0 \ ! ham
0 0 0 0 \ ! hac
0 \ ! density
-fc 5E0 1. \ ! fc
-na 1E2 1. \ ! na
-na 0 90. \ ! na
-nd 1E2 .8 ! nd
''',
        ref_strain=yield_stress / young_modulus,
        ref_stress=yield_stress,
        contour_samples=30,
) as error_map:
    error_map.contour("balloon.uniaxial", center=(-4, 0), size=5, type={"rel", "abs"})
    error_map.contour("balloon.biaxial", center=(-4, -4), size=5, type={"rel", "abs"})

```

![absolute error uniaxial](balloon.uniaxial.abs.error.svg)
![absolute error biaxial](balloon.biaxial.abs.error.svg)
![relative error uniaxial](balloon.uniaxial.rel.error.svg)
![relative error biaxial](balloon.biaxial.rel.error.svg)
