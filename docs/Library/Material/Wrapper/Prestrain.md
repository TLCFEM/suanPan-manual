# Prestrain

Prestrain Wrapper

Wraps a uniaxial host material model so that a prestrain can be applied.
This may be useful for modelling prestressed reinforced concrete or similar multiphase materials.

## Syntax

```
material Prestrain (1) (2) (3) (4)
# (1) int, unique material tag
# (2) int, underlying material tag
# (3) int, amplitude tag, set to 0 to use a ramp function
# (4) double, maginutde
```

## Remarks

It is necessary to attach an amplitude.
The amplitude is in charge of applying the designated prestrain (of the specified magnitude) to the underlying material in a controlled manner.

If only a prestress is available, one can always develop a uniaxial test model to compute the prestrain from the prestress.
Thus, we do not provide a `Prestress` counterpart.

## Example

```text
node 1 0 0
node 2 1 0

material Elastic1D 1 100
material Prestrain 2 1 0 1E-2

element T2D2 1 1 2 1 10
element T2D2 2 1 2 2 10

fix2 1 1 1
fix2 2 2 1 2

step static 1
set ini_step_size .1

converger AbsIncreDisp 1 1E-4 10 1

analyze

peek node 2

exit
```

The above example is a simple demonstration.
The prestrain $$\num{1E-2}$$ will be gradually (linearly increasing from zero to the specific magnitude) applied to the second element.
The system balances itself without any external load.

The final displacement of node 2 should be $$\num{5E-3}$$ since both elements share the same section properties.
