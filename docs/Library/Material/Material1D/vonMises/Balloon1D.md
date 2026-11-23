# Balloon1D

Uniaxial Balloon Model

Both this model and [Balloon3D](../../Material3D/vonMises/Balloon.md) share the same definitions of parameters.
Both models shall yield the same uniaxial behaviour if the same parameter set is used.

## References

1. [10.31224/6937](https://doi.org/10.31224/6937)

## Syntax

```text title="Balloon1D"
material Balloon1D (1) (2...24) (25) [(26) (27) (28)...]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, k_r
# (4) double, load reversal memory size
# (5 6 7 8) double, u bound, initial, linear, saturation, rate
# (9 10 11 12) double, fm bound, initial, linear, saturation, rate
# (13 14 15 16) double, fc bound, initial, linear, saturation, rate
# (17 18 19 20) double, am bound, initial, linear, saturation, rate
# (21 22 23 24) double, ac bound, initial, linear, saturation, rate
# (25) double, density
# (26) string, token, one of '-fc', '-ac', '-na', '-nd', '-memory'
# (27 28) double, saturation and rate, omitted for '-memory'
```

## Theory

See [Balloon3D](../../Material3D/vonMises/Balloon.md) for more details.

The model uses the subloading surface idea of [`Subloading1D`](Subloading1D.md), in which a normal yield ratio $$0\leqslant z\leqslant1$$ gives a smooth elastic--plastic transition.
The scalar bounds all share the form

$$
\chi(q)=\chi_0+kq+\chi_s\left(1-e^{-rq}\right),
$$

where $$q$$ is the accumulated plastic strain.
The five bounds `u`, `fm`, `fc`, `am` and `ac` control the yield-ratio evolution rate, the monotonic isotropic and kinematic bounds, and their cyclic (reversal-dependent) counterparts.
The cyclic bounds are multiplied by Armstrong--Frederick type saturations,

$$
h_{fc,i}=\dfrac{a_i\gamma(1-k_m)f_c+h_{fc,i}^n}{1+b_i\gamma(1-k_m)},\qquad h_c=f_c+\sum_i h_{fc,i},
$$

and similarly for the kinematic side.
Here $$f_c$$ and $$a_c$$ are the scalar bounds, and the optional `-fc`, `-ac`, `-na` and `-nd` groups supply the saturation bounds and rates.

The axial subloading surface and the evolution of $$z$$ are

$$
f_s=\left|\sigma-h_a\sum_i n_i+(1-z)h_f\sum_j d_j\right|-zh_f=0,
$$

$$
h_f\left(z-z_\text{start}\right)-\gamma u\ln\dfrac{1}{z}=0.
$$

The split ratio $$k_r$$ and the memory buffer of past $$z$$ values define a reference value $$z_r$$, and the fraction of plastic strain feeding the memory variable is

$$
k_m=1-\exp\left[\dfrac{z-z_r}{(z-1)k_r}\right]\quad\text{for }z>z_r.
$$

This memory branch is the feature that gives the Balloon model its enhanced cyclic behaviour compared with the plain subloading surface model.

!!! info "deviation from theory"
    The reference $z_r$ is chosen as the minimum, maximum or mean of past normal yield ratios.
    It is not obtained from a continuously integrated plastic-strain memory surface.

!!! note "developer note"
    The reference $z_r$ is extracted from a finite ring buffer of past normal yield ratios.
    The one-dimensional model uses scalar back-stress and elastic-core variables, while the three-dimensional formulation uses tensor-valued quantities.

The implicit system is solved for the plastic multiplier and $$z$$ by Newton iteration, and the consistent tangent is formed by condensing the $$z$$ equation out of the Jacobian.
A special check at the beginning of the step detects elastic unloading and updates $$z$$ without plastic flow.

## Remarks

All twenty-three numerical inputs and the density are compulsory in the parser.

!!! warning "implementation limitation"
    An incomplete parameter list causes a parse error rather than reverting to defaults.
    The `-memory` group takes a type name and not a saturation bound and rate.

!!! note "developer note"
    The load-reversal memory size is cast to an unsigned integer without a range check.

The load reversal memory size is converted to an unsigned integer and the memory type defaults to `mean`.
The `-memory` group takes one of `minimum`, `maximum` or `mean` and does not take saturation or rate numbers.
Multiple `-fc`, `-ac`, `-na` and `-nd` groups may be supplied and their contributions are summed.
A saturation bound of unity with a positive rate is the usual choice for the cyclic groups, so that they approach the corresponding scalar bound.
The split ratio $$k_r$$ is dimensionless and controls how quickly the memory effect develops; a small value makes the transition sharp.
The three-dimensional counterpart [Balloon](../../Material3D/vonMises/Balloon.md) uses the same parameters and should give the same uniaxial response.
Because the model uses the logarithmic evolution of $$z$$, it inherits the smooth elastic--plastic transition and the need for a converged local Newton solution from [`Subloading1D`](Subloading1D.md).
