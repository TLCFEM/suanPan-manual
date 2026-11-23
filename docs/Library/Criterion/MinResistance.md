# MinResistance

The `MinResistance` criterion tests the resistance of the specified node; if it is **smaller** than the given value, the analysis is terminated.

## Syntax

```text title="MinResistance"
criterion MinResistance (1) (2) (3) (4)
# (1) int, unique criterion tag
# (2) int, node
# (3) string, dof token
# (4) double, limit
```

## Background

The test reads the current global resistance of the first DoF matching the given token.
It emits a termination signal only for the strict inequality `current resistance < limit`.
If the node has no matching DoF, the criterion does nothing.

## Remarks

The resistance is the signed force component conjugate to the selected DoF, so the limit may be positive or negative.
The criterion must be active in the current step, as explained in [`Criterion`](Criterion.md).

## Example

```text
step static 1
criterion MinResistance 1 11 2 -5.
```
