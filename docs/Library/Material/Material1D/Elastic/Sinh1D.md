# Sinh1D

Uniaxial Elastic Material Using $$\sinh$$

## Syntax

```
material Elastic1D (1) (2) [3]
# (1) int, unique material tag
# (2) double, elastic modulus
# [3] double, density, default: 0.0
```

## Theory

The constitutive equation is defined as

$$
\sigma=E\sinh(\epsilon),
$$

where $$E$$ is the elastic modulus and $$\epsilon$$ is the strain.
