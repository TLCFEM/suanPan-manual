# Metal

To model metals, von Mises yielding criterion based models are often used.

## 1D

The simplest von Mises bilinear hardening model with/without linear kinematic hardening rule (Prager's rule) can be used
for simple analysis tasks.

The [`Bilinear1D`](../Material1D/vonMises/Bilinear1D.md) model supports both linear isotropic and kinematic hardening
rules. The [`BilinearMises1D`](../Material1D/vonMises/BilinearMises1D.md) model is an example of derived classes of
the `Mises1D` model and only implements the isotropic hardening.

The [`ExpMises1D`](../Material1D/vonMises/ExpMises1D.md) model implements the exponential type isotropic hardening rule
with a saturated stress, again there is no kinematic hardening defined.

For nonlinear kinematic hardening rule, often an Armstrong-Frederick type definition is used for modelling Bauschinger
effect. Two models are available, they are the [`ArmstrongFredick1D`](../Material1D/vonMises/ArmstrongFrederick1D.md)
model which is rate dependent and the [`VAFCRP1D`](../Material1D/vonMises/VAFCRP1D.md) model which is rate dependent,
the corresponding viscosity is defined in a Peric style. If experiment data is available, those two models will give
better simulation results for a wide range of metals.

Another model that can be used is the asymmetric [`SteelBRB`](../Material1D/Hysteresis/SteelBRB.md) model which is
developed to simulate BRBs. It has a rheology model which reveals some insights of response.

For general phenomenological hysteresis models, the [`MPF`](../Material1D/Hysteresis/MPF.md) model (
Menegotto-Pinto-Filippou model) and the [`RambergOsgood`](../Material1D/Hysteresis/RambergOsgood.md) model are widely
used. In terms of the determination of the model parameters, readers are referred to the related literature.

The Bouc-Wen family ([`BoucWen`](../Material1D/Hysteresis/BoucWen.md) and [`BWBN`](../Material1D/Hysteresis/BWBN.md))
can be used.

## 3D

Apart from the [`MPF`](../Material1D/Hysteresis/MPF.md) model and
the [`RambergOsgood`](../Material1D/Hysteresis/RambergOsgood.md) model, other models have the corresponding 3D versions.
