# Gap01

Uniaxial gap material with no compressive resistance and bilinear elastic-perfectly plastic response in tension.

## Syntax

```text title="Gap01"
material Gap01 (1) (2) (3) [4] [5]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, yield stress
# [4] double, gap strain, default: 0.0
# [5] double, density, default: 0.0
```

## Background

The material carries no stress in compression and yields at a fixed tensile stress.
On reloading from zero stress, the strain must first close the gap before tensile stress develops.
The `gap strain` `(4)` is the strain offset measured from the stress-free reference to the point where tension starts.

## Remarks

The modulus, yield stress and gap strain are all converted to absolute values, so their signs do not matter.
The stress is clamped to zero in compression and to the yield stress in tension, and the tangent stiffness is zero in both clamped states.
A `gap strain` of zero, the default, gives an ordinary elastic-perfectly plastic tensile model without a gap.
