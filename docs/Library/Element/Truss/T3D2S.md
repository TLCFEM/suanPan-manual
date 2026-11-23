# T3D2S

3D Linear Truss Using Section

* Number of Nodes: 2
* Number of DoFs: 3 (Translation, Translation, Translation)
* DoF Label: U1, U2, U3

## Background

The suffix `S` stands for **Section**: the implementation derives from `SectionElement1D` and takes a section tag, while the canonical [T3D2](T3D2.md) derives from `MaterialElement1D` and takes a material tag plus a cross-sectional area.
The spatial kinematics and the corotational transformation `T3DC` are the same as those derived on the [T2D2](T2D2.md) page.

The attached section carries the axial rigidity, so the initial stiffness is $$\mathbf K_0=\mathbf k_{s,0}/L_0$$.
Under corotational kinematics the section strain is $$\varepsilon=\ln(L/L_0)$$ with log strain or $$\varepsilon=L/L_0-1$$ with engineering strain, and the tangent is formed by dividing the section stiffness by $$L$$ or $$L_0$$ respectively.
The geometric stiffness is $$\mathbf K_g=\mathbf T^\mathrm T(N/L)\,\partial^2u/\partial\mathbf v^\mathrm T\partial\mathbf v\,\mathbf T$$, with $$N$$ the section resistance.
No area update and no Euler buckling check are available, so [T3D2](T3D2.md) is the choice when constant-volume area changes matter.

!!! warning "implementation limitation"
    The parser exposes only the corotational and log-strain switches for this variant, so element-level nonlinearity cannot change the area owned by the section.

Suitable one-dimensional sections include [`Rectangle1D`](../../Section/Section1D/Rectangle1D.md), [`Circle1D`](../../Section/Section1D/Circle1D.md), [`TrussSection`](../../Section/Section1D/TrussSection.md) and [`Fibre1D`](../../Section/Section1D/Fibre1D.md).

## Syntax

```text title="T3D2S"
element T3D2S (1) (2) (3) (4) [5] [6]
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, section tag
# [5] bool string, nonlinear geometry switch, default: false
# [6] bool string, whether to use log strain, default: false
```

## Remarks

1. Compared to `T3D2`, `T3D2S` uses section instead of material.
   Hence, sectional area is handled by the corresponding section model.
2. The nonlinearity cannot propagate into the section level.
   So it is not possible to update area in `T3D2S`.
3. The `S` suffix denotes the section-based formulation, not a simplified or small-displacement variant.
4. Use [T3D2](T3D2.md) when a constant-volume area update is required.
5. The section must be one-dimensional, and its initial stiffness must represent the axial rigidity $$EA$$.
