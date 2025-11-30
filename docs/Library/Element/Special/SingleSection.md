# SingleSection

Single Section Analysis

- 2D:
  * Number of DoFs: 2 (AXIAL, STRONG AXIS ROTATION)
- 3D:
  * Number of DoFs: 3 (AXIAL, STRONG AXIS ROTATION, WEAK AXIS ROTATION)

It is often demanded to do a section analysis to see the capacity of the target section, etc.
The `SingleSection` element is exactly for this purpose.

To use the element, a proper section shall be defined.

## Syntax

```
element SingleSection2D (1) (2) (3)
element SingleSection3D (1) (2) (3)
# (1) int, unique tag
# (2) int, node tag
# (3) int, section tag
```

## Remarks

It directly exposes the associated section.

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
