# AbaqusCDP

The Abaqus CDP Model

This model offers a flavor of the CDP model that resembles the one implemented in Abaqus.

In total, four tables are required.

## Background

This model follows the Abaqus implementation of the concrete damaged plasticity model, which itself is based on Lubliner et al. (1989) with the modifications of Lee and Fenves (1998).
The plasticity, damage and return-mapping algorithms are the same as those of [`CDP`](CDP.md) and [`TableCDP`](TableCDP.md); only the shape of the yield surface and the source of the hardening curves differ.

### Yield surface and the $K_c$ parameter

In effective-stress space the yield function is

$$
F=\alpha I_1+\sqrt{3J_2}-\left(1-\alpha\right)\bar\sigma_c+\beta\left\langle\bar\sigma_{\max}\right\rangle-\zeta\left\langle-\bar\sigma_{\max}\right\rangle,
$$

with the coefficients

$$
\alpha=\dfrac{\sigma_{b0}/\sigma_{c0}-1}{2\sigma_{b0}/\sigma_{c0}-1},\qquad
\beta=(1-\alpha)\dfrac{\bar\sigma_c}{\bar\sigma_t}-(1+\alpha),\qquad
\zeta=\dfrac{3(1-K_c)}{2K_c-1}.
$$

Here $\sigma_{b0}/\sigma_{c0}$ is argument (9), the ratio of the equibiaxial to uniaxial compressive yield stress, and $K_c$ is argument (10).
The coefficient $\alpha$ is fixed by the biaxial compression test, because on that stress path the yield condition reduces to the Drucker--Prager criterion.
The coefficient $\zeta$ only enters for triaxial compression states where the algebraically largest principal effective stress is negative.
It is obtained by matching the deviatoric stress on the tensile meridian, where $\bar\sigma_1=\bar\sigma_2<\bar\sigma_3$, to that on the compressive meridian, where $\bar\sigma_1<\bar\sigma_2=\bar\sigma_3$.
With $K_c=1$ the deviatoric section is circular and $\zeta=0$, which is the value implicitly used by [`CDP`](CDP.md), [`TableCDP`](TableCDP.md) and [`CustomCDP`](CustomCDP.md).
With the default $K_c=2/3$ the section is triangular near the compressive corner, giving $\zeta=3(1-2/3)/(4/3-1)=3$.

### Flow potential

Abaqus uses the Drucker--Prager hyperbolic flow potential

$$
G=\sqrt{\left(e\bar\sigma_t\right)^2+\left(\alpha_p q\right)^2}-\bar p\tan\psi ,
$$

where $\psi$ is the dilation angle, $e$ is the eccentricity, $\bar p=-I_1/3$ is the compression-positive hydrostatic pressure and $q=\sqrt{3J_2}$.
The eccentricity smooths the apex, which otherwise has a non-unique flow direction.
The implementation instead uses the linear potential $G=\left\|\bar{\mathbf s}\right\|+\alpha_p I_1$ described on the [`CDP`](CDP.md) page, so the plastic potential has a corner at the hydrostatic axis but no additional parameter.
The relation between the input dilatancy parameter and the dilation angle is $\alpha_p=\tan\psi$, so the default $\alpha_p=0.6$ corresponds roughly to $\psi=31\text{\textdegree}$.

!!! warning "implementation limitation"
    The eccentricity $e$ of the hyperbolic potential is not an input and is not implemented.
    The plastic potential is therefore a linear cone with a corner at the hydrostatic axis rather than the smooth Abaqus surface.
    The dilation angle is interpreted directly through the slope $\alpha_p$, so its value is not identical to the angle in the hyperbolic Abaqus potential at low confining pressure.

### Tables and damage

The four tables are the tensile backbone, compressive backbone, tensile damage and compressive damage, all expressed against plastic strain rather than against the internal variable $\kappa$.
In the parser, the area under each backbone is integrated by the trapezoidal rule to recover the normalised energies $g_t$ and $g_c$, and the plastic-strain axis is mapped to $\kappa$ by cumulative energy.
The last table point is connected to complete damage at $\kappa=1$ by an exponential tail, so the tables should extend well into the softening branch.
Damage degrades the stiffness through $\mathbf\sigma=[1-s(r)d_t][1-d_c]\bar{\mathbf\sigma}$, with the stress-state factor $s(r)=w+r(1-w)$ and a single recovery parameter $w$ given by argument (11).
The default $w=0$ means no recovery of tensile stiffness when cracks close, matching the Abaqus default; other CDP variants default to $w=0.5$.
Viscous regularisation, available in Abaqus/Standard through the viscosity parameter, is not implemented.

