# Parallel

Container of Material Models In Parallel

Combines multiple 1D material models into a single one.

## Theory

A parallel rheological arrangement connects several constitutive elements between the same pair of nodes, so every element undergoes the same deformation.
Compatibility therefore gives $\varepsilon^{(k)}=\varepsilon$ for every constituent $k$, while equilibrium of the nodal forces requires the stresses to add,

$$
\sigma(\varepsilon)=\sum_{k=1}^{n}\sigma^{(k)}(\varepsilon),
\qquad
D(\varepsilon)=\dfrac{\partial\sigma}{\partial\varepsilon}=\sum_{k=1}^{n}D^{(k)}(\varepsilon),
$$

where $D^{(k)}=\partial\sigma^{(k)}/\partial\varepsilon^{(k)}$ is the tangent of constituent $k$.
For a unit-volume representative element with volume fractions $f_k$ the same relations read $\sigma=\sum_k f_k\sigma^{(k)}$ and $D=\sum_k f_k D^{(k)}$, so the parallel arrangement is the iso-strain or Voigt assumption and gives an upper bound on the effective stiffness.
For linear springs this reduces to $E_{\mathrm{eq}}=\sum_k f_k E_k$, and the free energies of the constituents add.

The implementation stores a copy of every listed 1D material and drives all copies with the identical trial strain.
It accumulates the trial stress, the trial tangent and, when present, the trial damping from every constituent.
The density and the initial tangent are summed in the same way during initialization.
Recorded histories are concatenated in the order in which the tags were supplied, so a recorder sees one column block per constituent.

This wrapper is the 1D counterpart of [Laminated](Laminated.md) for 2D materials and [Stacked](Stacked.md) for 3D materials, all of which impose an iso-strain condition.
The complementary iso-stress arrangement is [Sequential](Sequential.md).
The wrapper carries no volume or area fraction of its own, so any weighting must be absorbed into the parameters of the constituent materials or into the section assigned to the element.

## Syntax

```text title="Parallel"
material Parallel (1) (2...)
# (1) int, unique material tag
# (2...) int, material tags of 1D models need to be contained
```

## Caveat

Please do not include any viscosity-related models into the wrapper.
This container is only designed for rate-independent hysteretic models.
The response of attached 1D material models will be output when recorded.
The output has a uniform size and data is arranged in the order as defined.

## Remarks

All listed tags must refer to initialized 1D materials; the wrapper reports an error otherwise.
Because every constituent sees the full strain, a soft constituent cannot unload simply because a stiff one carries more force; that behaviour belongs to the series arrangement in [Sequential](Sequential.md).
The current source also provides a strain-rate overload that forwards the rate to each host and sums the damping matrices, so rate-dependent hosts are handled consistently when they expose a damping tangent.
The `Caveat` above remains the conservative guidance for rate-independent hysteretic hosts, whose damping matrices are normally empty.

!!! info "caveat versus implemented behaviour"
    The original `Caveat` states that viscosity-related models must not be placed in this wrapper.
    Rate-dependent hosts are supported when they expose a damping tangent.
    Treat the caveat as conservative guidance for hysteretic rate-independent models rather than as a hard restriction of the code.

!!! note "developer note"
    The current `Parallel` implementation forwards the strain rate to every host and sums the damping matrices.

The wrapper is natural for truss elements such as [T2D2](../../Element/Truss/T2D2.md), where the section area supplies the missing force weighting.

## References

- Theoretische Studien über die Elastizitätsverhältnisse der Kristalle
- [10.1016/0022-5096(63)90036-X](https://doi.org/10.1016/0022-5096(63)90036-X)
- [ISBN 978-1-56032-712-7](https://search.worldcat.org/search?q=bn:9781560327127)
