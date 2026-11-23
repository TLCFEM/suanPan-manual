# Mindlin

Mindlin Plate Element

* Number of Nodes: 4
* Number of DoFs: 3 (Translation, Rotation, Rotation)
* DoF Label: U3, UR1, UR2

![encoding](../PIC/Q4.svg)

## Background

The Mindlin--Reissner plate theory relaxes the Kirchhoff condition by treating the section rotation $\boldsymbol\theta$ as an independent field.

The transverse displacement $w$ and the two rotations have independent interpolations, and the transverse shear strain is the difference between the slope of $w$ and the section rotation, $\boldsymbol\gamma=\nabla w-\boldsymbol\theta$ up to the sign convention used for the two rotation components.

!!! info "deviation from theory"
    The source assembles $\gamma_1=\partial w/\partial y-\theta_1$ and $\gamma_2=\partial w/\partial x+\theta_2$, so the shear components are swapped and signed differently from texts that write $\boldsymbol\gamma=\nabla w-\boldsymbol\theta$ with the same ordering.
    The rotation DoFs are local plate rotations and are not the global vector components implied by that compact notation.

The curvature is $\boldsymbol\kappa=\nabla\boldsymbol\theta$ in the symmetric part, and the strain at a fibre of coordinate $z$ is $\boldsymbol\varepsilon(z)=\boldsymbol\kappa^{\rm sym}\,z$, while the shear strain is uniform through the thickness.

The internal energy therefore contains a bending part of order $t^3$ and a shear part of order $t$.

As the thickness tends to zero, the shear energy enforces $\boldsymbol\gamma\approx 0$ pointwise, and a displacement element that interpolates $w$ and $\boldsymbol\theta$ with the same order becomes over-constrained and locks, giving a response that is far too stiff.

The implementation avoids this shear locking by evaluating the shear contribution with a single reduced-integration point at the element centre.

The shear stiffness is assembled as

$$
\mathbf K_s=\dfrac{10}{3}\,G\,t\,\det\mathbf J\;\mathbf B_\gamma^{\mathsf T}\mathbf B_\gamma,
$$

where $G$ is the shear modulus supplied by the material, $\det\mathbf J$ is the Jacobian determinant at the centre, and $\mathbf B_\gamma$ contains the centre values of the bilinear shape functions and their derivatives.

This one-point rule is equivalent to an assumed-shear-strain or mixed formulation of the type analysed by Malkus and Hughes.

!!! info "deviation from theory"
    The shear energy is not integrated with the 2-by-2 rule used for bending, but is replaced by a single-point penalty with a fixed factor of $10/3$ multiplying $Gt\det\mathbf J$.
    No separate shear correction factor is computed from the section shape, so that factor is absorbed into the penalty coefficient.

The bending part is integrated with 2-by-2 Gauss points in the plane and with the chosen number of Gauss layers through the thickness.

## Syntax

```text title="Mindlin"
element Mindlin (1) (2...5) (6) (7) [8]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# (7) double, thickness
# [8] int, number of integration points, default: 5
```

## Remarks

* A zero shear modulus reported by the material causes initialization to fail, since the reduced-integration shear penalty cannot be formed.

!!! warning "implementation limitation"
    The element is restricted to four-node quadrilaterals and requires a material that reports a nonzero shear modulus.
    The through-thickness integration is the only adjustable rule, and the one-point shear penalty is hard-coded.

* The thickness is required and scales both the shear penalty and the through-thickness fibre coordinates.
* The optional argument selects the through-thickness Gauss rule and defaults to five points, while the in-plane rule for bending is a fixed 2-by-2 Gauss rule.
* Only the shear term uses reduced integration, so the bending part is still fully integrated and the element does not introduce an in-plane hourglass mechanism from that rule.
* Use a plane-stress two-dimensional material such as [`Elastic2D`](../../Material/Material2D/Elastic2D.md) so that the integrated bending stiffness has the correct $Et^3/[12(1-\nu^2)]$ coefficient.
* This is a plate-only element with three DoFs per node; for a six-DoF flat shell use [S4](../Shell/S4.md), which combines it with the [GQ12](../Membrane/Drilling/GQ12.md) membrane.
* For thin plates where transverse shear is negligible, [DKT4](DKT4.md) gives a locking-free Kirchhoff alternative.

## References

1. Mindlin, R.D. (1951), Influence of rotary inertia and shear on flexural motions of isotropic elastic plates, Journal of Applied Mechanics 18, 31--38.
2. Reissner, E. (1945), The effect of transverse shear deformation on the bending of elastic plates, Journal of Applied Mechanics 12, A69--A77.
3. Malkus, D.S. and Hughes, T.J.R. (1978), Mixed finite element methods---reduced and selective integration techniques: a unification of concepts, Computer Methods in Applied Mechanics and Engineering 15(1), 63--81, [doi:10.1016/0045-7825(78)90051-1](https://doi.org/10.1016/0045-7825(78)90051-1).
4. Hughes, T.J.R., The Finite Element Method: Linear Static and Dynamic Finite Element Analysis, Prentice Hall, 1987.
