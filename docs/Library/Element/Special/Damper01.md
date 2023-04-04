# Damper01/Damper03

Viscous/Nonviscous Damper

This damper uses **displacement** and **velocity** as inputs, not strain and strain rate, which means element length is
not used to compute strain or strain rate.

## Damper01

This `Damper01` is a simple 2D viscous/nonviscous damper.

See this [example](../../../Example/Structural/Dynamics/dynamic-analysis-of-a-portal-frame.md).

* Number of Nodes: 2
* Number of DoFs: 2 (Translation: UX, Translation: UY)

## Damper03

This `Damper03` is a simple 3D viscous/nonviscous damper.

* Number of Nodes: 2
* Number of DoFs: 3 (Translation: UX, Translation: UY, Translation: UZ)

## Syntax

```
element Damper01 (1) (2) (3) (4)
element Damper03 (1) (2) (3) (4)
# (1) int, unique tag
# (2) int, node i
# (3) int, node j
# (4) int, material tag of associated (non)viscosity material
```

## Remarks

Both viscous and nonviscous material can be used for this element, see [Viscosity](../../Material/Material1D/Viscosity).