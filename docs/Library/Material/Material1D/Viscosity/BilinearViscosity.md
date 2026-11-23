# BilinearViscosity

Viscous Material Using Bilinear Model

Reference:

1. [10.1016/j.soildyn.2018.06.021](https://doi.org/10.1016/j.soildyn.2018.06.021)

## Syntax

```text title="BilinearViscosity"
material BilinearViscosity (1) (2) (3) [4]
# (1) int, unique material tag
# (2) double, damping coefficient
# (3) double, yield stress
# [4] double, hardening ratio, default: 0
```

## Background

`BilinearViscosity` is a dashpot obtained from the [`NonlinearViscosity`](NonlinearViscosity.md) framework by fixing the power-law exponent at zero, so that the returned viscosity is the stress itself.
Let $v=\dot\varepsilon$ be the strain rate, $C$ the initial damping coefficient, $S$ the yield force and $H$ the hardening ratio.
The yield velocity is

$$
v_y=\dfrac{S}{C}.
$$

The stress is bilinear in $v$,

$$
\sigma(v)=\begin{cases}
C v, & |v|\le v_y,\\[2mm]
\operatorname{sign}(v)\left[S+C H\left(|v|-v_y\right)\right], & |v|>v_y.
\end{cases}
$$

The tangent damping $c=\mathrm d\sigma/\mathrm dv$ equals $C$ below the yield velocity and $C H$ above it.
There is no dependence on strain, so the model contributes no tangent stiffness.
For $H=0$ the force saturates at $S$ and the law becomes an elastic-perfectly-plastic dashpot, which is the bilinear oil-damper idealisation studied by Akcelyan et al. (2018).

!!! info "deviation from theory"
    The post-yield slope is not an independent input.
    The constructor forms it as $|C|H$, so $H$ is a fraction of the initial damping coefficient rather than a second viscosity.
    There is no internal state or return mapping, so the yield force does not evolve with cyclic loading.

## Remarks

The damping coefficient `(2)` and the yield force `(3)` are converted to absolute values in the constructor, whereas the hardening ratio `(4)` is not.
The coefficient $C$ has units of stress times time per strain when the element supplies strain rate, and $S$ has units of stress.
The hardening ratio is dimensionless, defaults to zero and is normally chosen as a small positive fraction of unity.
A negative hardening ratio is accepted and gives a softening post-yield branch, but it should be used with care because it can lead to a negative tangent damping.
The dashpot has no static stiffness and must be used with an element that passes strain rate, such as [`Damper01`](../../../Element/Special/Damper01.md) or [`Damper02`](../../../Element/Special/Damper02.md).
An element that passes strain only is rejected because the underlying framework does not implement a strain-only update.
Compared with the power-law dashpot [`Viscosity01`](Viscosity01.md), the force does not grow as $|v|^\alpha$, which limits the force demand transmitted to the brace at large velocity.
For a smooth force law without an explicit yield threshold see [`CoulombFriction`](CoulombFriction.md).

## Example

The following lines define a bilinear damper with coefficient 100, yield force 500 and hardening ratio 0.05, attached to a two-node damper element.

```text
material BilinearViscosity 2 1E2 500 0.05
element Damper02 2 1 2 2 1 true 0 .5
```

This is the configuration used in `Example/Material/BilinearViscosity.supan`.

## References

1. Akcelyan, S., Lignos, D. G., and Hikino, T. (2018), "Adaptive numerical method algorithms for nonlinear viscous and bilinear oil damper models subjected to dynamic loading," Soil Dynamics and Earthquake Engineering, 113, 488--502, [doi:10.1016/j.soildyn.2018.06.021](https://doi.org/10.1016/j.soildyn.2018.06.021).
