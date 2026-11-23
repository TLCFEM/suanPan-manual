# PCPE4DC

Bilinear Quadrilateral With Pore Pressure (Drained)

* Number of Nodes: 4
* Number of DoFs: 4 (Solid Translation, Solid Translation, Fluid Translation, Fluid Translation)
* DoF Label: U1, U2, FU1, FU2
* Supports Body Force
* Constant Consistent Mass Matrix With Same Order Integration

![encoding](../../PIC/Q4.svg)

## Theory

This is the four-node member of the drained consolidation family, whose siblings are [PCPE8DC](PCPE8DC.md), [PCPE4UC](PCPE4UC.md) and [PCPE8UC](PCPE8UC.md).

It implements the $u$--$U$ formulation of saturated porous media, in which the solid displacement $\mathbf u_s$ and the fluid displacement $\mathbf u_f$ have independent nodal degrees of freedom.

The formulation follows the drained and undrained assumptions of Biot consolidation theory as classified by Zienkiewicz, Chang and Bettess.

!!! info "deviation from theory"
    This is a $u$--$U$ mixture element rather than the more common $u$--$p$ consolidation element.
    Pore pressure is not a nodal unknown, and the coupling blocks use $(\alpha-n)$ and $n$ rather than a single Biot coefficient $\alpha$ multiplying a pressure shape function.

Let $K_s$ be the bulk modulus reported by the solid material, $K_f$ the bulk modulus of the fluid material, $n$ the porosity and $\alpha$ the Biot coefficient.

The code first forms the pressure coefficient

$$
q=\dfrac{K_sK_f}{nK_s+(\alpha-n)K_f}=\left(\dfrac{n}{K_f}+\dfrac{\alpha-n}{K_s}\right)^{-1}.
$$

This is the inverse of the storage compliance of the two compressible phases.

Define the volumetric strains $\varepsilon_s=\nabla\cdot\mathbf u_s$ and $\varepsilon_f=\nabla\cdot\mathbf u_f$.

The strain energy stored by the pore fluid is

$$
\Psi_f=\dfrac{q}{2}\big[(\alpha-n)\varepsilon_s+n\varepsilon_f\big]^2,
$$

and the pore pressure reported by the element is

$$
p=-q\big[(\alpha-n)\varepsilon_s+n\varepsilon_f\big].
$$

With $\mathbf B_s$ the solid strain--displacement matrix, $\mathbf B_f$ the fluid one and $\mathbf m=(1,1,0)^{\mathsf T}$ mapping volumetric strain into the three-plane-strain components, the discrete fluid stiffness is

$$
\mathbf K_f=\int_V q
\begin{bmatrix}
(\alpha-n)^2\mathbf m\mathbf m^{\mathsf T} & n(\alpha-n)\mathbf m\mathbf m^{\mathsf T}\\
n(\alpha-n)\mathbf m\mathbf m^{\mathsf T} & n^2\mathbf m\mathbf m^{\mathsf T}
\end{bmatrix}\,dV .
$$

This reproduces exactly the four blocks `meta_k(s_dof,s_dof)`, `meta_k(s_dof,f_dof)`, `meta_k(f_dof,s_dof)` and `meta_k(f_dof,f_dof)` of the implementation.

The effective stress is carried by the solid material, so the remaining stiffness is the usual $\int\mathbf B_s^{\mathsf T}\mathbf D\mathbf B_s\,dV$ evaluated by 2-by-2 Gauss integration at four points.

Darcy seepage is represented by a drag force proportional to the relative velocity $\mathbf v_s-\mathbf v_f$, with coefficient $n^2/k$ per unit volume.

This produces the constant viscous matrix

$$
\mathbf C=\dfrac{n^2}{k}\int_V
\begin{bmatrix}
\mathbf N^{\mathsf T}\mathbf N & -\mathbf N^{\mathsf T}\mathbf N\\
-\mathbf N^{\mathsf T}\mathbf N & \mathbf N^{\mathsf T}\mathbf N
\end{bmatrix}\,dV ,
$$

so that only relative motion of the two phases dissipates energy.

The consistent mass matrix uses $(1-n)\rho_s$ on the solid DoFs and $n\rho_f$ on the fluid DoFs, and the body force is split in the same proportions.

Both damping and mass are installed once during initialization through `ConstantDamping` and `ConstantMass`.

!!! warning "implementation limitation"
    Seepage is stored as a constant velocity-proportional damping matrix rather than as a time-integrated flux.
    Drainage is therefore a rate effect, and a purely static analysis has no mechanism to dissipate pore pressure.

## Syntax

```text title="PCPE4DC"
element PCPE4DC (1) (2...5) (6) (7) (8) (9) (10)
# (1) int, unique element tag
# (2...5) int, node i, j, k, l
# (6) int, solid material tag
# (7) int, fluid material tag
# (8) double, alpha
# (9) double, porosity n
# (10) double, permeability k
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

* DC denotes the drained variant, where the fluid phase has its own displacement DoFs and can flow relative to the solid through the permeability argument.
* The letter C is not expanded in the source, but the bulk modulus and Darcy drag terms are those of a Biot consolidation model, so DC is read as drained consolidation.
* [PCPE4UC](PCPE4UC.md) is the undrained counterpart, which eliminates the fluid DoFs by assuming $\mathbf u_f=\mathbf u_s$ and therefore takes no permeability argument.
* The solid material must be plane strain (`PlaneType::E`), the fluid material must be isotropic (`MaterialType::DS`), and both must report a nonzero bulk modulus, otherwise initialization fails.

!!! warning "implementation limitation"
    The permeability is a single isotropic scalar, so anisotropy and tensor permeability cannot be represented.
    A zero permeability is not a valid input because it appears in the denominator of the drag matrix.

* The permeability $k$ appears in the denominator of the viscous matrix, so it must be strictly positive and expressed in units consistent with the drag term $n^2/k$.
* Because seepage is a velocity-proportional damping term, pore pressure dissipation requires a transient or dynamic analysis step, while a purely static step has no time scale for consolidation.
* Fluid DoFs are labelled `FU1` and `FU2` and can be restrained with commands such as `fix 3 fu1 1 2 3 4`.
* The recorded pore pressure `PP` is sampled at the four Gauss points, and other recorded quantities are forwarded to the solid material.
* Use [PCPE8DC](PCPE8DC.md) for a quadratic approximation with five-point Irons integration when higher accuracy per element is needed.

## Example

```text
node 1 0 0
node 2 2 0
node 3 2 2
node 4 0 2
material Elastic2D 1 1500. 0.25 1E-4 1
material Fluid 2 1000. 1E-4
element PCPE4DC 1 1 2 3 4 1 2 1. 0.8 10.
```

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning |
|----------------|------------------|
| PP             | pore pressure    |

## References

1. Biot, M.A. (1941), General theory of three-dimensional consolidation, Journal of Applied Physics 12(2), 155--164, [doi:10.1063/1.1712886](https://doi.org/10.1063/1.1712886).
2. Zienkiewicz, O.C., Chang, C.T. and Bettess, P. (1980), Drained, undrained, consolidating and dynamic behaviour assumptions in soils, G\'eotechnique 30(4), 385--395, [doi:10.1680/geot.1980.30.4.385](https://doi.org/10.1680/geot.1980.30.4.385).
3. Zienkiewicz, O.C. and Taylor, R.L., The Finite Element Method, Volume 2: Solid Mechanics, Butterworth-Heinemann.
