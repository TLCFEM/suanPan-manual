# Sequential

Container of Material Models In Sequence

Combines multiple 1D material models into a single one.

## Theory

A series rheological arrangement places several constitutive elements end to end along the same load path.
Equilibrium of the force transmitted through the chain means every constituent carries the same stress, $\sigma^{(k)}=\sigma$, while compatibility makes the total elongation the sum of the individual ones,

$$
\varepsilon=\sum_{k=1}^{n}\varepsilon^{(k)}(\sigma),
\qquad
S(\sigma)=\dfrac{\partial\varepsilon}{\partial\sigma}=\sum_{k=1}^{n}S^{(k)}(\sigma),
\qquad
D=\left(\sum_{k=1}^{n}\dfrac{1}{D^{(k)}}\right)^{-1},
$$

where $S^{(k)}=1/D^{(k)}$ is the tangent compliance of constituent $k$.
With volume fractions the same statement becomes $S=\sum_k f_k S^{(k)}$, which is the iso-stress or Reuss assumption and gives a lower bound on the effective stiffness.
For two linear springs this reproduces the harmonic average $E_{\mathrm{eq}}=E_1E_2/(E_1+E_2)$ when no fractions are supplied.

!!! info "deviation from theory"
    The wrapper adds the constituent compliances with unit weight, so the Reuss average is obtained only when all volume fractions $f_k$ are equal.
    No area or volume fraction is read from the input, so any weighting must already be embedded in the constituent parameters.

For a prescribed total strain the local strains of the constituents are not known in advance, so the implementation solves a small nonlinear system at each trial state.
The unknowns are the strains $\varepsilon^{(k)}$ of all $n$ constituents, the first residual enforces $\varepsilon-\sum_k\varepsilon^{(k)}=0$, and the remaining $n-1$ residuals enforce equality of neighbouring stresses $\sigma^{(k)}-\sigma^{(k+1)}=0$.
The Jacobian is assembled from the host tangent stiffnesses with signs consistent with these residuals, and the Newton correction is added to each local strain until the correction or the residual falls below the tolerance.
The maximum number of local iterations is fixed at 20 in the class, and failure is reported as an error.
The wrapper stiffness is the harmonic sum $1/\sum_k 1/D^{(k)}$, and the reported stress is that of the first constituent, which equals the common series stress at convergence.

This wrapper is the 1D series counterpart of [Parallel](Parallel.md), which imposes equal strain instead.
It is useful for building Maxwell-type or generalised rheological arrangements from rate-independent 1D laws, although the viscosity-free restriction below still applies.
Histories are recorded in tag order, as in [Laminated](Laminated.md) and [Stacked](Stacked.md).
No volume fractions are applied by the wrapper, so any weighting must already be embedded in the constituent parameters.

## Syntax

```text title="Sequential"
material Sequential (1) (2...)
# (1) int, unique material tag
# (2...) int, material tags of 1D models need to be contained
```

## Caveat

Please do not include any viscosity-related models into the wrapper.
This container is only designed for rate-independent hysteretic models.
The response of attached 1D material models will be output when recorded.
The output has a uniform size and data is arranged in the order as defined.

## Remarks

At least two constituent tags are required, and the parser rejects a single tag.
Every tag must refer to a registered 1D material with a nonzero initial stiffness, since the harmonic average divides by each tangent.
The local Newton loop uses the current tangent of every constituent, so strongly nonlinear hosts benefits from smaller global increments.
All constituents share a single stress, so a constituent that softens cannot shed load to the others in the way that a parallel arrangement can; this is the characteristic limitation of the series idealisation.
Use [Parallel](Parallel.md) for iso-strain combinations and [Prestrain](Prestrain.md) when an imposed initial strain rather than a series stress is required.

## References

- [10.1002/zamm.19290090104](https://doi.org/10.1002/zamm.19290090104)
- [10.1016/0022-5096(63)90036-X](https://doi.org/10.1016/0022-5096(63)90036-X)
- [ISBN 978-0-444-60192-6](https://search.worldcat.org/search?q=bn:9780444601926)
