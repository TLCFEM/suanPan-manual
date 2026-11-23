# Metal

To model metals, von Mises yielding criterion based models are often used.

## Background

Metal plasticity is usually described by a yield criterion, a flow rule and hardening rules for the size and the centre of the yield surface.
The von Mises criterion is appropriate for ductile metals because yielding is nearly insensitive to hydrostatic pressure.
Isotropic hardening changes the radius of the yield surface and captures an increase of the monotonic yield stress, but it cannot reproduce the Bauschinger effect.
Kinematic hardening translates the yield surface and is the standard way to model the reduced reverse yield stress after a load reversal.
Nonlinear kinematic hardening of Armstrong--Frederick type introduces a saturating backstress and is needed when many reverse cycles must be reproduced.
Rate-dependent metals use an overstress formulation in which the stress may exceed the yield surface by an amount that grows with the strain rate.
Phenomenological hysteresis models describe the observed loop directly without tracking a yield surface and are useful when only cyclic test data are available.

!!! info "deviation from theory"
    The 1D models represent a single axial stress component and a scalar yield condition, so they cannot enforce multiaxial von Mises equivalence or capture non-proportional loading.

## Choosing a Model

Use [`Bilinear1D`](../Material1D/vonMises/Bilinear1D.md) for a first estimate of monotonic or simple cyclic response and when only a yield stress and a hardening modulus are known.
Use [`ArmstrongFrederick1D`](../Material1D/vonMises/ArmstrongFrederick1D.md) when reverse yielding and the Bauschinger effect matter, and [`VAFCRP1D`](../Material1D/vonMises/VAFCRP1D.md) when the same response is also rate dependent.
Use [`SteelBRB`](../Material1D/Hysteresis/SteelBRB.md) for buckling-restrained braces, whose asymmetric tension and compression response is part of the design.
Use [`MPF`](../Material1D/Hysteresis/MPF.md) or [`RambergOsgood`](../Material1D/Hysteresis/RambergOsgood.md) when a smooth hysteresis loop must be fitted to experimental cycles.
Move to a 3D model when multiaxial stress states, shear or non-proportional loading are important, since a 1D model cannot represent those effects.

## 1D

The simplest von Mises bilinear hardening model with/without linear kinematic hardening rule (Prager's rule) can be used for simple analysis tasks.

The [`Bilinear1D`](../Material1D/vonMises/Bilinear1D.md) model supports both linear isotropic and kinematic hardening rules.
The [`BilinearMises1D`](../Material1D/vonMises/BilinearMises1D.md) model is an example of derived classes of the `Mises1D` model and only implements the isotropic hardening.

The [`ExpMises1D`](../Material1D/vonMises/ExpMises1D.md) model implements the exponential type isotropic hardening rule with a saturated stress; again there is no kinematic hardening defined.

For nonlinear kinematic hardening rule, often an Armstrong-Frederick type definition is used for modelling Bauschinger effect.
Two models are available: the [`ArmstrongFrederick1D`](../Material1D/vonMises/ArmstrongFrederick1D.md) model which is rate independent and the [`VAFCRP1D`](../Material1D/vonMises/VAFCRP1D.md) model which is rate dependent.
The corresponding viscosity is defined in a Peric style.
If experiment data is available, those two models will give better simulation results for a wide range of metals.

Another model that can be used is the asymmetric [`SteelBRB`](../Material1D/Hysteresis/SteelBRB.md) model which is developed to simulate BRBs.
It has a rheology model which reveals some insights of response.

For general phenomenological hysteresis models, the [`MPF`](../Material1D/Hysteresis/MPF.md) model (Menegotto-Pinto-Filippou model) and the [`RambergOsgood`](../Material1D/Hysteresis/RambergOsgood.md) model are widely used.
In terms of the determination of the model parameters, readers are referred to the related literature.

The Bouc-Wen family ([`BoucWen`](../Material1D/Hysteresis/BoucWen.md) and [`BWBN`](../Material1D/Hysteresis/BWBN.md)) can be used.

## 3D

Apart from the [`MPF`](../Material1D/Hysteresis/MPF.md) model and the [`RambergOsgood`](../Material1D/Hysteresis/RambergOsgood.md) model, other models have the corresponding 3D versions.

## Remarks

The 1D models are intended for truss, beam and fiber-section applications where a single axial stress component is sufficient.
The 3D counterparts include [`ArmstrongFrederick`](../Material3D/vonMises/ArmstrongFrederick.md) and [`VAFCRP`](../Material3D/vonMises/VAFCRP.md), while [`BilinearJ2`](../Material3D/vonMises/BilinearJ2.md) and [`ExpJ2`](../Material3D/vonMises/ExpJ2.md) correspond to the simpler 1D hardening laws.
Hardening parameters should be calibrated against the specific heat treatment and strain range of interest, since the same steel can behave quite differently after cyclic softening.

## References

1. Chaboche, J.-L. (1989), "Constitutive Equations for Cyclic Plasticity and Cyclic Viscoplasticity," International Journal of Plasticity, 5(3), 247--302, [doi:10.1016/0749-6419(89)90015-6](https://doi.org/10.1016/0749-6419(89)90015-6).
