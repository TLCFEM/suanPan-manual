# Concrete22

Fixed Crack Concrete Model

## Background

The fixed crack model records the orientation of the first crack and keeps it fixed for the rest of the analysis, so subsequent loading can generate shear stress on the crack plane.
This is the main difference from the rotating crack model of [`Concrete21`](Concrete21.md), where the axes follow the principal strain directions and the shear stress on the crack face is always zero.
In the smeared formulation the crack is distributed over the element, and shear transfer across the rough crack surface is represented by a constant shear-retention factor.
The two normal directions are again driven by independent uniaxial [`ConcreteTsai`](../Material1D/Concrete/ConcreteTsai.md) laws, with no Poisson coupling between them.

## Syntax

```text title="Concrete22"
material Concrete22 (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) (11) [12]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, compression strength, should be negative but sign insensitive
# (4) double, tension strength, should be positive but sign insensitive
# (5) double, NC
# (6) double, NT
# (7) double, middle point
# (8) double, strain at compression strength
# (9) double, strain at tension strength
# (10) double, shear stress
# (11) double, shear retention factor
# [12] double, density, default: 0.0
```

## Theory

Let $\theta$ be the crack angle stored in `trial_history(0)` and let $\mathbf T(\theta)$ be the corresponding transformation matrix.
The trial strain is projected into these axes, $\hat{\boldsymbol\varepsilon}=\mathbf T\boldsymbol\varepsilon$, and the two normal components drive two independent uniaxial concrete models.
The source also records the largest tensile principal strain $\varepsilon_{t,\max}$ and the smallest compressive principal strain $\varepsilon_{c,\max}$ in `trial_history(1)` and `trial_history(2)`.
The angle is updated from the current strain only while $\varepsilon_{t,\max}<\varepsilon_{cr}$ and $\varepsilon_{c,\max}>\varepsilon_{pk}$, where $\varepsilon_{cr}$ and $\varepsilon_{pk}$ are the tensile cracking and compressive peak strains.
Once either cracking or crushing is detected the angle is frozen, which is the precise sense in which this model has fixed cracks.

!!! info "deviation from theory"
    A classical fixed crack model fixes the orientation at the first cracking event.
    This implementation keeps the axes rotating until the recorded tensile strain reaches the cracking strain or the compressive strain reaches the peak strain, and only then locks them.

The normal stress components are $\hat\sigma_i=f(\hat\varepsilon_i)$ with $f$ the selected uniaxial backbone.
The shear response is initially elastic with modulus $G=E/2$ until the shear strain reaches $\gamma_s=\tau_s/G$, where $\tau_s$ is the input shear stress.
Beyond that threshold the shear modulus is reduced to $\beta_s G$ and the shear stress continues as
$$
\hat\tau=\operatorname{sign}(\hat\gamma)\left[\tau_s+\left(|\hat\gamma|-\gamma_s\right)\beta_s G\right],
$$
with $\beta_s$ the shear retention factor.

!!! warning "implementation limitation"
    The shear retention factor is constant and the model has no crack-slip, aggregate-interlock or shear-dilatancy law.
    After the orientation is locked, continuing changes in the principal strain direction produce shear stress even though no new crack direction is created.

The stress and stiffness are finally rotated back to global axes by $\boldsymbol\sigma=\mathbf T^{\mathrm T}\hat{\boldsymbol\sigma}$ and $\mathbf K=\mathbf T^{\mathrm T}\hat{\mathbf K}\mathbf T$.

## Remarks

* `(10)` is the shear stress $\tau_s$ at which shear degradation starts, and `(11)` is the shear retention factor $\beta_s$ that multiplies the elastic shear modulus after cracking.
* A retention factor of zero removes all shear transfer across the crack, while a value of one gives no shear degradation at all.
* The initial shear modulus is $E/2$, so the transition strain is $\gamma_s=2\tau_s/E$ and no Poisson's ratio is needed.
* The crack angle is not frozen from the very first step; the axes rotate with the principal strains until the recorded tensile or compressive strain exceeds its cracking or peak value.
* The two independent uniaxial backbones imply no biaxial strength interaction and no Poisson effect, so biaxial compression confinement is not represented.
* The model is tagged `PlaneType::N`, so only `HIST` and `YF` are available as standard output from [Material2D](Material2D.md).
* Combine it with [`Rebar2D`](Rebar2D.md) through the [`Laminated`](../Wrapper/Laminated.md) wrapper to model a reinforced concrete membrane with shear transfer across fixed cracks.
* Strain softening is not regularised by fracture energy, so computed crack widths and post-peak response depend on mesh size.
* For rotating cracks without shear retention use [`Concrete21`](Concrete21.md), and for smeared damage coupled to a 3D law use [`IsotropicDamage`](../Material3D/Damage/IsotropicDamage.md).

## References

1. Crisfield, M. A. and Wills, J. (1989), "Analysis of R/C Panels Using Different Concrete Models", Journal of Engineering Mechanics, 115(3), 578--597, [10.1061/(ASCE)0733-9399(1989)115:3(578)](https://doi.org/10.1061/(ASCE)0733-9399(1989)115:3(578)).
2. Chen, W. F. and Han, D. J. (2007), "Plasticity for Structural Engineers", J. Ross Publishing, ISBN 978-1-932159-75-2, Chapter 7.
