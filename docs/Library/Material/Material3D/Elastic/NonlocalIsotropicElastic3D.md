# NonlocalIsotropicElastic3D

Isotropic Elastic Material With Gradient-Enhanced Damage

The `NonlocalIsotropicElastic3D` token implements three-dimensional linear isotropic elasticity, as in [`IsotropicElastic3D`](IsotropicElastic3D.md), coupled to a nonlocal, damage-like variable carried by a seventh material degree of freedom.
Once a strain-energy measure exceeds a prescribed maximum, the variable grows and degrades the stress, providing a regularised softening response.
`NonlocalElastic3D` is accepted as a short alias and takes the same arguments.
The material must be used with a nonlocal element such as `NonlocalC3D8`.

## Theory

The driving energy is $$\tfrac12\boldsymbol\sigma^\ast:\mathbf E^{-1}:\boldsymbol\sigma^\ast-\text{maximum\_energy}$$, where $$\boldsymbol\sigma^\ast$$ is the deviatoric tensile part of the trial stress.
A scalar damage variable $$d=1-\bigl[1+(r(\sqrt{\Delta/e_\text{max}+1}-1))^2\bigr]^{-1}$$ evolves with the excessive energy $$\Delta$$ at evolution rate $$r$$, and the stress is scaled by $$1-d$$.
The reference length sets the gradient length scale and the diffusion rate controls spatial coupling of the nonlocal field.

## Syntax

```text title="NonlocalIsotropicElastic3D"
material NonlocalIsotropicElastic3D (1) (2) (3) (4) (5) (6) (7) [8]
material NonlocalElastic3D (1) (2) (3) (4) (5) (6) (7) [8]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) double, maximum energy
# (5) double, evolution rate
# (6) double, reference length
# (7) double, diffusion rate
# [8] double, density, default: 0.0
```

## Remarks

The parser fixes the energy measure to the deviatoric tensile part of the stress; the other energy types available in the class cannot be selected from the command line.
All six numerical parameters are converted to their absolute values.
Below the maximum energy the response is ordinary isotropic elasticity.

## Example

```text
material NonlocalElastic3D 1 1E4 .2 1e1 2. 1. 1e1
```
