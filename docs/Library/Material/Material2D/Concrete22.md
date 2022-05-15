# Concrete22

Fixed Crack Concrete Model

## Syntax

```
material Concrete22 (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) (11) (12) [13]
# (1) int, unique material tag
# (2) double, compression strength, should be negative but sign insensitive
# (3) double, tension strength, should be positive but sign insensitive
# (4) double, MC
# (5) double, NC
# (6) double, MT
# (7) double, NT
# (8) double, middle point
# (9) double, strain at compression strength
# (10) double, strain at tension strength
# (11) double, shear stress
# (12) double, shear retention factor
# [13] double, density, default: 0.0
```
