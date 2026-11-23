# CINP4

Bilinear Infinite Quadrilateral

* Number of Nodes: 4
* Number of DoFs: 2 (Translation, Translation)
* DoF Label: U1, U2

## Background

[`CINP4`](CINP4.md) is a mapped infinite quadrilateral for two-dimensional unbounded domains.
It attaches to the boundary of a finite-element mesh through the two nodes at $\eta=-1$, while the two nodes at $\eta\to+1$ are placed at infinity.
The mapping functions are
$$
M_1=\frac{(1-\xi)\eta}{\eta-1},\quad M_2=\frac{(1+\xi)\eta}{\eta-1},\quad M_3=\frac{(1+\xi)(1+\eta)}{2(1-\eta)},\quad M_4=\frac{(1-\xi)(1+\eta)}{2(1-\eta)}.
$$
At $\eta=-1$ the functions reduce to the linear shape functions of the two finite nodes and $M_3=M_4=0$.
As $\eta$ tends to $1$ the mapping sends the parent point to infinity, so the far field is represented without truncating the mesh.
The strain-displacement matrix is formed from the derivatives of $M_a$ mapped by the inverse Jacobian, $\nabla N_a=\boldsymbol J^{-\mathrm T}\nabla_{\!\xi}M_a$.
The stiffness integral over the semi-infinite domain is evaluated on the finite parent square, with the stretching toward infinity carried by the Jacobian determinant.
A $2\times2$ Gauss rule in the parent domain is used, and the thickness is applied as in [`CP4`](CP4.md).

!!! warning "implementation limitation"
    The element assembles only a static stiffness and has no mass or damping matrix.
    It is therefore restricted to static and quasi-static unbounded-domain problems, as in the reference paper, and cannot absorb outgoing waves in a dynamic analysis.

## References

1. [10.1016/0045-7949(84)90019-1](https://doi.org/10.1016/0045-7949(84)90019-1)
2. [ISBN 978-1-85617-633-0](https://search.worldcat.org/search?q=bn:9781856176330)

## Syntax

```text title="CINP4"
element CINP4 (1) (2...5) (6) [7]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0
```

## Remarks

1. The first two nodes are finite nodes while the latter two are infinite nodes.
2. The finite nodes lie on $\eta=-1$ and the infinite direction is $\eta\to+1$; the element must be attached to a mesh of ordinary [`CP4`](CP4.md) elements.
3. The thickness argument is forced to unity when the material declares plane strain.
4. A $2\times2$ Gauss rule is used in the parent domain; no nonlinear-geometry path is available.
5. The infinite nodes should be placed so that their connecting edge points away from the region of interest.
