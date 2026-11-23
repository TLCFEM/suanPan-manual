# Viscosity01

Viscous Damper

The damping force is defined as a function of velocity (or strain rate, depending on what the input is).
This material model does not respond to strain/displacement.
To represent materials that respond to both displacement and velocity, see [`Maxwell`](Maxwell.md) and [`Kelvin`](Kelvin.md).

See this [example](../../../../Example/Structural/Dynamics/dynamic-analysis-of-a-portal-frame.md).

See also damper elements [`Damper01`](../../../Element/Special/Damper01.md) and [`Damper02`](../../../Element/Special/Damper02.md).

$$
\sigma=\text{sign}(\dot\varepsilon)~\eta~|\dot\varepsilon|^\alpha.
$$

The damping coefficient is constant.

## Syntax

```text title="Viscosity01"
material Viscosity01 (1) (2) (3) [4]
# (1) int, unique tag
# (2) double, alpha
# (3) double, damping coefficient
# [4] double, limit, default: 1.0
```

## Theory

The model is a pure dashpot whose force depends only on the current strain rate $v=\dot\varepsilon$.

$$
\sigma=\operatorname{sign}(v)\,\eta\,|v|^\alpha.
$$

For $\alpha=1$ this is the linear viscous law $\sigma=\eta v$, for $\alpha<1$ the response is shear thinning and for $\alpha>1$ it is shear thickening.
The coefficient $\eta$ has units of stress times time to the power $\alpha$ per strain to the power $\alpha$, so its numerical value depends on the chosen exponent.
The tangent damping is

$$
c=\dfrac{\mathrm d\sigma}{\mathrm dv}=\eta\alpha|v|^{\alpha-1},
$$

with the cubic regularisation of [`NonlinearViscosity`](NonlinearViscosity.md) applied when $0<\alpha<1$ and $|v|$ is below the cut-off $L$ given by the optional fourth argument.
Passing $\alpha=0$ does not produce a power-law dashpot in this framework, because the stress then equals the constant $\eta$ and is independent of the sign of the rate.
That degenerate setting is intended for derived classes such as [`BilinearViscosity`](BilinearViscosity.md) and [`CustomViscosity`](CustomViscosity.md).
There is no strain dependence, so the model contributes no tangent stiffness.

!!! info "deviation from theory"
    For $0<\alpha<1$ and $|v|<L$ the power law is replaced by a cubic polynomial, so the tangent damping is finite at zero velocity instead of singular.
    For $\alpha=0$ the stress is constant and independent of the sign of velocity, which is a framework convention rather than a dashpot law.

!!! note "developer note"
    The $\alpha=0$ convention is defined in the base class.

## Remarks

The exponent `(2)`, the damping coefficient `(3)` and the cut-off `[4]` are all converted to absolute values, so their signs do not matter.
The cut-off defaults to 1.0 and is inactive for $\alpha\ge1$.
Typical fluid dampers use $\alpha$ between 0.3 and 1.0, with $\alpha=1$ giving a linear damper.
A small $\alpha$ gives a nearly rate-independent force but widens the regularised transition near zero velocity.
The material must be attached to an element that passes strain rate, such as [`Damper01`](../../../Element/Special/Damper01.md) or [`Damper02`](../../../Element/Special/Damper02.md).
For a damping coefficient that changes with displacement use [`Viscosity02`](Viscosity02.md).
For a force with a yield plateau use [`BilinearViscosity`](BilinearViscosity.md) or [`CoulombFriction`](CoulombFriction.md).

## References

1. [10.1016/j.ymssp.2021.108795](https://doi.org/10.1016/j.ymssp.2021.108795)
