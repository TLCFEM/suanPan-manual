# Cell3DOS

Basic Building Block for 3D OS Section

## References

1. [Distributed plasticity analysis of steel building structural systems](https://www.proquest.com/dissertations-theses/distributed-plasticity-analysis-steel-building/docview/304696456/se-2)

## Syntax

```
section Cell3DOS (1) (2) (3) (4) (5) (6) [7] [8]
# (1) int, unique section tag
# (2) double, area
# (3) double, sectional coordiante
# (4) double, py
# (5) double, pz
# (6) int, material tag
# [7] double, eccentricity/location along y axis, default: 0.0
# [8] double, eccentricity/location along z axis, default: 0.0
```

## Remarks

The parameter `(3)` is the warping function $$\omega$$.

The parameters `(4)` and `(5)` are partial derivatives of the warping function $$\omega$$, namely,
$$\frac{\partial \omega}{\partial y}$$ and $$\frac{\partial \omega}{\partial z}$$.

The attached material needs to be an OS material.
Use a wrapper, for example, [OS146](../../Material/Wrapper/OS146.md) (for 3D host material)
and [OS146S](../../Material/Wrapper/OS146S.md) (for 1D host material with linear elastic shear response).

## Example

See [this](../../../Example/Structural/Statics/thin-walled-section.md) example.
