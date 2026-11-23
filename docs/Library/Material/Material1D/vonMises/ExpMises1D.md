# ExpMises1D

Exponential Isotropic Hardening Model

The kinematic hardening is not defined in this model.

## Theory

The isotropic hardening backbone function is defined as

$$
\sigma=\sigma_y+a-ae^{-b\varepsilon_p}+cE\varepsilon_p,
$$

where $$a$$, $$b$$ and $$c$$ are three constants that control the shape of the backbone.
The stiffness at the beginning of yielding is $$\sigma'|_{\varepsilon_p=0}=ab+cE$$.

!!! warning "implementation limitation"
    The constructor replaces the yield stress and all three constants by their absolute values.
    A negative input cannot be used to encode softening or a reversed saturation direction.
    The back stress is identically zero, so the yield surface only expands and never translates.

It can be identified that

1. $$a$$ represents the saturation stress.
2. $$b$$ controls the rate of saturation.
3. $$c$$ represents the linear hardening ratio (w.r.t. plastic strain).

The isotropic radius passed to the [`Mises1D`](Mises1D.md) base class is exactly this backbone, $$k(\varepsilon_p)=\sigma+a-ae^{-b\varepsilon_p}+cE\varepsilon_p$$, and the kinematic part vanishes.
Its derivative is

$$
\dfrac{\mathrm{d}k}{\mathrm{d}\varepsilon_p}=abe^{-b\varepsilon_p}+cE.
$$

This derivative enters the Newton denominator of the return mapping and the consistent tangent $$E^{ep}=E\,k'/(E+k')$$.
At large plastic strain the exponential term decays and the response approaches linear hardening with slope $$cE$$.

## Syntax

```text title="ExpMises1D"
material ExpMises1D (1) (2) (3) (4) (5) (6) [7]
# (1) int, unique tag
# (2) double, elastic modulus
# (3) double, yield stress
# (4) double, a, saturation stress
# (5) double, b, saturation rate
# (6) double, c, linear hardening ratio
# [7] double, density, default: 0
```

## Remarks

All four material constants `(3)`--`(6)` are converted to absolute values in the constructor.
The parameter $$b$$ has units of inverse plastic strain, while $$a$$ and $$\sigma_y$$ have units of stress and $$c$$ is dimensionless.
Setting $$a=0$$ leaves pure linear hardening with ratio $$c$$, and setting $$c=0$$ gives a purely saturating backbone.
With $$a=c=0$$ the model reduces to a perfectly plastic von Mises material.
Because the kinematic part is identically zero, the model cannot reproduce the Bauschinger effect; use [`ArmstrongFrederick1D`](ArmstrongFrederick1D.md) or [`Subloading1D`](Subloading1D.md) for cyclic loading.
The hardening law is evaluated only at the accumulated plastic strain, so the stress--strain envelope is identical in tension and compression.

## References

1. J. C. Simo and T. J. R. Hughes, *Computational Inelasticity*, Springer, New York, 1998, Section 1.4.4, [doi:10.1007/b98904](https://doi.org/10.1007/b98904).
