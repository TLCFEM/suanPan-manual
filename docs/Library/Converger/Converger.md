# Converger

Though the term `converger` is not a valid word, it is used to denote the object that provides information about whether the
system converges.

## Syntax

All convergers, except for [`Logic`](Other/Logic.md) and [`FixedNumber`](Other/FixedNumber.md), share the same definition.

```text title="Converger"
converger (1) (2) [3] [4] [5]
# (1) string, converger type
# (2) int, unique tag
# [3] double, tolerance, default: 1E-6
# [4] int, maximum iteration, default: 10
# [5] bool string, print switch, default: false
```

## Available Convergers

Currently, the following convergers are available.

* [AbsDisp](Absolute/AbsDisp.md)
* [AbsError](Absolute/AbsError.md)
* [AbsIncreDisp](Absolute/AbsIncreDisp.md)
* [AbsIncreEnergy](Absolute/AbsIncreEnergy.md)
* [AbsIncreAcc](Absolute/AbsIncreAcc.md)
* [AbsResidual](Absolute/AbsResidual.md)
* [RelDisp](Relative/RelDisp.md)
* [RelError](Relative/RelError.md)
* [RelIncreDisp](Relative/RelIncreDisp.md)
* [RelIncreEnergy](Relative/RelIncreEnergy.md)
* [RelIncreAcc](Relative/RelIncreAcc.md)
* [RelResidual](Relative/RelResidual.md)
* [FixedNumber](Other/FixedNumber.md)
* [Logic](Other/Logic.md)

## Choosing a Converger

The tolerance-based convergers converge when their error is strictly smaller than the tolerance.
The error measures used by the `is_converged()` implementations are summarised below.

| Converger | Error measure | Typical use |
| --- | --- | --- |
| [AbsResidual](Absolute/AbsResidual.md) / [RelResidual](Relative/RelResidual.md) | residual norm, optionally divided by its value at the first iteration | force equilibrium; use the relative form when the load level varies |
| [AbsIncreDisp](Absolute/AbsIncreDisp.md) / [RelIncreDisp](Relative/RelIncreDisp.md) | incremental displacement norm, relative form divided by the total trial increment | general-purpose static and nonlinear analysis |
| [AbsDisp](Absolute/AbsDisp.md) / [RelDisp](Relative/RelDisp.md) | total displacement norm, relative form divided by the trial displacement | when absolute drift matters |
| [AbsError](Absolute/AbsError.md) / [RelError](Relative/RelError.md) | error reported by the solver, relative form divided by the trial displacement norm | when the solver supplies its own error measure |
| [AbsIncreEnergy](Absolute/AbsIncreEnergy.md) / [RelIncreEnergy](Relative/RelIncreEnergy.md) | absolute value of the inner product of incremental displacement and residual | energy-based stopping for nonlinear problems |
| [AbsIncreAcc](Absolute/AbsIncreAcc.md) / [RelIncreAcc](Relative/RelIncreAcc.md) | incremental acceleration norm, relative form divided by the total trial acceleration | dynamic analysis |
| [FixedNumber](Other/FixedNumber.md) | none; stops once the iteration counter reaches the maximum | forcing a fixed number of iterations |
| [Logic](Other/Logic.md) | combination of two other convergers | AND, OR or XOR of existing tests |

[`FixedNumber`](Other/FixedNumber.md) and [`Logic`](Other/Logic.md) have their own syntax and do not take the tolerance argument.
