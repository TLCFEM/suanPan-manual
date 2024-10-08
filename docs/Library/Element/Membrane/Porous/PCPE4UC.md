# PCPE4UC

Bilinear Quadrilateral With Pore Pressure (Undrained)

* Number of Nodes: 4
* Number of DoFs: 4 (Solid Translation, Solid Translation, Fluid Translation, Fluid Translation)
* Supports Body Force
* Constant Consistent Mass Matrix With Same Order Integration

![encoding](../../PIC/Q4.svg)

## Syntax

```
element PCPE4UC (1) (2...5) (6) (7) (8) (9)
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, solid material tag
# (7) int, fluid material tag
# (8) double, alpha
# (9) double, porosity n
```

## Remarks

Only plane strain is supported. Plane stress does not make sense in geotechnical engineering.

For fluid phase, an isotropic fluid material can be provided, it mainly provides the bulk modulus of the fluid phase.
For example,

```
# material Fluid (tag) (bulk modulus) (density)
material Fluid 1 1000. 1E-2
```

The $$\alpha$$ parameter `(8)` is often close to unity for soils. The porosity $$n$$ ranges from zero to unity. The
isotropic permeability is assumed.

Interactions with other elements (with different arrangements of DoFs) can only be fulfilled via constraints.

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning |
|----------------|------------------|
| PP             | pore pressure    |
