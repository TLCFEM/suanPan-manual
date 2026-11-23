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

The local driving measure is $\Phi=\tfrac12\boldsymbol\sigma^\ast:\mathbf D^{-1}:\boldsymbol\sigma^\ast-E_\max$, where $\mathbf D$ is the elastic stiffness and $\boldsymbol\sigma^\ast$ is the tensile part of the deviatoric trial stress obtained from a spectral split.
The parser selects this `DEV_TENSILE` measure, while the `TOTAL` and `TENSILE` variants exist in the class but cannot be chosen from the command line.

!!! warning "implementation limitation"
    The `TOTAL` and `TENSILE` energy measures are unreachable from the input file.

!!! note "developer note"
    The parser always passes `EnergyType::DEV_TENSILE` to the constructor.

The nonlocal field $k$ is carried by the seventh material degree of freedom and enters a gradient term with coefficient $s=[h\ln(1+k)+1]/l$, where $h$ is the diffusion rate and $l$ is the reference length.

!!! info "deviation from theory"
    The gradient coefficient depends nonlinearly on the nonlocal field through $s=[h\ln(1+k)+1]/l$ rather than being a constant.
    Both $s$ and its derivative $\mathrm ds/\mathrm dk=h/[l(1+k)]$ enter the nonlocal tangent.

When the excess energy $\Delta=\Phi$ grows beyond the stored maximum, the damage becomes $d=r^2/(1+r^2)$ with $r=h_\mathrm{ev}(\sqrt{\Delta/E_\max+1}-1)$ and $h_\mathrm{ev}$ the evolution rate.
The elastic stress is multiplied by $1-d$ and the consistent tangent includes the coupling between the mechanical strain and the nonlocal field.

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

!!! warning "implementation limitation"
    All six numerical arguments are converted to their absolute values, so negative values are silently replaced rather than rejected.

Below the maximum energy the response is ordinary isotropic elasticity.
The reference length $l$ and diffusion rate $h$ together set the gradient length scale $s$, so a larger $l$ spreads the degradation over a wider zone.
The evolution rate $h_\mathrm{ev}$ controls how rapidly damage saturates once the energy threshold is exceeded.
The seventh degree of freedom is the nonlocal field and must be supplied by a nonlocal element such as [`NonlocalC3D8`](../../../Element/Cube/C3D8.md), which adds an NL1 DoF at every node.

!!! warning "implementation limitation"
    A standard solid element does not provide the seventh degree of freedom and cannot be used with this material.

The stored maximum energy is a monotonically increasing history variable, so unloading does not heal the damage.

## Example

```text
material NonlocalElastic3D 1 1E4 .2 1e1 2. 1. 1e1
```
