# SGCMS

Simplified Generalized Conforming Mixed Shell Element

A planar shell element uses SGCMQ for membrane action and the DKT4 element for plate action.

* Number of Nodes: 4
* Number of DoFs: 6 (Translation, Translation, Translation, Rotation, Rotation, Rotation)
* DoF Label: U1, U2, U3, UR1, UR2, UR3
* Integration Membrane: Five-Point Irons Scheme
* Integration Plate: 3rd Gauss Scheme

![encoding](../PIC/Q4.svg)

## Background

SGCMS is a four-node flat shell assembled by [ShellBase](ShellBase.md) from the simplified generalized conforming membrane [SGCMQ](../Membrane/Drilling/GCMQ.md) and the discrete Kirchhoff plate [DKT4](../Plate/DKT4.md).

The membrane part uses a twelve-parameter local stress expansion and a five-point Irons rule, as described on the [GCMQ](../Membrane/Drilling/GCMQ.md) page, and supplies the drilling rotation $UR_3$.

The plate part imposes the Kirchhoff condition at the four edge midpoints and uses 2-by-2 Gauss points in the plane with three Gauss layers through the thickness.

At a fibre of coordinate $z$ the strain is $\mathbf\varepsilon=\mathbf B_m\mathbf d_m+z\,\mathbf B_p\mathbf d_p$, which produces the coupled membrane--bending stiffness blocks described on [ShellBase](ShellBase.md).

Unlike [S4](S4.md), no transverse shear strain is retained, so the plate is a thin-plate model that is free of shear locking.

!!! info "deviation from theory"
    The plate part enforces the Kirchhoff condition only at the four midpoints and has no transverse shear energy.
    The SGCMQ membrane uses the actual edge lengths without the objective-length option of the standalone element, so its drilling interpolation is mesh dependent.

## Syntax

```text title="SGCMS"
element SGCMS (1) (2...5) (6) [7] [8]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, thickness, default: 1.0
# [8] bool string, nonlinear geometry switch, default: false
```

## Remarks

1. If the nonlinear geometry is switched on, the transformation between the global and local reference frames will depend on the current displacement.
   The nonlinear transformation is similar to the corotational transformation, and the local response is still linear.
   Thus, it follows "large displacement, small deformation" assumption.

* Use a plane-stress two-dimensional material such as [`Elastic2D`](../../Material/Material2D/Elastic2D.md) so that the through-thickness integration yields the correct thin-plate bending stiffness.

!!! warning "implementation limitation"
    A plane-strain material changes the synthesized bending stiffness, and the uniform drilling mode has no explicit stabilization.

!!! note "developer note"
    The five-point Irons membrane rule and the three-layer plate rule are hard-coded.

* The membrane and plate integrations are fixed by the formulation and are not command-line arguments.
* The drilling rotation comes from the SGCMQ interpolation and can still lack stiffness in a uniform drilling mode, as noted on [Allman](../Membrane/Drilling/Allman.md).
* For a moderately thick plate with transverse shear deformation use [S4](S4.md), and for a triangular mesh use [DKTS3](DKTS3.md).

## References

1. [10.1002/nme.6066](https://doi.org/10.1002/nme.6066)
2. [10.1002/nme.1620151205](https://doi.org/10.1002/nme.1620151205)
3. Evaluation of a new quadrilateral thin plate bending element
