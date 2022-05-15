# Damper01

Viscous Damper

This `Damper01` is a simple viscous damper. This damper uses **displacement** and **velocity** as inputs, not strain and
strain rate, that is, element length is not used to compute strain or strain rate.

See this [example](../../../Example/Structural/Dynamics/dynamic-analysis-of-a-portal-frame.md).

* Number of Nodes: 2
* Number of DoFs: 2 (Translation, Translation)

## Syntax

```
element Damper01 (1) (2) (3) (4)
# (1) int, unique tag
# (2) int, node i
# (3) int, node j
# (4) int, material tag of associated viscosity material
```