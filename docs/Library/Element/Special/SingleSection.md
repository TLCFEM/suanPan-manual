# SingleSection

Single Section Analysis

- 2D:
  * Number of DoFs: 2 (AXIAL, STRONG AXIS ROTATION)
  * DoF Label: AXIAL, RS
- 3D:
  * Number of DoFs: 3 (AXIAL, STRONG AXIS ROTATION, WEAK AXIS ROTATION)
  * DoF Label: AXIAL, RS, RW

It is often necessary to perform a section analysis to determine the capacity of the target section.
The `SingleSection` element is exactly for this purpose.

To use the element, a proper section shall be defined.

## Background

A fibre section represents a cross-section by a set of integration points, each carrying a uniaxial material law.
For an axial strain $$\epsilon$$ and a curvature $$\kappa$$ about the bending axis, the strain at a fibre with lever arm $$y$$ from the reference axis is

$$
\epsilon_f=\epsilon+y\,\kappa .
$$

The section deformation is obtained by integrating the fibre response over the area,

$$
N=\int_A\sigma(\epsilon_f)\,\mathrm dA,\qquad
M=\int_A y\,\sigma(\epsilon_f)\,\mathrm dA,
$$

and the section tangent is the corresponding integral of the fibre tangents weighted by $$1$$ and $$y$$.
The sign of the lever arm follows the convention of the chosen section model.

The `SingleSection` element exposes one such section directly at a single node.
Its DoFs are passed unchanged to the section as the section deformation, and the section returns the conjugate forces and the consistent tangent.
This isolates sectional behaviour from any spatial discretisation, so the element can be used to generate moment--curvature or axial force--strain curves and to validate a section definition before using it in a beam or shell model.

!!! warning "implementation limitation"
    Later changes to the original section are not reflected in this element.
    The element has no geometric stiffness of its own.

!!! note "developer note"
    The section is copied when the element is initialized.

## Syntax

```text title="SingleSection"
element SingleSection2D (1) (2) (3)
element SingleSection3D (1) (2) (3)
# (1) int, unique tag
# (2) int, node tag
# (3) int, section tag
```

## Remarks

It directly exposes the associated section.

1. In 3D there are two bending DoFs, RS and RW, so the section deformation has three components and the section must be defined accordingly.
2. The element has only one node and no geometric stiffness, so it is intended for a section-level analysis rather than for a structural model.
3. The section is copied when the element is initialised, hence changes to the original section afterwards are not seen by this element.

!!! warning "breaking changes"
    Before `v4`, one can use integer indices (`1`, `2` and `3` in 3D cases) to apply a load or constrain a DoF.
    Starting from `v4`, one must use `AXIAL`, `RS` and `RW` to achieve the same purpose.

    ```text
    node 1 0 0
    material Bilinear1D 1 10 .8 .02
    section Rectangle2D 1 12 1 1
    element SingleSection2D 1 1 1

    // use rs to apply a concentrated load of magnitude 3 to the strong axis bending DoF of node 1
    cload 1 0 3 rs 1
    ```
