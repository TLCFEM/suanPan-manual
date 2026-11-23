# CustomStrainDegradation

Strain History Based Degradation With Custom Rules

This model implements the [universal damage model](Degradation.md) assuming the degradation factor depends on the strain history.

## Background

This wrapper is the strain-driven member of the [degradation family](Degradation.md).
It delegates the intact response to a host material and scales the stress by a factor that evolves with extreme strains.
The wrapper records the maximum tensile strain $$\varepsilon_{\max}$$ and the minimum compressive strain $$\varepsilon_{\min}$$ of the whole history.
The degradation factor in tension is $$D_+=D_+(\varepsilon_{\max})$$ and in compression is $$D_-=D_-(\varepsilon_{\min})$$.
On a new extreme the tangent stiffness follows the strain-dependent chain rule given in [`Degradation`](Degradation.md),

$$
K=D\bar K+\bar\sigma\frac{\mathrm{d}D}{\mathrm{d}\varepsilon_{\text{ext}}},
$$

whereas on unloading or reloading below the previous extreme the derivative term vanishes and $$K=D\bar K$$.

## Syntax

```text title="CustomStrainDegradation"
material CustomStrainDegradation (1) (2) (3) [4]
# (1) int, unique material tag
# (2) int, host intact material tag
# (3) int, tension degradation expression tag
# [4] int, compression degradation expression tag, default: (3)
```

## Usage

The usage of `CustomStrainDegradation` is identical to [`CustomStressDegradation`](CustomStressDegradation.md).

The degradations for positive/negative strains are defined separately.

$$
D_{pos}=D_{pos}(\varepsilon_{max}),\quad
D_{neg}=D_{neg}(\varepsilon_{min}).
$$

Here $$\varepsilon_{max}$$ is the maximum strain (positive) of the whole loading history, and $$\varepsilon_{min}$$ is the minimum strain (negative) of the whole loading history.

## Remarks

The host material tag `(2)` must refer to an already defined one-dimensional material.
The tension expression `(3)` and optional compression expression `(4)` must each take one scalar input and return a vector of two scalars, namely the degradation factor and its derivative with respect to that input.
If the compression expression is omitted, the tension expression is reused with the absolute value of the strain as input and the derivative negated, giving a symmetric law.

!!! info "deviation from theory"
    When the compression expression is omitted, the tension expression is evaluated with the absolute value of the strain and its derivative is negated.
    A single expression therefore always defines a symmetric law in $|\varepsilon|$, even if the expression itself is asymmetric.

!!! note "developer note"
    The default case is handled by `compute_negative_degradation`, which calls the tension expression with `fabs(t_strain)` and flips the sign of the returned derivative.

The branch is selected by the sign of the intact stress from the host material, not by the sign of the strain.

!!! warning "implementation limitation"
    The tension or compression envelope is selected by the sign of the undamaged stress returned by the host, not by the sign of the strain.
    A host with a compression offset or a non-symmetric backbone can therefore route a strain of a given sign to the opposite envelope.
    The envelope variable is updated only when the strain moves further in the direction selected by that stress sign.

!!! note "developer note"
    `StrainDegradation::update_trial_status` tests `trial_stress(0) > 0` against the undamaged stress returned by the host.

The wrapper inherits the density of the host material and records the two degradation factors as `DT` and `DC`.
See [`CustomStressDegradation`](CustomStressDegradation.md) for the stress-driven counterpart and [`TrilinearStrainDegradation`](TrilinearStrainDegradation.md) for a built-in piecewise law.
