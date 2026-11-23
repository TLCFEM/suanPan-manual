# (S)GCMQ

Generalised Conforming Mixed Quadrilateral With Drilling DoFs

* Number of Nodes: 4
* Number of DoFs: 3 (Translation, Translation, Rotation)
* DoF Label: U1, U2, UR3
* Supports Body Force
* Constant Consistent Mass Matrix With Same Order Integration

![encoding](../../PIC/Q4.svg)

## Background

The GCMQ family is a four-node drilling membrane derived from a modified Hu--Washizu principle, in which displacement, strain and stress fields are treated as independent variables.

The same drilling interpolation idea as [Allman](Allman.md) and [GQ12](GQ12.md) is used, but the discrete equations are built in a 12-parameter local stress space with the linear stress modes $\{1,x,y,xy\}$.

Write the local stress as $\boldsymbol\sigma=\mathbf P\boldsymbol\alpha$, with $\boldsymbol\alpha$ the 12 stress parameters, and the local strain as $\boldsymbol\varepsilon=\mathbf P_\varepsilon\boldsymbol\beta$.

The compatibility and equilibrium equations reduce to solving small systems with matrices $\mathbf H$, $\mathbf N$ and $\mathbf M$ assembled from the integration points, after which the element stiffness is condensed to the nodal DoFs.

The full `GCMQ` adds three enhanced strain modes to avoid excessive stiffness on coarse or distorted meshes: a quadratic dilatational mode $(3x^2-1,\,3y^2-1)$, a quadratic shear mode $x^2-y^2$ and a complementary mode $x^2+y^2-2/3$.

!!! info "deviation from theory"
    The enhanced strain basis is a fixed set of three quadratic polynomials rather than a general assumed-strain expansion.
    The complementary mode $x^2+y^2-2/3$ is included specifically to keep the two shear modes frame invariant, so the basis is tailored to this element rather than being the standard EAS choice.

The simplified `SGCMQ` omits these modes and the associated internal variables, giving a cheaper displacement-like element that is the membrane part of the shell [SGCMS](../../Shell/SGCMS.md).

The three available integration rules are a five-point Irons rule, a third-order Lobatto rule and a third-order Gauss rule, selected by the letters `I`, `L` and `G`.

## References

1. [10.1002/nme.6066](https://doi.org/10.1002/nme.6066)
2. [10.1016/j.engstruct.2019.109592](https://doi.org/10.1016/j.engstruct.2019.109592)
3. [10.1016/j.engstruct.2020.110760](https://doi.org/10.1016/j.engstruct.2020.110760)
4. [10.1016/0045-7825(89)90124-2](https://doi.org/10.1016/0045-7825(89)90124-2)

## Syntax

```text title="GCMQ"
element GCMQI (1) (2...5) (6) [7] [8]
element GCMQL (1) (2...5) (6) [7] [8]
element GCMQG (1) (2...5) (6) [7] [8]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0
# [8] double, objective length, default: -1.0 (disabled)

element SGCMQI (1) (2...5) (6) [7] [8]
element SGCMQL (1) (2...5) (6) [7] [8]
element SGCMQG (1) (2...5) (6) [7] [8]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# [7] double, element thickness, default: 1.0
# [8] double, objective length, default: -1.0 (disabled)
```

## Remarks

* Three integration schemes are available: "I", "L" and "G".
  - "I": Five-Point Irons Scheme
  - "L": 3rd Order Lobatto Scheme
  - "G": 3rd Order Gauss Scheme
* `GCMQ` is the full version described in [10.1002/nme.6066](https://doi.org/10.1002/nme.6066) with enhanced strain.
  `SGCMQ` is a `PS` like element with no enhanced strain, the direct result of which is that less computation is required (less than `CP8R`).

The default approach interpolates translations from drilling rotations using edge length, potentially causing severe mesh dependency for drilling DoFs.
This is only an issue if the simulation actually uses drilling DoFs, as it can skew the accuracy of connected components.
To prevent this, providing a positive objective length [8] triggers an alternative formulation that relies on this specific length for interpolation.

!!! warning "implementation limitation"
    The objective length defaults to -1, so the mesh-dependent edge-length interpolation is active unless a positive value is supplied.
    Initialization fails and the element is disabled if the local projection matrices are singular.
    The thickness argument is silently overwritten to 1.0 for a plane-strain material.

* The parser also accepts `GCMQ` without a suffix, followed by an optional thickness and an optional scheme character that defaults to `I`.
* A non-singular local projection matrix is required, so an element whose initialization solve fails is disabled with an error message.
* The thickness argument is overridden to 1.0 for a plane-strain material, as in [GQ12](GQ12.md).
* The simplified variant is used as the membrane part of [SGCMS](../../Shell/SGCMS.md), which combines it with the [DKT4](../../Plate/DKT4.md) plate.
