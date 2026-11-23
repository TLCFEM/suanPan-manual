# DCP4

Bilinear Quadrilateral With Crack Phase

* Number of Nodes: 4
* Number of DoFs: 3 (Translation, Translation, Damage)
* DoF Label: U1, U2, DAMAGE
* Integration Scheme: 2nd Order Gauss
* Zero Mass Entries On Damage DoFs

![encoding](../../PIC/Q4.svg)

## Background

[`DCP4`](DCP4.md) implements the phase-field brittle-fracture formulation of [`DCP3`](DCP3.md) on the bilinear quadrilateral.
The energy functional is
$$
\Psi=\int_\Omega (1-d)^2\,\psi(\boldsymbol\varepsilon)\,\mathrm d\Omega+G_c\int_\Omega\left[\frac{d^2}{2l}+\frac{l}{2}|\nabla d|^2\right]\mathrm d\Omega,
$$
with $d$ the damage field, $G_c$ the energy release rate and $l$ the characteristic length.
The displacement and damage fields share the bilinear shape functions, so each node carries `U1`, `U2` and `DAMAGE`.
At each of the four Gauss points the strain is $\boldsymbol\varepsilon=\boldsymbol B\boldsymbol a$ and the local damage is $d=\sum_aN_ad_a$, which gives the degradation $g=(1-d)^2$.
The stiffness contributions are $g\,\boldsymbol B^\mathrm T\boldsymbol D\boldsymbol B$ for the displacement block and $G_c\big(l^{-1}\boldsymbol N^\mathrm T\boldsymbol N+l\,\boldsymbol B^\mathrm T\boldsymbol B\big)$ for the damage block.
The history field $\mathcal H=\max\psi$ drives damage evolution and prevents healing.

!!! info "deviation from theory"
    The implementation uses the total strain energy $\tfrac12\boldsymbol\varepsilon^\mathrm T\boldsymbol\sigma$ as the history field.
    No tensile-compressive spectral split is applied, so a compressive stress state can also increase the damage-driving variable.

The staggered version omits the displacement-damage coupling blocks, while `DCP4M` includes the term $-2(1-d)\boldsymbol B^\mathrm T\boldsymbol\sigma\boldsymbol N^\mathrm T$ in the off-diagonal blocks for a monolithic solve.
A $2\times2$ Gauss rule is used, and a negative characteristic length is replaced by $2\sqrt{A}$ from the element area.
See [`DCP3`](DCP3.md) for the derivation of the coupled equations and the role of the history variable.

## Syntax

```text title="DCP4"
element DCP4 (1) (2...5) (6) (7) (8) [9]
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, material tag
# (7) double, characteristic length
# (8) double, energy release rate
# [9] double, element thickness, default: 1.0
```

## Remarks

* The third DoF is the damage variable.
  Boundary conditions can be assigned.
* The characteristic length `(7)` can be set to a negative value to automatically determine it based on the element geometry.
* The energy release rate `(8)` is the fracture toughness $G_c$ used in the crack-surface energy.
* The damage DoF has zero mass entries, so the formulation is intended for quasi-static crack growth.
* One history variable is stored per Gauss point and is updated to the maximum strain energy seen so far.
* Use at least four to eight elements across the expected crack width $l$ for a smooth damage field.
* [`DCP4M`](DCP4.md) adds the coupling blocks for a monolithic solution, while the default `DCP4` uses a staggered scheme.

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning |
|----------------|------------------|
| DAMAGE         | damage variable  |

## Variants

`DCP4M` uses the same command `element DCP4M (1) (2...5) (6) (7) (8) [9]` as `DCP4`, but solves displacement and damage monolithically by adding their coupling blocks to the stiffness matrix instead of using a staggered update.

## References

1. G. Liu, G. Li, Q. M. Li, K. Zhang and L. Wang, *Abaqus implementation of monolithic and staggered schemes for quasi-static and dynamic fracture phase-field model*, Computational Materials Science 121, 35-47 (2016), [doi:10.1016/j.commatsci.2016.04.009](https://doi.org/10.1016/j.commatsci.2016.04.009).
2. C. Miehe, M. Hofacker and F. Welschinger, *A phase field model for rate-independent crack propagation: robust algorithmic implementation based on operator splits*, Computer Methods in Applied Mechanics and Engineering 199(45-48), 2765-2778 (2010), [doi:10.1016/j.cma.2010.04.016](https://doi.org/10.1016/j.cma.2010.04.016).
