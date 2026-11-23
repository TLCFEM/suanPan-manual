# SphericalParticle2D

Spherical DEM Particle in 2D

A discrete-element particle that attaches a circular disc of given radius to a single node and carries the properties used by pairwise particle interactions: elastic modulus, Poisson ratio and damping, together with its mass.
The element defines no stiffness of its own; it contributes a constant diagonal mass matrix and exposes its parameters to the DEM contact constraints.

* Number of Nodes: 1
* Number of DoFs: 2 (Translation, Translation), or 3 if inertia is supplied
* DoF Label: U1, U2, optionally UR3
* Element Type: DEM
* Constant Mass Matrix, No Stiffness

## Background

The discrete element method (DEM) represents a particulate assembly as individual bodies whose motion is integrated in time and whose interactions are evaluated pairwise at contacts.
A `SphericalParticle2D` element attaches a circular disc of radius $R$ to one node and stores the parameters needed to evaluate a contact, but it defines no stiffness of its own.
It contributes only a constant diagonal mass matrix, $\mathrm{diag}(m,m)$, or $\mathrm{diag}(m,m,I)$ when rotational inertia is supplied.

For two particles $i$ and $j$ with centre distance $d$, the overlap or compression is

$$
\delta=R_i+R_j-d .
$$

A contact exists only for $\delta>0$.
The implementation uses a Hertzian normal law, with pair properties

$$
E^*=\left[\dfrac{1-\nu_i^2}{E_i}+\dfrac{1-\nu_j^2}{E_j}\right]^{-1},
\qquad
R^*=\left[\dfrac1{R_i}+\dfrac1{R_j}\right]^{-1},
\qquad
\eta^*=\dfrac{\eta_i+\eta_j}{2}.
$$

The elastic normal force magnitude is $\frac43 E^*\sqrt{R^*\,\delta}\,\delta$, and a viscous contribution proportional to the relative normal velocity is superposed, so the contact force is repulsive along the line of centres and the damping opposes the relative approach.
The contact force is distributed to the two nodes with equal magnitude and opposite sign, and its linearisation contributes to the global stiffness and damping matrices.

General DEM formulations often add a tangential spring and Coulomb friction, but the current `Hertzian` interaction is frictionless and acts only along the line of centres.
Neighbour search is performed with a cell list whose cell size is twice the largest particle radius.

!!! warning "implementation limitation"
    The `Hertzian` interaction implements only the normal force law.
    Tangential springs and Coulomb friction, which are standard in DEM, are absent.

!!! warning "implementation limitation"
    Rotational inertia is stored on the particle, but the contact law uses only translational positions and velocities.
    The `MolecularDynamics2D` constraint is instantiated with rotation disabled, so rotational DoFs do not affect pairwise contact.

## Syntax

```text title="SphericalParticle2D"
element SphericalParticle2D (1) (2) (3) (4) (5) (6) (7) [8]
# (1) int, unique element tag
# (2) int, node tag
# (3) double, particle radius
# (4) double, elastic modulus
# (5) double, Poisson ratio
# (6) double, damping
# (7) double, mass
# [8] double, optional rotational inertia
```

## Remarks

1. With five parameters `(3)...(7)`, the element is `SphericalParticle2D`: it has DoFs U1 and U2 and a mass matrix $$\mathrm{diag}(m,m)$$.
2. If the inertia `(8)` is given, `InertialSphericalParticle2D` is created instead: the UR3 DoF is added and the mass matrix becomes $$\mathrm{diag}(m,m,I)$$.
3. The radius, damping, elastic modulus and Poisson ratio are read by DEM interactions to build the effective radius, damping and modulus of a particle pair, so use a unit system consistent with the rest of the model.
4. Use this element together with an [interaction](../../../Collection/Define/interaction.md) and a `MolecularDynamics2D` constraint, as in the `Other/MD2D` example.
5. The interaction reads radius, elastic modulus, Poisson ratio and damping through the element parameter interface, while the mass only enters the diagonal mass matrix.
6. The storage scheme must be `full`, `sparse` or `sparse symmetric` so that the constraint can assemble the contact contributions into the global matrices.
7. The spatial variant with the same contact law is [`SphericalParticle3D`](SphericalParticle3D.md).

## References

1. P. A. Cundall and O. D. L. Strack, "A discrete numerical model for granular assemblies", *Géotechnique*, 29(1):47--65, 1979, [10.1680/geot.1979.29.1.47](https://doi.org/10.1680/geot.1979.29.1.47).
2. H. Hertz, "Über die Berührung fester elastischer Körper", *Journal für die reine und angewandte Mathematik*, 92:156--171, 1882.
3. K. L. Johnson, *Contact Mechanics*, Cambridge University Press, 1985.

## Example

```text
element SphericalParticle2D 1 1 1. 1e3 .2 1e-4 1.
```
