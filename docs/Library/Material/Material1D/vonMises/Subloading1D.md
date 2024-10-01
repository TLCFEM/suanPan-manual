# Subloading1D

The Modified Extended Subloading Surface (Hashiguchi) Model

The subloading surface framework provides a very versatile approach to model cyclic behaviour.
It is highly recommended to try it out.

## References

1. [10.1007/978-3-030-93138-4](https://doi.org/10.1007/978-3-030-93138-4)
2. [10.1007/s11831-023-10022-1](https://doi.org/10.1007/s11831-023-10022-1)
3. [10.1007/s11831-022-09880-y](https://doi.org/10.1007/s11831-022-09880-y)

Prof. Koichi Hashiguchi has published a large amount of papers on this topic.
To find more references, please refer to the monograph and the references therein.

Alternatively, refer to the corresponding section
in [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook/releases/download/latest/COOKBOOK.pdf)
for implementation details.

## Theory

### Subloading Surface

The subloadin surface is defined as

$$
f_s=|\eta|-z\sigma^y
$$

where $$\eta=\sigma-a^y\alpha+\left(z-1\right)\sigma^yd$$ is the shifted stress, shifted from the centre defined by $$a^y\alpha+\left(1-z\right)\sigma^yd$$.
The scalar $$0\leqslant{}z\leqslant{}1$$ is the normal yield ratio that provides a smooth transition from the interior to the normal yield surface.
The scalar $$\sigma^y$$ is the yield stress, that is affected by isotropic hardening.

### Isotropic Hardening

The isotropic hardening combines linear hardening and exponential saturation.

$$
\sigma^y=\sigma^i+k_\text{iso}q+\sigma^s_\text{iso}\left(1-e^{-m^s_\text{iso}q}\right)
$$

where $$\sigma^i$$ is the initial yield stress, $$k_\text{iso}$$ is the linear hardening modulus, $$\sigma^s_\text{iso}$$ is the saturation stress
and $$m^s_\text{iso}$$ is the hardening rate.

The history variable $$q$$ is the accumulated plastic strain, conventionally, it is

$$
\dot{q}=\gamma
$$

where $$\gamma$$ is the plasticity multiplier.

### Kinematic Hardening

A modified Armstrong--Frederick rule is adopted for the normalised back stress $$\alpha$$.

$$
\dot{\alpha}=b\gamma\left(n-\alpha\right)
$$

with

$$
a^y=a^i+k_\text{kin}q+a^s_\text{kin}\left(1-e^{-m^s_\text{kin}q}\right)
$$

where $$b$$ is hardening rate.
Compared to the conventional AF rule, the saturation bound is not a constant in this model.
Instead, it is associated to plasticity.
The backbone $$a^y$$ mimics $$\sigma^y$$.
The parameters $$a^i$$, $$k_\text{kin}$$, $$a^s_\text{kin}$$ and $$m^s_\text{kin}$$ share similar implications compared to their counterparts.

### Evolution of $$z$$

The following rule is used.
Noting that the original formulation uses a cotangent function.
Here, the logarithmic function is used instead.
Also, the original formulation sets a minimum value for $$z$$ ($$R$$ in the references).
We do not adopt such a limit.

$$
\dot{z}=-u\ln\left(z\right)\gamma.
$$

In which, $$u$$ is a constant that controls the rate of transition.

### Evolution of $$d$$

The evolution of $$d$$ resembles that of $$\alpha$$.

$$
\dot{d}=c_e\gamma\left(z_en-d\right)
$$

in which $$c_e$$ and $$z_e<1$$ are two constants.

## Syntax

```text
material ExpGurson1D (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) (11) (12) (13) (14) [15]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, initial isotropic stress, \sigma^i
# (4) double, linear isotropic hardening modulus, k_{iso}
# (5) double, isotropic saturation stress, \sigma^s
# (6) double, isotropic saturation rate, m^s_{iso}
# (7) double, initial kinematic stress, a^i
# (8) double, linear kinematic hardening modulus, k_{kin}
# (9) double, kinematic saturation stress, a^s
# (10) double, kinematic saturation rate, m^s_{kin}
# (11) double, yield ratio evolution rate, u
# (12) double, kinematic hardening rate, b
# (13) double, elastic core evolution rate, c_e
# (14) double, limit elastic core ratio, z_e
# [15] double, density, default: 0.0
```

## Example

See [this](../../../../Example/Structural/Statics/calibration-subloading.md) example.
