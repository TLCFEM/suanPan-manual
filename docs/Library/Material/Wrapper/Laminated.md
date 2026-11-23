# Laminated

Parallel Wrapper For 2D Material Models

Combines multiple 2D material models into a single one.

## Theory

A laminate is an assembly of layers bonded together so that all layers share the same in-plane deformation.
For a two-dimensional strain vector $$\mathbf e=(\varepsilon_{11},\varepsilon_{22},\gamma_{12})$$, the iso-strain assumption gives $$\mathbf e^{(k)}=\mathbf e$$ for every layer $$k$$, and the resultant stress and tangent are obtained by summation,

$$
\mathbf s(\mathbf e)=\sum_{k=1}^{n}\mathbf s^{(k)}(\mathbf e),
\qquad
\mathbf D(\mathbf e)=\sum_{k=1}^{n}\mathbf D^{(k)}(\mathbf e).
$$

If the layers have thicknesses $$t_k$$, a physical laminate stress resultant is $$\mathbf N=\sum_k t_k\mathbf s^{(k)}$$, so the thickness weighting must be absorbed into the parameters or the section assigned to the element, since the wrapper performs an unweighted sum.
Classical lamination theory instead builds extensional, coupling and bending matrices from the through-thickness distribution of $$\mathbf D^{(k)}$$; this wrapper does not compute those matrices and is intended for membrane-like layers sharing a strain.

!!! info "deviation from theory"
    The wrapper adds layer stresses and tangents with unit weight, so the result is a membrane stress per unit thickness rather than the thickness-weighted resultant $$\mathbf N=\sum_k t_k\mathbf s^{(k)}$$ of a physical laminate.
    Any thickness or volume weighting must be absorbed into the layer parameters or the section assigned to the element.
    No $$A$$, $$B$$ or $$D$$ matrix is formed, so the wrapper cannot represent the bending stiffness of a stacked laminate.

The implementation copies each listed 2D material, evaluates all copies with the identical trial strain, and accumulates their stresses and tangents.
Densities are summed during initialization, and recorded histories are concatenated in tag order.

This wrapper is the two-dimensional analogue of [Parallel](Parallel.md) for 1D models and of [Stacked](Stacked.md) for 3D models.
Use [Rotation2D](Rotation2D.md) around a layer whose material axes are not aligned with the global axes, so that differently oriented plies can be combined.

## Syntax

```text title="Laminated"
material Laminated (1) (2...)
# (1) int, unique material tag
# (2...) int, material tags of 2D models need to be contained
```

The response of attached 2D material models will be output when recorded.
The output has a uniform size and data is arranged in the order as defined.

## Remarks

Every listed tag must refer to a registered 2D material, and the wrapper declares the plane type `S`, so pair it with plane-stress membrane elements.
A host based on [PlaneStress](PlaneStress.md) already reduces a 3D law to plane stress and can be listed directly.
The wrapper has no local iteration or equilibrium solve, because all layers share the same strain by construction; use [Sequential](Sequential.md) for the complementary iso-stress idea in one dimension.
Recorded quantities come from the individual layers in tag order, which makes it straightforward to inspect ply-by-ply damage or plasticity.

## References

- [ISBN 978-1-56032-712-7](https://search.worldcat.org/search?q=bn:9781560327127)
- [ISBN 978-0-8493-1592-3](https://search.worldcat.org/search?q=bn:9780849315923)
