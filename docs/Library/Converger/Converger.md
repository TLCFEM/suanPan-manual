# Converger

Though the term `converger` is not a valid word, it is used to denote the object that provide information about if the
system converges.

## Syntax

All convergers, except for [`Logic`](Other/Logic.md) and [`FixedNumber`](Other/FixedNumber.md), share the same definition.

```
converger (1) (2) (3) (4) [5]
# (1) string, converger type
# (2) int, unique tag
# (3) double, tolerance
# (4) int, maximum iteration
# [5] bool string, print switch, default: false
```

## Available Convergers

Currently, following convergers are available.

* [AbsDisp](Absolute/AbsDisp.md)
* [AbsError](Absolute/AbsError.md)
* [AbsIncreDisp](Absolute/AbsIncreDisp.md)
* [AbsIncreEnergy](Absolute/AbsIncreEnergy.md)
* [AbsResidual](Absolute/AbsResidual.md)
* [RelDisp](Relative/RelDisp.md)
* [RelError](Relative/RelError.md)
* [RelIncreDisp](Relative/RelIncreDisp.md)
* [RelIncreEnergy](Relative/RelIncreEnergy.md)
* [RelResidual](Relative/RelResidual.md)
* [FixedNumber](Other/FixedNumber.md)
* [Logic](Other/Logic.md)
