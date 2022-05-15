# VAFCRP1D

Viscous J2 Steel Model

The `VAFCRP1D` model is the uniaxial version of the [`VAFCRP`](../../Material3D/vonMises/VAFCRP.md) model.

## Reference

1. [10.1017/S0368393100118759](https://doi.org/10.1017/S0368393100118759)
2. [10.1179/096034007X207589](https://doi.org/10.1179/096034007X207589)
3. [10.1016/0749-6419(89)90015-6](https://doi.org/10.1016/0749-6419(89)90015-6)
4. [10.1002/nme.1620360807](https://doi.org/10.1002/nme.1620360807)

## Theory

The `VAFCRP` model is a von Mises J2 yield criterion based model and uses an associative plasticity flow. The yield
function is defined as

$$
F=\Big|\sigma-\beta\Big|-k.
$$

So the plastic flow is

$$
\dot{\varepsilon}^p=\gamma\dfrac{\partial{}F}{\partial{}\sigma}=\gamma{}n,
$$

where $$n=\dfrac{\eta}{\Big|\eta\Big|}=\dfrac{\sigma-\beta}{\Big|\sigma-\beta\Big|}=\mathrm{sign}~\left(
\sigma-\beta\right)$$.

### V

The Voce (1955) type isotropic hardening equation is used.

$$
k=\sigma_y+k_s(1-e^{-mp})+k_lp,
$$

where $$\sigma_y$$ is the initial elastic limit (yielding stress), $$k_s$$ is the saturated stress, $$k_l$$ is the
linear hardening modulus, $$m$$ is a constant that controls the speed of hardening,
$$\mathrm{d}p=\Big|\mathrm{d}\varepsilon^p\Big|=\gamma$$ is the rate of accumulated plastic strain $$p$$.

### AF

The Armstrong-Frederick (1966) kinematic hardening rule is used. The rate form of back stress $$\beta^i$$ is

$$
\mathrm{d}\beta^i=a^i~\mathrm{d}\varepsilon^p-b^i\beta~\mathrm{d}p,
$$

where $$a^i$$ and $$b^i$$ are material constants.

### CR

A multiplicative formulation (Chaboche and Rousselier, 1983) is used for the total back stress.

$$
\beta=\sum\beta^i.
$$

### P

The Peric (1993) type definition is used for viscosity.

$$
\dfrac{\gamma}{\Delta{}t}=\dot{\gamma}=\dfrac{1}{\mu}\left(\left(\dfrac{\Big|\eta\Big|}{k}\right)
^{\dfrac{1}{\epsilon}}-1\right),
$$

where $$\mu$$ and $$\epsilon$$ are two material constants that controls viscosity. ***Note either $$\mu$$ or
$$\epsilon$$ can be set to zero to disable rate-dependent response, in that case this model is identical to the
Armstrong-Frederick model.***

## Syntax

```
material VAFCRP1D (1) (2) (3) (4) (5) (6) (7) (8) [(9) (10)...] [11]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, yield stress
# (4) double, saturated stress
# (5) double, linear hardening modulus
# (6) double, m
# (7) double, mu
# (8) double, epsilon
# (9) double, a
# (10) double, b
# [11] double, density, default: 0.0
```
