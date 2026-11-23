# CustomDP

Drucker-Prager Model With Custom Hardening

## Background

This model shares the yield function, plastic potential and return mapping of [`NonlinearDruckerPrager`](NonlinearDruckerPrager.md),

$$
F=\sqrt{J_2}+\eta_y p-\xi c(\bar\varepsilon_p),\qquad
\Phi=\sqrt{J_2}+\eta_f p,\qquad
\bar\varepsilon_p=\xi\gamma,
$$

where $c(\bar\varepsilon_p)$ is supplied by a user expression.
At every local iteration the solver calls the expression once for its value and once for its gradient with respect to the accumulated plastic strain.
Both the value and the derivative enter the consistency equation, so a wrong or discontinuous derivative degrades the quadratic convergence of the local Newton loop.

!!! warning "implementation limitation"
    The expression must have exactly one input and one output and must be able to evaluate its analytical gradient.
    Tabulated or finite-difference-only expressions are not accepted, and [`BilinearDP`](BilinearDP.md) or [`ExpDP`](ExpDP.md) should be used for closed-form laws without an expression engine.

## Syntax

```text title="CustomDP"
material CustomDP (1) (2) (3) (4) (5) (6) (7) [8]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, \eta_y
# (5) double, \eta_f
# (6) double, \xi
# (7) unsigned, cohesion expression tag
# [8] double, density, default: 0.0
```

***The expressions shall be able to compute derivatives.***

## Remarks

- The expression tag is read as an unsigned integer before the numeric arguments; all six numeric arguments are required and density defaults to zero.
- Initialization fails if the expression tag cannot be found or if the expression is not a univariate function.
- The law should return a non-negative cohesion; negative values are not clamped and would move the apex of the cone across the origin.
- This variant inherits no tension cutoff from the base class; only the cone apex limits tensile stress.
- Use [`BilinearDP`](BilinearDP.md) for a piecewise linear law and [`ExpDP`](ExpDP.md) for the exponential hardening--softening law.

## References

1. Mechanics of thermo-elastic-plastic materials with a thermoelastic-plastic change in volume
