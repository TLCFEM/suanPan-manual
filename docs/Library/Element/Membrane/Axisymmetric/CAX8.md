# CAX8

Axisymmetric Quadratic Quadrilateral

* Number of Nodes: 8
* Number of DoFs: 2
* DoF Label: RADIAL, AXIAL

## Background

[`CAX8`](CAX8.md) is the eight-node quadratic quadrilateral of the axisymmetric family.
The four corner nodes are ordered counter-clockwise from $(\xi,\eta)=(-1,-1)$, and nodes 5 to 8 are the midside nodes on the bottom, right, top and left edges.
The isoparametric interpolation uses the serendipity shape functions also used by [`CP8`](../Plane/CP8.md), so curved meridian boundaries can be represented.
The strain vector is $\mathbf\varepsilon=[\varepsilon_{rr},\varepsilon_{zz},\varepsilon_{\theta\theta},\gamma_{rz}]^\mathrm T$, with the hoop strain $\varepsilon_{\theta\theta}=u_r/r$ evaluated at each integration point.
The radius is interpolated with the eight-term quadratic monomial vector $[1,\xi,\eta,\xi^2,\xi\eta,\eta^2,\xi^2\eta,\xi\eta^2]$, and the quadrature weight is $2\pi r_qJ_qw_q$.
The default rule is $3\times3$ Gauss; the parser currently constructs the element with reduced integration disabled.

!!! warning "implementation limitation"
    Reduced integration and nonlinear geometry cannot be selected from an `element CAX8` command.

!!! note "developer note"
    No parser token exposes reduced integration for `CAX8`, and the nonlinear-geometry argument is left at its default false.
    The class contains branches for both options, but they cannot be selected from an `element CAX8` command.

The parent page [`CAX4`](CAX4.md) derives the axisymmetric strain-displacement matrix and discusses the singularity at $r=0$.

## Syntax

```text title="CAX8"
element CAX8 (1) (2...9) (10)
# (1) int, unique element tag
# (2...9) int, node tags
# (10) int, material tag
```

## Remarks

* The assigned material must declare an axisymmetric plane type or initialisation fails.
* Boundary conditions use the `RADIAL` and `AXIAL` DoF labels.
* Mid-edge nodes must be placed at the true geometric midpoint of a straight edge, or at the appropriate point on a curved edge, to avoid a distorted Jacobian.
* The quadratic interpolation gives accurate hoop stresses with far fewer elements than [`CAX4`](CAX4.md) or [`CAX3`](CAX3.md), at the cost of a $3\times3$ quadrature loop.
* The nonlinear-geometry path is not reachable from the current element parser.

## References

1. [ISBN 978-1-85617-633-0](https://search.worldcat.org/search?q=bn:9781856176330)
