# ElementalLee

Elemental Damping Using Lee's Formulation

## Reference

1. [10.1016/j.compstruc.2023.107152](https://doi.org/10.1016/j.compstruc.2023.107152)

!!! Note
    This modifier must be used with [`LeeElementalNewmark`](../../../Library/Integrator/Newmark/LeeElementalNewmark.md)
    integrator to work properly.

## Syntax

```text
modifier ElementalLee (1) (2) [(3)...]
# (1) int, unique modifier tag
# (2) double, damping ratio
# [(3)...] int, element tags
```

## Remarks

1. If no element tag is provided, this modifier applies to all active elements.
   In this case, it is equivalent to a global damping model such
   as [`LeeNewmark`](../../../Library/Integrator/Newmark/LeeNewmark.md)
   or [`LeeNewmarkFull`](../../../Library/Integrator/Newmark/LeeNewmarkFull.md).
2. Unlike the above global damping models, damping ratio is applied to each element individually. In case of an invalid
   number assigned, a default one $$0.02$$ is used.
