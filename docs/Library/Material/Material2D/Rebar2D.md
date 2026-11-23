# Rebar2D

Orthotropic Material

## Background

The `Rebar2D` model is a smeared reinforcement layer that adds the uniaxial response of two orthogonal steel families to a two-dimensional plane-stress continuum.
Each family is described by a one-dimensional host material, so the steel can be elastic, elastoplastic or hysteretic without any change to the reinforcement formulation.
If $\rho_x$ and $\rho_y$ are the reinforcement ratios, the added in-plane stress is
$$
\boldsymbol\sigma^{\mathrm{reb}}=\begin{bmatrix}\rho_x\sigma_{sx}(\varepsilon_{11})\\\rho_y\sigma_{sy}(\varepsilon_{22})\\0\end{bmatrix},\qquad
\mathbf K^{\mathrm{reb}}=\begin{bmatrix}\rho_x E_{sx}^{t}&0&0\\0&\rho_y E_{sy}^{t}&0\\0&0&0\end{bmatrix},
$$
where $E_{sx}^{t}$ and $E_{sy}^{t}$ are the current tangent moduli of the two steel models.
The shear term is identically zero because a smeared bar layer carries only axial force along its own direction and has no dowel or bond-slip shear stiffness.

!!! warning "implementation limitation"
    The stiffness matrix has a zero shear entry, so the reinforcement layer contributes no in-plane shear resistance.
    Dowel action, bond slip and bar kinking across a crack are not represented.

The density is similarly smeared as $\rho=\rho_x\rho_{s,x}+\rho_y\rho_{s,y}$, where $\rho_{s,x}$ and $\rho_{s,y}$ are the densities returned by the two host materials.

## Syntax

```text title="Rebar2D"
material Rebar2D (1) (2) (3) (4) (5)
# (1) int, unique material tag
# (2) int, x direction steel material tag
# (3) int, y direction steel material tag
# (4) double, x direction reinforcement ratio
# (5) double, y direction reinforcement ratio
```

The uniform reinforcement is defined along global axes.
To have arbitrarily aligned layout, users can wrap it into a [`Rotation2D`](../Wrapper/Rotation2D.md) wrapper.

## Remarks

* The two host material tags must refer to one-dimensional materials, since the source rejects any host whose material type is not `D1`.
* Each host material is copied from the domain at initialisation, so the same steel tag can be reused by several reinforcement layers without sharing history state.
* The reinforcement ratios are dimensionless area fractions of the layer and are usually of order $10^{-3}$ to $10^{-2}$ for a reinforced concrete membrane.
* Because the shear stiffness is zero, `Rebar2D` cannot be used alone in a continuum element; combine it with a concrete model through the [`Laminated`](../Wrapper/Laminated.md) wrapper.
* The wrapper sums stresses and stiffnesses of all constituent 2D models, so it plays the same role for plane materials that the [`Parallel`](../Wrapper/Parallel.md) wrapper plays for one-dimensional materials.
* Compression is handled by the steel host material, so buckling, crimping and bond slip are not represented unless the chosen one-dimensional law includes them.
* The model has `PlaneType::S`, so it must be used with plane-stress elements such as [CP4](../../Element/Membrane/Plane/CP4.md); for a three-dimensional reinforcement layout use `Rebar3D`.

!!! info "deviation from theory"
    The two bar directions are fixed to the global axes by the class itself.
    Inclined reinforcement is only obtained by wrapping the whole layer in [`Rotation2D`](../Wrapper/Rotation2D.md), which rotates the strain into the local bar axes before calling the steel models.

## Example

```text
material Elastic1D 1 2E5
material Elastic1D 2 2E5
material Rebar2D 3 1 2 .01 .005
material Concrete21 4 3E4 -30 3 2 2 .3 -2E-3 1E-4
material Laminated 5 3 4
```

Material 5 provides a smeared reinforced concrete membrane, with 1% steel in the global $x$ direction and 0.5% in the global $y$ direction.
