# ISection3D

3D I-Section

![arrangement](PIC/ISection.svg)

## Syntax

```text title="ISection3D"
section ISection3D (1) (2) (3) (4) (5) (6) (7) (8) [9] [10] [11]
# (1) int, unique section tag
# (2) double, top flange width
# (3) double, top flange thickness
# (4) double, bottom flange width
# (5) double, bottom flange thickness
# (6) double, web height
# (7) double, web thickness
# (8) int, material tag
# [9] int, number of integration points, default: 6
# [10] double, eccentricity along y axis, default: 0.0
# [11] double, eccentricity along z axis, default: 0.0
```

## Remarks

1. The flange/web is assumed to be slender.
   Thus, only one integration point is assigned across the thickness.
   The web, top flange and bottom flange share the same number of integration points over the height/width no matter how wide/tall the section is.
2. If either flange thickness exceeds 10% of the web height, both flanges will use two integration point layers through their thickness.
3. If the web thickness exceeds 10% of the larger flange width, the web will use two integration point layers through its thickness.

See [Eccentricity](../Eccentricity.md) for more details.

## Variants

The `ISection3DC` variant builds the same section but places its reference axis at the barycenter.

It is registered as `new_isection3d<true>`, which computes the eccentricity along the y axis from the section dimensions instead of reading the eccentricity arguments from the command.

This removes the default zero eccentricity that would otherwise introduce extra bending moments under axial force when the flanges differ in size.

The integration point argument is still accepted, but any user-supplied eccentricity is ignored.

See [Eccentricity](../Eccentricity.md) for more details.