!!! warning "implementation limitation"
    Abaqus accepts separate tension and compression recovery factors and several damage-input formats, whereas this model exposes only one factor $w$ and only plastic-strain-based tables.
    Compression damage is never recovered, and no viscous regularisation is available to stabilise localisation in softening analyses.

## Syntax

```text title="AbaqusCDP"
material AbaqusCDP (1) (2) (3) (4) (5) (6) (7) [8] [9] [10] [11] [12]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) string, file name of tension backbone table
# (5) string, file name of compression backbone table
# (6) string, file name of tension damage table
# (7) string, file name of compression damage table
# [8] double, dilatancy parameter, default: 0.6
# [9] double, biaxial compression strength ratio, default: 1.16
# [10] double, ratio between tensile and compressive meridian stresses, default: 0.667
# [11] double, stiffness recovery ratio, default: 0
# [12] double, density, default: 2400e-12
```

## Remarks

The definitions and usages of tables are identical to that of the [`TableCDP`](TableCDP.md) model.
Compared to the [`TableCDP`](TableCDP.md) model, the following differences shall be noted.

1. An additional parameter `[10]` is required, this is the ratio between tensile and compressive meridian stresses, in Abaqus' notation, it is $$K$$ or $$K_c$$.
   According to [10.1016/0020-7683(89)90050-4](https://doi.org/10.1016/0020-7683(89)90050-4), typical values range from $$0.6$$ to $$0.8$$ and the default value is $$2/3$$.
   This only affects the triaxial compression cases.
2. The stiffness recovery ratio `[11]` defaults to $$0$$ to match the same default behaviour in Abaqus.
3. The dilatancy parameter `[8]` defaults to $$0.6$$, which corresponds to about $$31\text{\degree}$$ dilatancy angle.
   Neither this value nor the original value $$0.2$$ would be universal; one may still need to choose a proper value to meet the specific shear demand.

Compared to the original Abaqus' CDP implementation, the following features are **not** implemented.

1. Abaqus supports input tables of various formats, this `AbaqusCDP` model only accepts tables using plastic strain as the x-axis.
2. Abaqus supports both tension and compression damage recovery, this `AbaqusCDP` model only accounts for tension stiffness recovery (via parameter `[11]`).
3. Abaqus has an eccentricity parameter in the plastic flow potential, this is not considered in this `AbaqusCDP` model.
   This parameter only affects a small region around the apex and is introduced to ensure the surface is smooth to remove the singularity.
   The gain is not significant while accounting for this parameter would significantly complicate the implementation.

### Implementation and calibration notes

- The parser accepts $E=3\times10^4$, $\nu=0.2$, $\alpha_p=0.6$, $\sigma_{b0}/\sigma_{c0}=1.16$, $K_c=2/3$, $w=0$ and density $2400\times10^{-12}$ as defaults.
- All table ordinates are converted to absolute values by the parser; the first abscissa must be exactly zero and the backbone must end with a decaying tail.
- The table ordinates are integrated and rescaled internally, so the softening energy is determined by the tabulated curve rather than by a separate fracture-energy argument.
- The parameter $K_c$ must be greater than $0.5$ for the expression $3(1-K_c)/(2K_c-1)$ to remain finite and positive.
- Concrete calibrations commonly use $\sigma_{b0}/\sigma_{c0}$ between $1.10$ and $1.16$, giving $\alpha$ of roughly $0.08$ to $0.12$, and $K_c$ close to $2/3$.
- Since the potential is linear rather than hyperbolic, users should avoid extrapolating the model to stress states very close to pure hydrostatic compression, where the apex corner lies.
- For a single recovery factor that is active by default, or for the $K_c=1$ surface, use [`CDP`](CDP.md) or [`TableCDP`](TableCDP.md) instead.

## References

1. [10.1016/0020-7683(89)90050-4](https://doi.org/10.1016/0020-7683(89)90050-4)
2. [10.1061/(ASCE)0733-9399(1998)124:8(892)](https://doi.org/10.1061/(ASCE)0733-9399(1998)124:8(892))
3. Mechanics of thermo-elastic-plastic materials with a thermoelastic-plastic change in volume
