# Degradation

The uniaxial degradation model can be implemented separately from the intact material model if the degradation model only depends on the input strain history or the output stress and stiffness.

## Background

The wrappers in this family implement scalar isotropic damage for one-dimensional materials.
A damage variable $$d\in[0,1]$$ reduces the effective stress of an intact host material through $$\sigma=(1-d)\bar\sigma=D\bar\sigma$$.
The intact or effective stress $$\bar\sigma$$ is computed by the host model from the same strain, so the wrapper adds only a multiplicative factor.
The factor is irreversible because it is driven by the extreme value seen in the history, which is stored in two history variables.
Two independent factors are kept for tension and compression and are reported as `DT` and `DC`.

!!! info "deviation from theory"
    Classical scalar isotropic damage uses a single damage variable for both loading directions.
    The wrappers here use two independent envelope variables and switch between them according to the sign of the undamaged stress.
    The result is closer to a unilateral damage formulation than to a single isotropic scalar.

The secant stiffness of the damaged response is $$D\bar K$$, whereas the tangent stiffness contains an additional term whenever the damage is evolving.
This distinction matters in a Newton--Raphson solution because only the tangent provides quadratic convergence.
The wrapper evaluates the host model independently and does not modify the host history, so the intact and degraded states are advanced in parallel.
The effective stress concept originates in the creep damage theory of Kachanov, in which the stress acting on the intact area is $\bar\sigma=\sigma/D$.
A scalar factor implies isotropic damage, so directional effects such as crack closure must be handled by using separate tension and compression envelopes.

## Stress

The general expression of a degradation model can be expressed as

$$
\sigma=D\bar{\sigma}=(1-d)\bar{\sigma},
$$

where $$D$$ and $$d$$ are degradation factors, $$\bar\sigma$$ is the stress of the intact material model.
It is often called the effective stress.
Whether to use $$D$$ or $$(1-d)$$ relies on the specific definition of degradation.
Here we focus on the first expression.
The factor $$D=1$$ denotes an intact material and $$D=0$$ denotes a complete loss of stress.

## Stiffness

The stiffness can be expressed by applying the chain rule.

### Strain Dependent Degradation

Assuming the degradation factor depends on the strain history, namely, $$D=D(\varepsilon_{max})$$.
Here $$\varepsilon_{max}$$ is the maximum strain of the whole loading history.

Where damage evolution is activated, the stiffness can be expressed as

$$
K=\dfrac{\mathrm{d}\sigma}{\mathrm{d}\varepsilon}=\dfrac{\partial{}D}{\partial\varepsilon}\bar\sigma+D\dfrac{\partial\bar\sigma}{\partial\varepsilon}=\dfrac{\partial{}D}{\partial\varepsilon}\bar\sigma+D\bar{K}
$$

where $$\bar{K}$$ is the effective stiffness of the intact material model.
In the implementation the derivative term is omitted when no new extreme is reached, so unloading and reloading are governed by the secant factor alone.

### Stress Dependent Degradation

Assuming the degradation factor depends on the stress history, namely, $$D=D(\bar{\sigma}_{max})$$.
Here $$\bar{\sigma}_{max}$$ is the maximum effective stress of the whole loading history.

Where damage evolution is activated, the stiffness can be expressed as

$$
K
=\dfrac{\mathrm{d}\sigma}{\mathrm{d}\varepsilon}
=\dfrac{\partial{}D}{\partial\bar{\sigma}}\dfrac{\partial\bar\sigma}{\partial\varepsilon}\bar{\sigma}+D\dfrac{\partial\bar\sigma}{\partial\varepsilon}
=\left(\dfrac{\partial{}D}{\partial\bar{\sigma}}\bar{\sigma}+D\right)\bar{K}
$$

where $$\bar{K}$$ is the effective stiffness of the intact material model.

## Computation Procedure

In general, the computation procedure of a degradation model can be listed as follows.

1. input trial strain and trial strain rate if required
2. call the associated intact material model to compute the intact stress and stiffness
3. calculate $$D$$ and $$\dfrac{\partial{}D}{\partial{}\varepsilon}$$ accordingly and update history variables if any
4. update trial stress and trial stiffness

## Caveats

Such a formulation is only valid for the damage models that do not depend on plasticity history.

!!! warning "implementation limitation"
    The wrapper calls the host model with the strain and then multiplies its stress and stiffness.
    It never modifies the host history variables, so damage cannot alter yielding, plastic flow or the size of the yield surface.
    Host models that require such coupling should use an integrated plastic-damage material instead of this wrapper.

## Recording

This model (and its derivatives) supports the following additional history variables to be recorded.

| variable label | physical meaning   |
|----------------|--------------------|
| DT             | tensile damage     |
| DC             | compressive damage |

The recorded quantities are the current degradation factors, not the complementary damage indices.

## Remarks

The host material must be defined before the wrapper and is referenced by its tag in all derived models.
The wrapper copies the density from the host material, so no density argument appears in wrapper commands.
The tension and compression branches are selected by the sign of the intact stress, and their envelope variables are the extreme strain or the extreme intact stress.
The initial stiffness is scaled by the degradation factor evaluated at zero, which is unity for all built-in wrappers.
The formulation is intended for host models whose degradation does not depend on plasticity history, such as [`Elastic1D`](../Elastic/Elastic1D.md) or [`MPF`](../Hysteresis/MPF.md).
The custom variants [`CustomStrainDegradation`](CustomStrainDegradation.md) and [`CustomStressDegradation`](CustomStressDegradation.md) allow arbitrary evolution laws through expressions.
The built-in [`TrilinearStrainDegradation`](TrilinearStrainDegradation.md) and [`Dhakal`](Dhakal.md) wrappers provide piecewise laws without expressions.

## References

1. Kachanov, L. M. (1958). Time of the rupture process under creep conditions. *Izvestia Akademii Nauk USSR, Otdelenie Tekhnicheskich Nauk*, 8, 26--31.
2. Lemaitre, J. and Chaboche, J.-L. (1990). *Mechanics of Solid Materials*. Cambridge University Press.
3. Mazars, J. and Pijaudier-Cabot, G. (1989). Continuum damage theory: application to concrete. *Journal of Engineering Mechanics*, 115(2), 345--365. [doi:10.1061/(ASCE)0733-9399(1989)115:2(345)](https://doi.org/10.1061/(ASCE)0733-9399(1989)115:2(345)).
