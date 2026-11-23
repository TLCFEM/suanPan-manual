# MultilinearJ2

Multilinear Hardening J2 Model

## Theory

The `MultilinearJ2` model is a concrete implementation of the [`NonlinearJ2`](NonlinearJ2.md) framework with a tabulated piecewise-linear isotropic hardening law.
The backbone is a set of control points $$(p_i,\sigma_{y,i})$$ with the first plastic strain fixed to zero.
Between two adjacent control points the yield radius is

$$
k(p)=\sigma_{y,i}+\dfrac{\sigma_{y,i+1}-\sigma_{y,i}}{p_{i+1}-p_i}\left(p-p_i\right),\qquad p_i\leqslant p\leqslant p_{i+1}.
$$

The derivative $$k'(p)$$ is the slope of the current segment and is zero beyond the last control point, so the response becomes perfectly plastic there.

!!! info "deviation from theory"
    A conventional piecewise-linear hardening table extrapolates the slope of the last segment beyond the final control point.
    This implementation sets the final slope to zero, so the curve becomes a perfectly plastic plateau instead of continuing to harden.

!!! warning "implementation limitation"
    The first plastic strain must be exactly zero; a table with any other starting strain is rejected.

The kinematic contribution is $$h(p)=0$$.
The return mapping solves the same discrete consistency condition as [`CustomJ2`](CustomJ2.md), using the current segment slope in the Newton denominator.
The stored history is the accumulated plastic strain followed by a permanently zero back stress.

## Syntax

```text title="MultilinearJ2"
material MultilinearJ2 (1) (2) (3) (4) ((5) (6)...)
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, density
# (5) double, plastic strain of control point
# (6) double, stress of control point
```

## Remarks

The density is compulsory and occupies the fourth argument.
The control points are supplied as alternating plastic strain and yield stress values.
The first plastic strain must be exactly zero, otherwise the constructor throws an invalid-argument exception.
The initial yield stress is the stress value of the first control point.
The last segment is extrapolated as a perfectly plastic plateau because its slope is set to zero.
Kinks at the control points can slow down the local Newton iteration, so prefer closely spaced points or a smooth law such as [`ExpJ2`](ExpJ2.md) when a smooth tangent is important.
The uniaxial counterpart is [`MultilinearMises1D`](../../Material1D/vonMises/Multilinear1D.md).
Use a three-dimensional solid element such as `C3D8` with this material.

## References

1. [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)
