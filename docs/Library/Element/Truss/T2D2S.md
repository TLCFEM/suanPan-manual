# T2D2S

2D Linear Truss Using Section

* Number of Nodes: 2
* Number of DoFs: 2 (Translation, Translation)
* DoF Label: U1, U2

## Background

The suffix `S` stands for **Section**: the implementation derives from `SectionElement1D` and takes a section tag, whereas the canonical [T2D2](T2D2.md) derives from `MaterialElement1D` and takes a material tag together with a cross-sectional area.
The kinematics, the corotational transformation `T2DC` and the strain measures are identical to those derived on the [T2D2](T2D2.md) page.

The attached section supplies the axial rigidity, so the initial element stiffness is $$\mathbf K_0=\mathbf k_{s,0}/L_0$$.
In the corotational case the section is driven by the chosen strain measure, $$\varepsilon=\ln(L/L_0)$$ for log strain or $$\varepsilon=L/L_0-1$$ for engineering strain, and the tangent is $$\mathbf K=\mathbf k_s/\varepsilon_\mathrm{den}$$ with $$\varepsilon_\mathrm{den}=L$$ or $$L_0$$.
The geometric stiffness is assembled from the section resistance as $$\mathbf K_g=\mathbf T^\mathrm T(N/L)\,\partial^2u/\partial\mathbf v^\mathrm T\partial\mathbf v\,\mathbf T$$.
Because the section owns the area, this element has no area-update switch and no Euler buckling check.

!!! warning "implementation limitation"
    The parser exposes only the corotational and log-strain switches for this variant, so a constant-volume area update and the Euler buckling check of [T2D2](T2D2.md) are unavailable.

Suitable one-dimensional sections include [`Rectangle1D`](../../Section/Section1D/Rectangle1D.md), [`Circle1D`](../../Section/Section1D/Circle1D.md), [`TrussSection`](../../Section/Section1D/TrussSection.md) and [`Fibre1D`](../../Section/Section1D/Fibre1D.md).

## Syntax

```text title="T2D2S"
element T2D2S (1) (2) (3) (4) [5] [6]
# (1) int, unique element tag
# (2) int, node i
# (3) int, node j
# (4) int, section tag
# [5] bool string, nonlinear geometry switch, default: false
# [6] bool string, whether to use log strain, default: false
```

## Remarks

1. Compared to `T2D2`, `T2D2S` uses section instead of material.
   Hence, sectional area is handled by the corresponding section model.
2. The nonlinearity cannot propagate into the section level.
   So it is not possible to update area in `T2D2S`.
3. The `S` suffix denotes the section-based formulation, not a simplified or small-displacement variant.
4. Use [T2D2](T2D2.md) when a constant-volume area update or the Euler buckling check is required.
5. The section must be one-dimensional, and its initial stiffness must represent the axial rigidity $$EA$$.
