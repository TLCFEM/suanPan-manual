# Concrete21

Rotating Concrete Model

## Reference

1. [10.1061/(ASCE)0733-9399(1989)115:3(578)](https://doi.org/10.1061/(ASCE)0733-9399(1989)115:3(578))

## Syntax

```
material Concrete21 (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) [11]
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
# [11] double, density, default: 0.
```

## Theory

The `Concrete21` material model implements the smeared rotating crack model for concrete. In general, it takes in-plane strain vector as the input, converts it into principal strains and calls uniaxial material models to compute uniaxial stress and stiffness response. These ae rotated back to the nominal direction using the same eigen vectors.

The underlying uniaxial concrete model used is the [`ConcreteTsai`](../Material1D/Concrete/ConcreteTsai.md) model.

The formulation can be interpreted via two approaches. One in pure mathematics style and the other from engineering perspective.

Fundamentally, the stress response is an isotropic tensor function of in-plane strain tensor. One can refer to [10.1002/cnm.1640091105](https://doi.org/10.1002/cnm.1640091105) for a more general derivation of stiffness, which eventually gives the same expression as shown in [10.1061/(ASCE)0733-9399(1989)115:3(578)](https://doi.org/10.1061/(ASCE)0733-9399(1989)115:3(578)).



