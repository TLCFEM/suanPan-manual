# IsotropicDamage

Independent Isotropic Damage Model

The `IsotropicDamage` model interacts with an associated 3D material model and computes the damage factor based on total
strain or other related quantities.

## Interface

The `update_trial_status(const vec&)` is implemented so that `trial_stress` and `trial_stiffness` store the
corresponding response of the associated material model and call the `update_damage()` method.

The `update_damage()` method shall be implemented in all derived classes.

Alternatively, material state update method `update_trial_status(const vec&)` can be thoroughly overridden by the
derived classes.
