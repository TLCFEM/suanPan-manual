# Patch

Isogeometric Patches

In isogeometric analysis, the geometry of elements is defined by NURBS based surfaces or volumes.
Several elements are grouped into patches and patches behave similarly to traditional finite elements.

To define IGA patches, the knot vectors along each dimension and the control node polygon need to be assigned.

## Theory

Isogeometric analysis uses the same non-uniform rational B-spline (NURBS) basis to describe the geometry and the unknown field.
A univariate B-spline basis of degree $$p$$ is built from an open knot vector $$\Xi=\{\xi_1,\dots,\xi_{n+p+1}\}$$ by the Cox-de Boor recursion.
The number of basis functions, and therefore the number of control points along that direction, is $$n=\mathrm{length}(\Xi)-p-1$$.

The rational basis functions are
$$
R_i(\xi)=\frac{N_{i,p}(\xi)w_i}{\sum_{j=1}^n N_{j,p}(\xi)w_j},
$$
where $$w_i$$ is the weight attached to control point $$i$$ and $$N_{i,p}$$ is the corresponding B-spline basis function.
In this implementation the weight is stored as the last coordinate of each control node, so setting all weights to one recovers a B-spline basis.

In several dimensions the basis is the tensor product $$R_{ijk}(\xi,\eta,\zeta)=R_i(\xi)R_j(\eta)R_k(\zeta)$$.
The isoparametric geometry and displacement fields are $$\mathbf x=\sum_a R_a\mathbf x_a$$ and $$\mathbf u=\sum_a R_a\mathbf u_a$$.
The strain is $$\mathbf\varepsilon=\mathbf B\mathbf u_e$$ with $$\mathbf B$$ assembled from the physical derivatives $$\partial R_a/\partial x_i$$, which follow from the Jacobian $$\mathbf J=\partial\mathbf x/\partial\mathbf\xi$$.

Each nonzero knot span between two distinct knots is treated as one integration cell.
A $$2\times2$$ Gauss rule is used for surface patches and a $$2\times2\times2$$ rule for volume patches, with the sampling points mapped from $$[-1,1]$$ onto each span.
Because a basis function has support over several spans, one patch element couples a larger stencil of control nodes than a Lagrange finite element.
Refinement by knot insertion or degree elevation can change the approximation without changing the geometry, which is the central idea of the isogeometric concept.

## Remarks

A patch is not a single Lagrange element, so the number of connected control nodes is determined by the knot vectors and can be much larger than four or eight.
Control nodes must be supplied in the tensor-product order implied by the knot spans, and their last coordinate is the NURBS weight.
The basis is at least $$C^0$$ continuous across spans and is $$C^{p-1}$$ continuous at simple interior knots.
Use [PatchQuad](PatchQuad.md) for a two-dimensional membrane patch and [PatchCube](PatchCube.md) for a three-dimensional solid patch.
For conventional hexahedral elements with polynomial shape functions see [C3D8](../Cube/C3D8.md) and [C3D20](../Cube/C3D20.md).

## References

1. [10.1016/j.cma.2004.10.008](https://doi.org/10.1016/j.cma.2004.10.008)
2. [ISBN 978-0-470-74908-1](https://search.worldcat.org/search?q=bn:9780470749081)
