# SubloadingViscous1D

Rate-Dependent Subloading Surface Model (1D)

The `SubloadingViscous1D` token extends the modified extended subloading surface model of [`Subloading1D`](Subloading1D.md) with a viscous (overstress) regularisation.
It makes the response depend on the loading rate and is convenient for modelling rate-sensitive cyclic behaviour.

## Theory

In addition to the normal yield ratio $$z$$, a viscous yield ratio $$z_v$$ is introduced and confined to $$z\leqslant z_v\leqslant c_v z$$.
It is obtained from an overstress relation that involves the viscosity $$\mu$$, the exponent $$n_v$$ and the time increment, so the model is rate dependent.
Viscosity is switched on only when both $$\mu>0$$ and $$n_v>0$$; with the defaults the model reduces to the rate-independent [`Subloading1D`](Subloading1D.md).
All other ingredients — the yield surface, isotropic and kinematic hardening, and the evolution of $$z$$ — are unchanged.

Writing the normalised viscous ratio as $$\zeta=z_v/z$$, the implicit overstress relation solved at each step is

$$
\zeta^{1/n_v}=1+\dfrac{\mu}{\Delta t}\left(c_v-\zeta\right)z\gamma .
$$

The ratio therefore grows from unity toward the upper bound $$c_v$$ as the plastic multiplier accumulates.
In the implementation the interval $$z\leqslant z_v\leqslant c_vz$$ is enforced by clamping after every Newton update, so the bound is respected even for parameter combinations that would otherwise overshoot.
The viscosity is scaled by the inverse of the time increment, and a unit increment is substituted when no positive increment is available.
The remaining two residuals of the implicit system are identical to those of [`Subloading1D`](Subloading1D.md).

!!! warning "implementation limitation"
    Setting either $\mu=0$ or $n_v=0$ removes viscosity entirely and the model reduces exactly to [`Subloading1D`](Subloading1D.md).
    With a unit time increment the viscosity has no physical time scale.
    The parser rejects a viscous limit $c_v$ below unity.

!!! info "deviation from theory"
    The standard Perzyna overstress is an explicit power law in the distance to the yield surface.
    Here the viscous ratio is bounded by $c_vz$ and is confined by clamping after every Newton update.
    Viscosity is scaled by $\mu/\Delta t$, so the response is tied to the analysis time increment.

## Syntax

```text title="SubloadingViscous1D"
material SubloadingViscous1D (1) [2-17] [18]
# (1) int, unique material tag
# [2] double, elastic modulus, default: 2E5
# [3] double, initial isotropic stress, default: 2E2
# [4] double, linear isotropic hardening modulus, default: 0.
# [5] double, isotropic saturation stress, default: 2E2
# [6] double, isotropic saturation rate, default: 1E1
# [7] double, initial kinematic stress, default: 2E2
# [8] double, linear kinematic hardening modulus, default: 0.
# [9] double, kinematic saturation stress, default: 2E2
# [10] double, kinematic saturation rate, default: 1E1
# [11] double, yield ratio evolution rate, u, default: 1E1
# [12] double, viscous limit, c_v, must be >=1, default: 1.
# [13] double, viscosity, mu, default: 0.
# [14] double, viscosity exponent, n_v, default: 0.
# [15] double, back-stress saturation rate, default: 1E1
# [16] double, elastic-core saturation rate, default: 1E1
# [17] double, elastic-core bound, default: 0.7
# [18] double, density, default: 0.0
```

## Remarks

The viscous limit $$c_v$$ must not be less than unity, and the evolution rates of the isotropic and kinematic bounds must be non-negative.
The viscosity is scaled by the inverse of the time increment; when no positive increment is available, a unit increment is used.
The elastic-core bound is capped just below unity.

All parameters are optional in the parser and take the defaults shown in the syntax block.
The default viscosity $$\mu=0$$ and exponent $$n_v=0$$ mean that a bare `SubloadingViscous1D` command behaves exactly like [`Subloading1D`](Subloading1D.md).
A larger $$c_v$$ permits a larger overstress and hence a stronger rate effect.
A larger $$\mu$$ or a smaller time increment increases the apparent rate sensitivity because the viscosity enters as $$\mu/\Delta t$$.
A single back-stress saturation with unit bound and a single elastic-core saturation are installed by this token, exactly as in [`Subloading1D`](Subloading1D.md).
The history layout is the four common slots of [`Subloading1D`](Subloading1D.md) plus one slot for the back stress and one for the elastic core.
Use [`VAFCRP1D`](VAFCRP1D.md) when viscosity should be applied to an Armstrong--Frederick backbone instead of a subloading surface.

## References

1. K. Hashiguchi, Subloading surface model in unconventional plasticity, *International Journal of Solids and Structures* 25 (1989) 917--945, [doi:10.1016/0020-7683(89)90038-3](https://doi.org/10.1016/0020-7683(89)90038-3).
2. P. Perzyna, Fundamental problems in viscoplasticity, *Advances in Applied Mechanics* 9 (1966) 243--377.
3. D. Perić, On a class of constitutive equations in viscoplasticity: formulation and computational issues, *International Journal for Numerical Methods in Engineering* 36 (1993) 1365--1393, [doi:10.1002/nme.1620360807](https://doi.org/10.1002/nme.1620360807).

## Example

```text
material SubloadingViscous1D 1 2E5 200 0 0 0 100 10 0 0 4E1 2 3E2 4 2E1 1E1 0
```
