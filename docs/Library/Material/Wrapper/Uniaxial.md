# Uniaxial

Uniaxial Wrapper

Wraps a 3D host material model into a 1D uniaxial model that can be used with 1D elements.

It is assumed that $$\sigma_{22}=\sigma_{33}=\tau_{12}=\tau_{23}=\tau_{31}=0$$.

## Theory

A uniaxial stress state is the one-dimensional limit of the plane stress condensation implemented by [PlaneStress](PlaneStress.md).
Only the axial component $$\sigma_{11}$$ is active, so the five remaining stress components are prescribed to vanish.
Writing the host stress and tangent in the Voigt ordering $$(\sigma_{11},\sigma_{22},\sigma_{33},\tau_{12},\tau_{23},\tau_{13})$$, the wrapper partitions the strain vector into the axial entry and the five constrained entries.
Given the axial strain $$\varepsilon_{11}$$ from a truss or beam fibre, it solves

$$
\mathbf s_O(\varepsilon_{11},\mathbf e_O)=\mathbf 0,
\qquad
\mathbf e_O=(\varepsilon_{22},\varepsilon_{33},\gamma_{12},\gamma_{23},\gamma_{13}),
$$

using the host tangent block $$\mathbf D_{OO}$$ and the same Newton correction as in plane stress.
The reduced stress and tangent are $$\sigma^{\mathrm{1D}}=\sigma_{11}-\mathbf D_{1O}\mathbf D_{OO}^{-1}\mathbf s_O$$ and $$D^{\mathrm{1D}}=D_{11}-\mathbf D_{1O}\mathbf D_{OO}^{-1}\mathbf D_{O1}$$.
For a linear isotropic host this recovers $$\sigma_{11}=E\varepsilon_{11}$$ with lateral strains $$\varepsilon_{22}=\varepsilon_{33}=-\nu\varepsilon_{11}$$.

The implementation is the `StressWrapper` base class with `F1={0}`, so it shares its condensation, local iteration and nonlocal-history handling with [PlaneStress](PlaneStress.md) and [OS146](OS146.md).
With the default `[3]=1` only one Newton update is made, while larger values trigger local iterations until the constrained stress residual is small.

!!! warning "implementation limitation"
    With the default `[3]=1` the five constrained stresses are not exactly zero after the update.

!!! note "developer note"
    The lateral strain correction is computed from the host state of the previous step and applied only once.
    With `[3]>1` the convergence test is relative to the first correction and the counter is tested before each evaluation, so at most `[3]-1` corrections are applied.

The host must provide a nonsingular constrained tangent block, and nonlocal history variables are carried after the six strain entries.

## Syntax

```
material Uniaxial (1) (2) [3]
# (1) int, unique material tag
# (2) int, associated 3D material tag
# [3] int, maximum iteration allowed, default: 1
```

The response of attached 3D material models will be output when recorded.

## Remarks

Use this wrapper with 1D elements such as [T2D2](../../Element/Truss/T2D2.md) when the constitutive law is available only as a 3D model.
To obtain a 1D model from a 1D host instead, use the host directly; [Prestrain](Prestrain.md) is the appropriate wrapper when an imposed initial strain is needed.
For a two-dimensional in-plane state use [PlaneStress](PlaneStress.md), which keeps both normal stresses and the in-plane shear.
The wrapper reports a single stress component to the element but forwards recording to the 3D host, so recorded stresses still contain the full 3D state.
Increase the optional iteration count or reduce the step size if a large strain increment leaves a residual lateral stress in the single-pass mode.

## References

- [ISBN 978-1-4398-0247-2](https://search.worldcat.org/search?q=bn:9781439802472)
- [ISBN 978-0-387-97520-7](https://search.worldcat.org/search?q=bn:9780387975207)
