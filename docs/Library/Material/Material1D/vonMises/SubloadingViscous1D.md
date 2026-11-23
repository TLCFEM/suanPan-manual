# SubloadingViscous1D

Rate-Dependent Subloading Surface Model (1D)

The `SubloadingViscous1D` token extends the modified extended subloading surface model of [`Subloading1D`](Subloading1D.md) with a viscous (overstress) regularisation.
It makes the response depend on the loading rate and is convenient for modelling rate-sensitive cyclic behaviour.

## Theory

In addition to the normal yield ratio $$z$$, a viscous yield ratio $$z_v$$ is introduced and confined to $$z\leqslant z_v\leqslant c_v z$$.
It is obtained from an overstress relation that involves the viscosity $$\mu$$, the exponent $$n_v$$ and the time increment, so the model is rate dependent.
Viscosity is switched on only when both $$\mu>0$$ and $$n_v>0$$; with the defaults the model reduces to the rate-independent [`Subloading1D`](Subloading1D.md).
All other ingredients — the yield surface, isotropic and kinematic hardening, and the evolution of $$z$$ — are unchanged.

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

## Example

```text
material SubloadingViscous1D 1 2E5 200 0 0 0 100 10 0 0 4E1 2 3E2 4 2E1 1E1 0
```
