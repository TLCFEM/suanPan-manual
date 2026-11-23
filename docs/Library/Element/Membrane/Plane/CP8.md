# CP8

Second Order Quadrilateral

* Number of Nodes: 8
* Number of DoFs: 2 (Translation, Translation)
* DoF Label: U1, U2
* Integration Scheme: 2nd Order Irons (Full) or 2nd Order Gauss (Reduced)
* Supports Body Force
* Constant Consistent Mass Matrix With Same Order Integration

![encoding](../../PIC/Q8.svg)

## Syntax

```text title="CP8"
element CP8 (1) (2...9) (10) [11] [12] [13]
# (1) int, unique element tag
# (2...9) int, node 1 to node 8
# (10) int, material tag
# [11] double, element thickness, default: 1.0
# [12] bool string, reduced integration switch, default: false
# [13] bool string, nonlinear geometry switch, default: false
```

## Remarks

* The `CP8` element resembles CPS8, CPE8, CPS8R and CPE8R elements in ABAQUS.
* The full integration scheme uses 3-by-3 Gauss scheme and the reduced integration uses a 2-by-2 scheme.

## Variants

The plane stress or plane strain behaviour is set by the material's plane type, not by the element token; a plane-strain material forces unit thickness.
`CPS8` is the plane-stress name for the same `CP8` implementation and accepts the identical `element CPS8 (1) (2...9) (10) [11] [12] [13]` arguments.
`CPE8` is the plane-strain counterpart; `element CPE8 (1) (2...9) (10) [11] [12]` omits the thickness argument and takes the optional reduced-integration and nonlinear-geometry switches.
`CPE8R` is the plane-strain variant with reduced integration forced; `element CPE8R (1) (2...9) (10) [11]` accepts only the nonlinear-geometry switch.
