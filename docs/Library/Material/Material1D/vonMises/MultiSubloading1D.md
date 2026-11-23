# MultiSubloading1D

Multiple-Saturation Subloading Surface Model (1D)

The `MultiSubloading1D` token implements the same modified extended subloading surface framework as [`Subloading1D`](Subloading1D.md), but allows several user-defined saturation terms for the back stress and the elastic core.
This is useful when a single exponential saturation cannot reproduce the observed cyclic response.

## Theory

The yield surface, isotropic hardening and the evolution of the normal yield ratio $$z$$ are identical to those of [`Subloading1D`](Subloading1D.md).
The back stress and the normalised elastic core are instead assembled from independent Armstrong--Frederick type saturations,

$$
\dot\alpha_i=r_i\left(b_i n-\alpha_i\right),\qquad
\dot d_j=r_j\left(b_j n-d_j\right),
$$

so that each term saturates exponentially toward its bound and the total saturation is the sum of the individual contributions.
Each term is defined by one rate and one bound.
If no `-back` or `-core` group is supplied, the corresponding quantity vanishes.

Each saturation is integrated with backward Euler together with the plastic multiplier $$\gamma$$,

$$
\alpha_i=\dfrac{\alpha_i^n+r_ib_i\,n\gamma}{1+r_i\gamma},\qquad d_j=\dfrac{d_j^n+r_jb_j\,n\gamma}{1+r_j\gamma},
$$

where $$n$$ is the direction of the shifted stress.
The symbols $$b_i$$ and $$b_j$$ here are the per-term saturation bounds and are not the kinematic hardening rate $$b$$ of the syntax block.
The total normalised quantities are $$\alpha=\sum_i\alpha_i$$ and $$d=\sum_jd_j$$, so choosing bounds that sum to unity recovers the single-saturation response of [`Subloading1D`](Subloading1D.md).
The implicit residual system is the same three-equation system as in [`Subloading1D`](Subloading1D.md), with the sums above replacing the single terms.

!!! info "deviation from theory"
    The code does not normalise the saturation bounds, so the user must choose them so that each group sums to a meaningful total.
    The logarithmic evolution of the normal yield ratio and its numerical floor are inherited unchanged from [`Subloading1D`](Subloading1D.md).
    This token reuses the same `Subloading1D` C++ class as the single-saturation model.

## Syntax

```text title="MultiSubloading1D"
material MultiSubloading1D (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) (11) (12) [-back (13) (14)] ... [-core (15) (16)] ...
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, initial isotropic stress, \sigma^i>=0
# (4) double, linear isotropic hardening modulus, k_{iso}>=0
# (5) double, isotropic saturation stress, \sigma^s>=0
# (6) double, isotropic saturation rate, m^s_{iso}>=0
# (7) double, initial kinematic stress, a^i>=0
# (8) double, linear kinematic hardening modulus, k_{kin}>=0
# (9) double, kinematic saturation stress, a^s>=0
# (10) double, kinematic saturation rate, m^s_{kin}>=0
# (11) double, yield ratio evolution rate, u>=0
# (12) double, density
# -back (13) (14): add a back-stress saturation, (13) rate, (14) bound
# -core (15) (16): add an elastic-core saturation, (15) rate, (16) bound
```

All twelve numerical arguments are compulsory.
The `-back` and `-core` groups may appear in any order and may be repeated.

!!! warning "implementation limitation"
    The parser reads all twelve numbers with strict parsing, including the density at position `(12)`.
    An omitted density causes a parse error rather than defaulting to zero.
    The number of `-back` and `-core` groups determines the amount of allocated history space.

## Remarks

Unlike [`Subloading1D`](Subloading1D.md), where density is optional and a single saturation is used for each quantity, density is mandatory here and each saturation set is given explicitly.
The evolution rates of the isotropic and kinematic bounds must be non-negative.
All eleven numerical inputs before the token groups are read with strict parsing, so none of them may be omitted.
The bounds supplied to `-back` and `-core` are commonly chosen so that each group sums to unity.
A larger rate makes the corresponding term saturate over a shorter plastic strain interval, so mixing rates is a practical way to fit both early and late cyclic hardening.
The history layout is the common four slots of [`Subloading1D`](Subloading1D.md) followed by one slot per back-stress term and one slot per elastic-core term.
The consistent tangent is obtained by the same static condensation of the Newton Jacobian as in [`Subloading1D`](Subloading1D.md).

## References

1. K. Hashiguchi, Subloading surface model in unconventional plasticity, *International Journal of Solids and Structures* 25 (1989) 917--945, [doi:10.1016/0020-7683(89)90038-3](https://doi.org/10.1016/0020-7683(89)90038-3).
2. The implementation paper cited in [`Subloading1D`](Subloading1D.md), [doi:10.1007/s00707-025-04339-0](https://doi.org/10.1007/s00707-025-04339-0).

## Example

```text
material MultiSubloading1D 1 2E5 \
200 10 50 10 \
200 10 50 10 \
8E2 0. \
-back 10 .6 -back 1E2 .3 -back 5E2 .1 \
-core 10 .3 -core 1E2 .4

materialTest1D 1 1E-4 100 200 200
```
