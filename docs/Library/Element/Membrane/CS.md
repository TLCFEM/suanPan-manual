# CST/CSM

Couple Stress Mixed Triangle/Quadrilateral

* Number of Nodes: 3, 4, 5, 6, 7, 8
* Number of DoFs: 3 (Translation, Translation, Rotation)
* DoF Label: U1, U2, UR3

## Background

The `CS` family is based on the consistent couple stress theory, in which the rotation is an independent kinematic field and the strain energy depends on both the symmetric strain and the curvature.
Each node carries two translations and one drilling rotation $\omega$, so the displacement and rotation fields are interpolated independently.
The conjugate stress measures are the usual Cauchy stress $\boldsymbol\sigma$ and a couple stress $\boldsymbol m$, with the equilibrium equation
$$
\nabla\cdot\boldsymbol\sigma+\boldsymbol b=\boldsymbol 0,\qquad \nabla\cdot\boldsymbol m+\boldsymbol\epsilon:\boldsymbol\sigma=\boldsymbol 0.
$$
The six-field mixed variational principle used in the implementation introduces the displacement, rotation, strain, curvature, stress and couple stress as independent fields and removes the need for a local iteration.
The characteristic length $l$ couples the curvature energy to the strain energy and sets the scale at which rotational effects become significant.
A negative $l$ makes the element estimate the length as the square root of the element area, while a positive value fixes it explicitly.
The membrane geometries mirror the [`CP`](Plane/CP4.md) family, so the triangular and quadrilateral variants share the node ordering of [`CP3`](Plane/CP3.md) and [`CP8`](Plane/CP8.md).
The formulation is objective for the rotation but does not by itself regularise softening; additional regularisation is required for fracture problems, for which [`DCP3`](PFM/DCP3.md) and [`DCP4`](PFM/DCP4.md) are available.

## References

1. [arXiv:2207.02544](https://arxiv.org/abs/2207.02544)

## Syntax

```text title="CS"
element CSMT3 (1) (2...*) (3) [4] [5]
element CSMT6 (1) (2...*) (3) [4] [5]
element CSMQ4 (1) (2...*) (3) [4] [5]
element CSMQ5 (1) (2...*) (3) [4] [5]
element CSMQ6 (1) (2...*) (3) [4] [5]
element CSMQ7 (1) (2...*) (3) [4] [5]
element CSMQ8 (1) (2...*) (3) [4] [5]
# (1) int, unique element tag
# (2...*) int, corresponding number of node tags
# (3) int, material tag
# [4] double, thickness, default: 1.0
# [5] double, characteristic length, default: -1.0
```

## Remarks

1. The geometry definitions of CS elements resemble those of CP elements (e.g., CP3, CP4, CP5, CP6, CP7, CP8).
2. The characteristic length `[5]` can be left as default value (negative) to automatically determine the value based on geometry (square root of area), or set to a positive value to manually specify the fixed length.
3. Currently, only [`Elastic2D`](../../Material/Material2D/Elastic2D.md) is supported.

!!! warning "implementation limitation"
    The elements read the elastic modulus and Poisson's ratio from the material and build an `IsotropicCouple` tangent internally instead of using the material's own stiffness matrix.
    Under plane stress the modulus and Poisson's ratio are first converted to $E/(1-\nu^2)$ and $\nu/(1-\nu)$.
    Inelastic materials are therefore not supported even though the underlying six-field formulation is materially general.

4. The drilling rotation is a genuine kinematic DoF here, unlike the fictitious rotation used in [`Allman`](Drilling/Allman.md) or [`GQ12`](Drilling/GQ12.md).
5. The characteristic length controls the couple-stress contribution; larger values stiffen the rotational response.
6. For problems without rotational size effects the simpler [`CP4`](Plane/CP4.md) or [`CP8`](Plane/CP8.md) membrane elements are cheaper.
