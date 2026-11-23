# DKT4

DKT Quadrilateral Plate

* Number of Nodes: 4
* Number of DoFs: 3 (Translation, Rotation, Rotation)
* DoF Label: U3, UR1, UR2

![encoding](../PIC/Q4.svg)

## Background

DKT4 is the four-node quadrilateral version of the discrete Kirchhoff plate described in detail on [DKT3](DKT3.md).

The transverse displacement and the two rotations $(w,\theta_x,\theta_y)$ are interpolated at the four corners, and the discrete Kirchhoff condition $\beta_s=-\partial w/\partial s$ is enforced at the four edge midpoints.

The implementation therefore works with eight sampling points, the four corners plus four midpoints, using an eight-node serendipity interpolation for the transverse displacement and linear edge interpolation for the rotations.

The curvature matrix has the same form $\boldsymbol\kappa=(\beta_{x,x},\,\beta_{y,y},\,\beta_{x,y}+\beta_{y,x})^{\mathsf T}$, and a fibre at thickness coordinate $z$ contributes $z^2\mathbf B^{\mathsf T}\mathbf D\mathbf B$ to the stiffness.

The in-plane integration uses 2-by-2 Gauss points, and the thickness integration uses the selected number of Gauss points with a default of three.

No transverse shear energy is included, so the element is a thin-plate element that is free of shear locking but cannot represent thick-plate shear deformation.

!!! info "deviation from theory"
    The discrete Kirchhoff condition is satisfied only at the four edge midpoints and not pointwise.
    The element is a Kirchhoff approximation with no transverse shear energy, so it differs from a fully conforming thin-plate element and from any Mindlin--Reissner element.

This plate interpolation supplies the bending part of the flat shell [SGCMS](../Shell/SGCMS.md).

## Syntax

```text title="DKT4"
element DKT4 (1) (2...5) (6) (7) [8]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# (7) double, thickness
# [8] int, number of integration points along thickness, default: 3
```

## Remarks

* The DoF layout is the plate-only triple $(U_3,UR_1,UR_2)$; a six-DoF shell uses [S4](../Shell/S4.md) or [SGCMS](../Shell/SGCMS.md) instead.
* Use a plane-stress two-dimensional material such as [`Elastic2D`](../../Material/Material2D/Elastic2D.md) so that the numerically integrated bending stiffness matches the thin-plate moment--curvature law.

!!! warning "implementation limitation"
    A plane-strain material gives a different bending stiffness because the matrix is integrated rather than prescribed.
    Only the thickness Gauss rule is configurable, and the in-plane rule is fixed.

* The thickness must be supplied explicitly and sets both the fibre coordinates $z=\xi t/2$ and the layer weights.
* The optional argument controls only the through-thickness Gauss rule; the in-plane 2-by-2 rule is fixed.
* For moderately thick plates use [Mindlin](Mindlin.md), which retains transverse shear deformation with reduced integration to avoid locking.

## References

1. Batoz, J.-L., Bathe, K.-J. and Ho, L.-W. (1980), A study of three-node triangular plate bending elements, International Journal for Numerical Methods in Engineering 15(12), 1771--1812, [doi:10.1002/nme.1620151205](https://doi.org/10.1002/nme.1620151205).
2. Batoz, J.-L. and Tahar, M.B. (1982), Evaluation of a new quadrilateral thin plate bending element, International Journal for Numerical Methods in Engineering 18(11), 1655--1677.
