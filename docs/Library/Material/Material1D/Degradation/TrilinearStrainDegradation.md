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

## Remarks

The general formulation and the corresponding stiffness expression are described in [`Degradation`](Degradation.md).
All three strain and factor arguments are converted to absolute values, so their signs do not matter.
As with other degradation wrappers, the formulation is only valid when degradation does not depend on plasticity history.

## Example

```text
material MPF 1 1000 5 .1
material TrilinearStrainDegradation 2 1 1E-2 6E-2 .1
```
