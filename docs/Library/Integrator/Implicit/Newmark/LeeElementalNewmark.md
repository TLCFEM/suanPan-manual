# LeeElementalNewmark

Newmark Algorithm With Lee Damping Model (Elemental Type 0 Only)

Please check the references for theory.

1. [10.1016/j.jsv.2020.115312](https://doi.org/10.1016/j.jsv.2020.115312)
2. [10.1016/j.engstruct.2020.110178](https://doi.org/10.1016/j.engstruct.2020.110178)
3. [10.1016/j.compstruc.2023.107152](https://doi.org/10.1016/j.compstruc.2023.107152)

**For the moment, MPC cannot be considered in all global damping models.**

!!! Note
    This integrator must be used with [`ElementalLee`](../../../Element/Modifier/ElementalLee.md)
    modifier to work properly.

## Syntax

```
integrator LeeElementalNewmark (1) (2) (3) ((4) (5)...)
# (1) int, unique integrator tag
# (2) double, alpha
# (3) double, beta
# (4) double, reference damping ratio \zeta_p at the peak of each mode
# (5) double, circular frequency \omega_p at the peak of each mode
```

See also [LeeNewmark](LeeNewmark.md)
and [LeeNewmarkFull](LeeNewmarkFull.md).

The actually damping ratio applied is the product of the reference damping ratio and the ratio defined in each modifier.
