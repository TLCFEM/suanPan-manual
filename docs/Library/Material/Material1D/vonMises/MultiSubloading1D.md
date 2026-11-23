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

## Remarks

Unlike [`Subloading1D`](Subloading1D.md), where density is optional and a single saturation is used for each quantity, density is mandatory here and each saturation set is given explicitly.
The evolution rates of the isotropic and kinematic bounds must be non-negative.

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
