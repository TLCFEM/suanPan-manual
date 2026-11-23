# ElementalLee

Elemental Damping Using Lee's Formulation

## References

1. [10.1016/j.compstruc.2023.107152](https://doi.org/10.1016/j.compstruc.2023.107152)

!!! note
    This modifier must be used with [`LeeElementalNewmark`](../../Integrator/Implicit/Newmark/LeeElementalNewmark.md) integrator to work properly.

## Background

`ElementalLee` is the element-level form of the damping model described on the [`Modifier`](Modifier.md) page.
For each selected element it writes the scaled mass and stiffness matrices

$$
\zeta_e\,\boldsymbol M_e,\qquad
\zeta_e\big(\boldsymbol K_e+\boldsymbol K_{g,e}\big),
$$

where $\zeta_e$ is the element damping multiplier, $\boldsymbol M_e$ the current mass matrix, $\boldsymbol K_e$ the current tangent stiffness and $\boldsymbol K_{g,e}$ the geometric stiffness when `nlgeom` is active and a geometric matrix exists.
These containers are read by the companion integrator [`LeeElementalNewmark`](../../Integrator/Implicit/Newmark/LeeElementalNewmark.md) as the damping contributions of the Lee formulation.

The integrator defines a reference bell-shaped damping curve from a reference ratio and a peak frequency.
The damping ratio actually applied to an element is the product of that reference ratio and $\zeta_e$, so different parts of a structure can be assigned different damping levels.

!!! note "developer note"
    The modifier does not assemble a separate damping matrix.
    It overwrites the element mass and stiffness containers, which the companion integrator then interprets as damping contributions.

## Syntax

```text title="ElementalLee"
modifier ElementalLee (1) [2] [(3)...]
# (1) int, unique modifier tag
# [2] double, damping ratio, default: 0.02
# [(3)...] int, element tags
```

## Remarks

1. If no element tag is provided, this modifier applies to all active elements.
   In this case, it is equivalent to a global damping model such as [`LeeNewmark`](../../Integrator/Implicit/Newmark/LeeNewmark.md) or [`LeeNewmarkFull`](../../Integrator/Implicit/Newmark/LeeNewmarkFull.md).
2. Unlike the above global damping models, damping ratio is applied to each element individually.
   In case of an invalid number assigned, a default one $$0.02$$ is used.
3. The input value is converted to its absolute value, so a negative ratio has the same effect as a positive one.
4. Only elements that require a viscous update and permit modification of their viscous data are affected; an element such as [`Damper01`](../Special/Damper01.md) sets `modify_viscous` to false and is skipped.
5. Because the modified matrices are interpreted as damping by the special integrator, using this modifier with a standard Newmark integrator does not produce the intended damping.
