# PatchQuad

Patch of Quadrilateral Elements

* Number of DoFs: 2
* DoF Label: U1, U2
* Number of Nodes: varies
* Supports Mass
* Supports Body Force

## Background

`PatchQuad` is the two-dimensional membrane patch element of the isogeometric framework described in [Patch](Patch.md).
It builds a NURBS surface from two knot vectors and a rectangular grid of control nodes, each carrying two translational DoFs.
The third coordinate of each control node is interpreted as the NURBS weight.
The displacement field is $\boldsymbol u=\sum_{ij}R_{ij}\boldsymbol u_{ij}$, and the in-plane strain follows from the physical derivatives of the tensor-product basis.
Each knot span is integrated with a $2\times2$ Gauss rule, and the element stiffness, mass and body force are multiplied by the thickness.

## Syntax

A key-value style is used.

```text title="PatchQuad"
element PatchQuad (1) -node (2...) -knotx (3...) -knoty (4...) -material (5) [-thickness (6)]
# (1) int, unique element (patch) tag
# (2...) int, node tags of control node polygon
# (3...) double, knot vector along x axis
# (4...) double, knot vector along y axis
# (5) int, material tag
# (6) double, thickness
```

## Remarks

The keys `-node`, `-knotx`, `-knoty` and `-material` are required, while `-thickness` is optional.
The number of control nodes must equal the product of the numbers of basis functions implied by the two knot vectors, and the nodes are ordered lexicographically.
The third coordinate of each control node is the NURBS weight, so use one for an ordinary B-spline surface.
For a plane-strain material the implementation overrides the thickness with one, so the supplied value is ignored.
A 2D material tag is required, and a consistent mass is assembled when the material supplies a density.
For the three-dimensional counterpart see [PatchCube](PatchCube.md).

## References

1. T. J. R. Hughes, J. A. Cottrell and Y. Bazilevs, Isogeometric analysis: CAD, finite elements, NURBS, exact geometry and mesh refinement, *Computer Methods in Applied Mechanics and Engineering* 194(39-41):4135-4195, 2005, [doi:10.1016/j.cma.2004.10.008](https://doi.org/10.1016/j.cma.2004.10.008).
