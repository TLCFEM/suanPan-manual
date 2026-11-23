# TrilinearStrainDegradation

Strain-based degradation wrapper with a three-segment, symmetric degradation law.

## Syntax

```text title="TrilinearStrainDegradation"
material TrilinearStrainDegradation (1) (2) (3) (4) (5)
# (1) int, unique material tag
# (2) int, host material tag
# (3) double, degradation initiation strain
# (4) double, degradation final strain
# (5) double, degradation final factor
```

## Background

This wrapper scales the stress of a host 1D material by a degradation factor $$D$$ that depends only on the strain history.
The factor is symmetric in tension and compression and evolves in three stages.
It equals 1 below the initiation strain, decreases linearly to the final factor at the final strain, and stays there for larger strains.
Writing $$\varepsilon_s=(3)$$, $$\varepsilon_e=(4)$$ and $$D_e=(5)$$,

$$
D(|\varepsilon|)=\begin{cases}
1, & |\varepsilon|\le\varepsilon_s,\\[2mm]
1+\dfrac{1-D_e}{\varepsilon_s-\varepsilon_e}\left(|\varepsilon|-\varepsilon_s\right), & \varepsilon_s<|\varepsilon|\le\varepsilon_e,\\[2mm]
D_e, & |\varepsilon|>\varepsilon_e.
\end{cases}
$$

The intermediate slope is $$m=(1-D_e)/(\varepsilon_s-\varepsilon_e)$$, which is negative for $$D_e<1$$ and $$\varepsilon_e>\varepsilon_s$$.
For negative strains the derivative is mirrored so that it remains consistent with the negative strain direction.

!!! warning "implementation limitation"
    The tension or compression envelope is chosen by the sign of the intact host stress, not by the sign of the strain.
    The extreme strain is updated only when the strain moves further in the direction selected by that stress sign.
    A host with a stress offset can therefore update the wrong envelope for a given strain.

The wrapper uses the maximum tensile strain and the minimum compressive strain as envelope variables, so degradation is irreversible.
On a new extreme the tangent stiffness is $$K=D\bar K+\bar\sigma\,\mathrm{d}D/\mathrm{d}\varepsilon$$, and on unloading it reduces to $$K=D\bar K$$.

## Remarks

The general formulation and the corresponding stiffness expression are described in [`Degradation`](Degradation.md).
All three strain and factor arguments are converted to absolute values, so their signs do not matter.
As with other degradation wrappers, the formulation is only valid when degradation does not depend on plasticity history.
The strain arguments are magnitudes internally, and the condition $$\varepsilon_s<\varepsilon_e$$ should be satisfied for a monotonic law.
A final factor of zero removes the stress entirely and produces a zero tangent stiffness, which can cause convergence problems.
Because the envelope is based on extreme strains, the factor cannot recover during unloading or reloading.
See [`Dhakal`](Dhakal.md) for a compression-only law and [`CustomStrainDegradation`](CustomStrainDegradation.md) for arbitrary evolution rules.

## Example

```text
material MPF 1 1000 5 .1
material TrilinearStrainDegradation 2 1 1E-2 6E-2 .1
```
