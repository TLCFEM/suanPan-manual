# SGCMS

Simplified Generalized Conforming Mixed Shell Element

A planar shell element uses SGCMQ for membrane action and DKT4 element for plate action.

* Number of Nodes: 4
* Number of DoFs: 6 (Translation, Translation, Translation, Rotation, Rotation, Rotation)
* Integration Membrane: Five-Point Irons Scheme
* Integration Plate: 3rd Gauss Scheme

## Syntax

```
element SGCMS (1) (2...5) (6) (7) [8]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# (7) double, thickness
# [8] bool, nonlinear geometry switch, default: false
```

## Remarks

1. If the nonlinear geometry switched on, the transformation between the global and local reference frames will depend
   on the current displacement. The nonlinear transformation is similar to the corotational transformation, and the
   local response is still linear. Thus, it follows "large displacement, small deformation" assumption.
