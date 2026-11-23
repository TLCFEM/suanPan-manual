# CIN3D8

Linear Infinite Cube/Brick

* Number of Nodes: 8
* Number of DoFs: 3 (All Translation)
* DoF Label: U1, U2, U3

## Theory

`CIN3D8` is a mapped infinite element used to represent an unbounded medium with a single layer of elements attached to the boundary of a finite mesh.
It has eight nodes, with nodes one through four on the near face and nodes five through eight on the far face in the $\zeta$ direction.
The far face corresponds to $\zeta=1$, which the mapping sends to infinity.

The implementation uses a mapping $\mathbf x=\sum_a M_a(\xi,\eta,\zeta)\mathbf x_a$ whose coefficient functions behave like $\zeta/(\zeta-1)$ as $\zeta\to1$.
The displacement shape functions contain the factors $\zeta(\zeta-1)$ on the near face and $1-\zeta^2$ on the far face, so they remain finite near the mesh and decay towards infinity.
Strain-displacement matrices are formed from the physical gradients $\nabla_{\mathbf x}N_a=\mathbf J^{-T}\nabla_{\mathbf\xi}N_a$, where $\mathbf J$ is built from the mapped geometry.

The stiffness and body-force integrals use a $2\times2\times2$ Gauss rule in the parent domain.
The element is intended for small-strain analysis and has no nonlinear-geometry switch.
It is normally coupled to ordinary finite elements such as [C3D8](C3D8.md) or [C3D20](C3D20.md) along the shared near face.

## References

1. [10.1016/0045-7949(84)90019-1](https://doi.org/10.1016/0045-7949(84)90019-1)
2. Infinite elements
3. [10.1002/nme.1620210705](https://doi.org/10.1002/nme.1620210705)

## Syntax

```text title="CIN3D8"
element CIN3D8 (1) (2...9) (10)
# (1) int, unique element tag
# (2...9) int, eight corner nodes with conventional order
# (10) int, material tag
```

## Remarks

The only argument beyond the tags is the material tag, which is used at each of the eight integration points.
Orient the element so that each edge from a near-face node to its far-face counterpart points away from the region of interest.
The far-face node coordinates define the geometric mapping, so they must be placed consistently with rays extending to infinity.
The source assembles a consistent mass matrix and a body-force contribution from the decayed interpolation when the material supplies a density.
No hourglass control is needed with the $2\times2\times2$ Gauss rule.
