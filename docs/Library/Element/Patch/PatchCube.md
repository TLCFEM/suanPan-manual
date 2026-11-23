# PatchCube

Patch of Hexahedron Elements

* Number of DoFs: 3
* DoF Label: U1, U2, U3
* Number of Nodes: varies
* Supports Mass
* Supports Body Force

## Background

`PatchCube` is the three-dimensional solid patch element of the isogeometric framework described in [Patch](Patch.md).
It builds a B-spline or NURBS volume from three knot vectors and a rectangular grid of control nodes, whose size follows from the knot vectors.
Each control node supplies three translational DoFs, and its fourth coordinate is interpreted as the NURBS weight.
The displacement field is $\boldsymbol u=\sum_{ijk}R_{ijk}\boldsymbol u_{ijk}$ with the tensor-product rational basis defined in [Patch](Patch.md).
Strains are integrated with a $2\times2\times2$ Gauss rule over each knot span, and the tangent, mass and body force use the same basis.

## Syntax

A key-value style is used.

```text title="PatchCube"
element PatchCube (1) -node (2...) -knotx (3...) -knoty (4...) -knotz (5...) -material (6)
# (1) int, unique element (patch) tag
# (2...) int, node tags of control node polygon
# (3...) double, knot vector along x axis
# (4...) double, knot vector along y axis
# (5...) double, knot vector along z axis
# (6) int, material tag
```

## Remarks

The key-value syntax expects the node list after `-node` and the knot vectors after `-knotx`, `-knoty` and `-knotz`.
The number of control nodes must equal the product of the numbers of basis functions implied by the three knot vectors, and the nodes are ordered lexicographically in the index triple.
The fourth coordinate of each control node is the NURBS weight, so use one for an ordinary B-spline volume.
A 3D material tag is required, and a consistent mass and body force are assembled when the material supplies a density.
The element has no nonlinear-geometry switch.
For the two-dimensional counterpart see [PatchQuad](PatchQuad.md), and for conventional polynomial bricks see [C3D8](../Cube/C3D8.md).

## References

1. T. J. R. Hughes, J. A. Cottrell and Y. Bazilevs, Isogeometric analysis: CAD, finite elements, NURBS, exact geometry and mesh refinement, *Computer Methods in Applied Mechanics and Engineering* 194(39-41):4135-4195, 2005, [doi:10.1016/j.cma.2004.10.008](https://doi.org/10.1016/j.cma.2004.10.008).
