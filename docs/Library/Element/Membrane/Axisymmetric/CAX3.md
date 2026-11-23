# CAX3

Axisymmetric Linear Triangle

* Number of Nodes: 3
* Number of DoFs: 2
* DoF Label: RADIAL, AXIAL

## Background

[`CAX3`](CAX3.md) is the three-node constant-strain triangle of the axisymmetric family.
Its nodal DoFs are the radial and axial displacements, and the strain vector is $$\mathbf\varepsilon=[\varepsilon_{rr},\varepsilon_{zz},\varepsilon_{\theta\theta},\gamma_{rz}]^\mathrm T$$, with $$\varepsilon_{\theta\theta}=u_r/r$$ and $$\gamma_{rz}=\partial u_r/\partial z+\partial u_z/\partial r$$.
The triangle uses area coordinates so the in-plane derivatives $$\partial N_a/\partial r$$ and $$\partial N_a/\partial z$$ are constant, derived from the inverse of the $$3\times3$$ coordinate matrix.
The hoop strain is evaluated at the element centroid radius $$r_c=(r_1+r_2+r_3)/3$$, so this element is one-point integrated.
The integration weight is $$2\pi r_c A$$, with $$A$$ the area of the meridian triangle.

!!! warning "implementation limitation"
    The hoop strain uses one centroid radius for the whole triangle, so elements that span a large radial extent approximate the variation of $$u_r/r$$ by a single value.
    A centroid at or near zero radius makes the strain row singular.

The stiffness is
$$
\mathbf K^e=2\pi r_c A\,\mathbf B^\mathrm T\mathbf D\mathbf B.
$$
The material must supply an axisymmetric tangent matrix, and the parent page [`CAX4`](CAX4.md) derives the full four-component formulation.

## Syntax

```text title="CAX3"
element CAX3 (1) (2...4) (5) [6]
# (1) int, unique element tag
# (2...4) int, node tags
# (5) int, material tag
# [6] bool string, nonlinear geometry switch, default: false
```

## Remarks

* The assigned material must declare an axisymmetric plane type or initialisation fails.
* Boundary conditions use the `RADIAL` and `AXIAL` DoF labels.
* The element is very stiff in bending, like its plane counterpart [`CP3`](../Plane/CP3.md), and dense meshes are needed for accurate stresses.
* The optional nonlinear-geometry switch is parsed, but the current implementation evaluates only the small-strain strain measure.

!!! info "deviation from theory"
    Supplying a true nonlinear-geometry switch does not activate a Total Lagrangian axisymmetric formulation.

!!! note "developer note"
    The `CAX3` constructor forwards the nonlinear-geometry flag to the base class, yet `update_status` never branches on it.

* A Gauss point at zero radius is singular, so keep the centroid away from the axis of revolution.

## References

1. [ISBN 978-1-85617-633-0](https://search.worldcat.org/search?q=bn:9781856176330)
