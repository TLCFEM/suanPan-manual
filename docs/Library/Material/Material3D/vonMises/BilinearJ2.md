# BilinearJ2

Bilinear J2 Plasticity

## Syntax

```text title="BilinearJ2"
material BilinearJ2 (1) (2) (3) (4) [5] [6] [7]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, yield stress
# [5] double, hardening ratio, default: 0.0
# [6] double, beta, default: 1.0
# [7] double, density, default: 0.0
```

## Variants

The `NonlocalBilinearJ2` token keeps this bilinear J2 backbone and adds a nonlocal failure variable stored in a seventh material degree of freedom.
The variable grows once the equivalent plastic strain exceeds a threshold and degrades the stress by a scalar factor, giving strain-softening with a regularised length scale.
It requires seven compulsory parameters: the elastic modulus, Poisson's ratio and yield stress as above, then `(5)` plastic strain threshold, `(6)` evolution rate, `(7)` reference length and `(8)` diffusion rate, followed by the optional hardening ratio, beta and density.
The reference length sets the gradient length scale and the diffusion rate controls spatial coupling of the nonlocal field.
It must be used with a nonlocal element such as `NonlocalC3D8`.
A minimal invocation is `material NonlocalBilinearJ2 1 1E4 .2 200 .1 5. 1. 100. .02`.
