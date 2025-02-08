# VAFCRP1D

Viscous J2 Steel Model

The `VAFCRP1D` model is the uniaxial version of the [`VAFCRP`](../../Material3D/vonMises/VAFCRP.md) model.

It adds viscosity on top of the [`ArmstrongFrederick1D`](ArmstrongFrederick1D.md).

## References

1. [10.1017/S0368393100118759](https://doi.org/10.1017/S0368393100118759)
2. [10.1179/096034007X207589](https://doi.org/10.1179/096034007X207589)
3. [10.1016/0749-6419(89)90015-6](https://doi.org/10.1016/0749-6419(89)90015-6)
4. [10.1002/nme.1620360807](https://doi.org/10.1002/nme.1620360807)

## Theory

The Peric (1993) type definition is used for viscosity.

$$
\dfrac{\gamma}{\Delta{}t}=\dot{\gamma}=\dfrac{1}{\mu}\left(\left(\dfrac{|\eta|}{k}\right)
^{\dfrac{1}{\epsilon}}-1\right),
$$

where $$\mu$$ and $$\epsilon$$ are two material constants that controls viscosity.
Note either $$\mu$$ or $$\epsilon$$ can be set to zero to disable rate-dependent response.
In that case this model is identical to the [`ArmstrongFrederick1D`](ArmstrongFrederick1D.md) model.

## Syntax

The following applies to `v3.6` and later.
Check the older syntax in the older version of the documentation.

```
material VAFCRP1D (1) (2) (3) (4) (5) (6) (7) (8) [(9) (10)...] [11]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, yield stress, \sigma^i
# (4) double, linear hardening modulus, K
# (5) double, saturation stress, \sigma^s
# (6) double, m^s, saturation rate
# (7) double, mu
# (8) double, epsilon
# (9) double, a
# (10) double, b
# [11] double, density, default: 0.0
```

## Examples

See [`VAFCRP`](../../Material3D/vonMises/VAFCRP.md).
