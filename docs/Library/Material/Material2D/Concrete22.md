# Concrete22

Fixed Crack Concrete Model

## Syntax

```
material Concrete22 (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) (11) [12]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, compression strength, should be negative but sign insensitive
# (4) double, tension strength, should be positive but sign insensitive
# (5) double, NC
# (6) double, NT
# (7) double, middle point
# (8) double, strain at compression strength
# (9) double, strain at tension strength
# (10) double, shear stress
# (11) double, shear retention factor
# [12] double, density, default: 0.0
```
