# ExpDP

Exponential Drucker-Prager model

## Background

This model uses the yield function and return mapping of [`NonlinearDruckerPrager`](NonlinearDruckerPrager.md),

$$
F=\sqrt{J_2}+\eta_y p-\xi c(\bar\varepsilon_p),\qquad
\Phi=\sqrt{J_2}+\eta_f p,
$$

where $J_2=\frac12\boldsymbol s:\boldsymbol s$ is the second deviatoric invariant, $p=\frac13\mathrm{tr}\,\boldsymbol\sigma$ is the hydrostatic stress and $\bar\varepsilon_p=\xi\gamma$ is the accumulated plastic strain.
The cohesion follows the exponential law introduced for concrete by Lubliner et al.,

$$
c(\kappa)=c\left[\left(1+a\right)e^{-b\kappa}-a\,e^{-2b\kappa}\right],
$$

where $\kappa$ denotes $\bar\varepsilon_p$, $a$ is the shape parameter (8) and $b$ is the decay parameter (9).
For $a=0$ the law reduces to simple exponential decay $c\,e^{-b\kappa}$.
For $a>1$ the cohesion first increases and then softens, which reproduces the hardening--softening shape of a confined compressive backbone.
The peak occurs at $\kappa=\ln[2a/(1+a)]/b$ and equals $c\,(1+a)^2/(4a)$.

!!! info "deviation from theory"
    When $a>1$ the input cohesion (7) is interpreted as the peak value and is rescaled to $c\,4a/(1+a)^2$.
    When $a\le1$ the input is used directly as the initial cohesion.
    This rescaling mirrors the compression-strength normalisation in [`CDP`](../Concrete/CDP.md) but differs from the raw coefficient of the published exponential law.

## Syntax

```text title="ExpDP"
material ExpDP (1) (2) (3) (4) (5) (6) (7) (8) (9) [10]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, \eta_y
# (5) double, \eta_f
# (6) double, \xi
# (7) double, cohesion
# (8) double, cohesion_a
# (9) double, cohesion_b
# [10] double, density, default: 0.0
```

## Remarks

- All nine numeric arguments are required; only the density is optional and defaults to zero.
- The parameters $\eta_y$ and $\eta_f$ are dimensionless pressure sensitivities, not friction angles; use the fitting formulas on the [`NonlinearDruckerPrager`](NonlinearDruckerPrager.md) page to obtain them from a friction angle and cohesion.
- With $\eta_f=\eta_y$ the flow is associative and the tangent is symmetric; otherwise a nonsymmetric solver is recommended.
- The parameter $b$ controls the rate of degradation and has units of inverse plastic strain.
- A negative $b$ gives exponential growth of cohesion, which can lead to unbounded hardening and should be used with care.
- The cohesion is not clamped at zero, so the softening branch approaches zero asymptotically rather than truncating sharply as in [`BilinearDP`](BilinearDP.md).
- This class inherits no tension cutoff or compression cap from the base class.

## References

1. [10.1016/0020-7683(89)90050-4](https://doi.org/10.1016/0020-7683(89)90050-4)
2. Mechanics of thermo-elastic-plastic materials with a thermoelastic-plastic change in volume
