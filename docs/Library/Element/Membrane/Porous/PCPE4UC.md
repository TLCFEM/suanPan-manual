# PCPE4UC

Bilinear Quadrilateral With Pore Pressure (Undrained)

* Number of Nodes: 4
* Number of DoFs: 2 (Solid Translation, Solid Translation)
* DoF Label: U1, U2
* Supports Body Force
* Constant Consistent Mass Matrix With Same Order Integration

![encoding](../../PIC/Q4.svg)

## Background

This is the four-node undrained member of the porous family described in full on [PCPE4DC](PCPE4DC.md).

It eliminates the fluid displacement field by imposing $\mathbf u_f=\mathbf u_s$, so that the fluid moves with the skeleton and no relative seepage is possible.

!!! info "deviation from theory"
    The undrained condition is imposed algebraically by tying the fluid displacement to the solid one.
    Pore pressure is recovered from the volumetric strain rather than solved as an independent field, so no pressure DoF or flow equation is present.

With $K_s$, $K_f$, $n$ and $\alpha$ as defined on the canonical page, the same pressure coefficient is used.

$$
q=\dfrac{K_sK_f}{nK_s+(\alpha-n)K_f}.
$$

Substituting $\varepsilon_f=\varepsilon_s$ into the pore energy of [PCPE4DC](PCPE4DC.md) gives the undrained constraint energy $\Psi_u=\tfrac12 q\alpha^2(\nabla\cdot\mathbf u_s)^2$ and the pore pressure $p=-\alpha q\,\nabla\cdot\mathbf u_s$.

The added stiffness is therefore

$$
\mathbf K_u=\int_V q\alpha^2\,\mathbf B^{\mathsf T}\mathbf m\mathbf m^{\mathsf T}\mathbf B\,dV ,
$$

which is exactly the `meta_k` matrix of the implementation, with $\mathbf m=(1,1,0)^{\mathsf T}$.

The element has no permeability argument and no viscous Darcy matrix, and its mass uses the mixture density $(1-n)\rho_s+n\rho_f$.

The recorded pore pressure `PP` is $-\alpha q$ times the volumetric strain at each of the four Gauss points.

## Syntax

```text title="PCPE4UC"
element PCPE4UC (1) (2...5) (6) (7) (8) (9)
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, solid material tag
# (7) int, fluid material tag
# (8) double, alpha
# (9) double, porosity n
```

## Remarks

Only plane strain is supported.
Plane stress does not make sense in geotechnical engineering.

For the fluid phase, an isotropic fluid material can be provided, which mainly provides the bulk modulus of the fluid phase.
For example,

```
# material Fluid (tag) (bulk modulus) (density)
material Fluid 1 1000. 1E-2
```

The $$\alpha$$ parameter `(8)` is often close to unity for soils.
The porosity $$n$$ ranges from zero to unity.
The isotropic permeability is assumed.

Interactions with other elements (with different arrangements of DoFs) can only be fulfilled via constraints.

* UC denotes the undrained variant, in which the fluid DoFs are suppressed and no permeability is supplied.
* The letter C is not expanded in the source, but the added stiffness is the undrained limit of the Biot consolidation model, so UC is read as undrained consolidation.
* The solid material must be plane strain (`PlaneType::E`), the fluid material must be isotropic (`MaterialType::DS`), and both must report a nonzero bulk modulus, otherwise initialization fails.

!!! warning "implementation limitation"
    Only plane strain and an isotropic fluid are accepted, and no permeability argument exists.
    The undrained constraint is exact for the chosen interpolation, but it cannot represent partial drainage or transient pore pressure dissipation.

* The fluid bulk modulus still affects the response through $q$ even though no fluid flow is modelled.
* Use [PCPE4DC](PCPE4DC.md) when drainage or time-dependent consolidation must be captured, and [PCPE8UC](PCPE8UC.md) for a quadratic undrained element.

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning |
|----------------|------------------|
| PP             | pore pressure    |

## References

1. Biot, M.A. (1941), General theory of three-dimensional consolidation, Journal of Applied Physics 12(2), 155--164, [doi:10.1063/1.1712886](https://doi.org/10.1063/1.1712886).
2. Zienkiewicz, O.C., Chang, C.T. and Bettess, P. (1980), Drained, undrained, consolidating and dynamic behaviour assumptions in soils, G\'eotechnique 30(4), 385--395, [doi:10.1680/geot.1980.30.4.385](https://doi.org/10.1680/geot.1980.30.4.385).
