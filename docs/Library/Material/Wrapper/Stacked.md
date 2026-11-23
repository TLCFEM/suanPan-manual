# Stacked

Parallel Wrapper For 3D Material Models

Combines multiple 3D material models into a single one.

## Theory

A stacked material is the three-dimensional form of the iso-strain or Voigt assumption.
Every constituent is subjected to the same six-component Voigt strain $$\mathbf e=(\varepsilon_{11},\varepsilon_{22},\varepsilon_{33},\gamma_{12},\gamma_{23},\gamma_{13})$$, and the overall stress and tangent are the sums of the constituent quantities,

$$
\mathbf s(\mathbf e)=\sum_{k=1}^{n}\mathbf s^{(k)}(\mathbf e),
\qquad
\mathbf D(\mathbf e)=\sum_{k=1}^{n}\mathbf D^{(k)}(\mathbf e).
$$

For constituents with volume fractions $$f_k$$ the physical mixture rule is $$\mathbf s=\sum_k f_k\mathbf s^{(k)}$$, so the fractions must be included in the material parameters because the wrapper applies no weighting.

!!! info "deviation from theory"
    The wrapper sums stresses and tangents with unit weight, so the Voigt mixture rule is recovered only when all volume fractions $$f_k$$ are equal.
    Any weighting must be built into the constituent parameters or the section assigned to the element, since no fraction is read from the input.

The rule is the upper bound on the effective stiffness of a composite, complementary to the iso-stress lower bound represented in one dimension by [Sequential](Sequential.md).
In terms of energy, the free energies of the constituents add under the common strain, which is consistent with a parallel rheological interpretation.

The implementation makes a copy of each listed 3D material, drives every copy with the same trial strain, and sums the returned stresses and tangents.
Densities and initial stiffnesses are summed during initialization, and recorded histories are concatenated in tag order.

This is the three-dimensional counterpart of [Laminated](Laminated.md) for 2D models and of [Parallel](Parallel.md) for 1D models.
Use [Rotation3D](Rotation3D.md) on any constituent whose material frame differs from the global frame.

## Syntax

```text title="Stacked"
material Stacked (1) (2...)
# (1) int, unique material tag
# (2...) int, material tags of 3D models need to be contained
```

The response of attached 3D material models will be output when recorded.
The output has a uniform size and data is arranged in the order as defined.

## Remarks

Every listed tag must refer to a registered 3D material, and the wrapper reports a six-component stress and stiffness to solid elements.
The wrapper skips the update entirely when the strain increment is below the internal tolerance, which is harmless for rate-independent hosts but worth noting for rate-dependent ones.

!!! warning "implementation limitation"
    A rate-dependent host cannot evolve in a step whose strain increment falls below the internal tolerance.

!!! note "developer note"
    `Stacked::update_trial_status` returns immediately when the strain-increment norm is below `datum::eps`, so none of the constituents is re-evaluated.

No local equilibrium solve is performed since compatibility is enforced by giving all constituents the same strain; the model cannot represent load shedding caused by different strains.
Use [Laminated](Laminated.md) when a 2D reduction is required, and [PlaneStress](PlaneStress.md) or [PlaneStrain](PlaneStrain.md) inside the stack for reduced constituents.

## References

- [10.1016/0022-5096(63)90036-X](https://doi.org/10.1016/0022-5096(63)90036-X)
- [ISBN 978-1-56032-712-7](https://search.worldcat.org/search?q=bn:9781560327127)
