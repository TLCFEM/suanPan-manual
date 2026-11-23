# MaxDisplacement

The `MaxDisplacement` criterion tests the displacement of the specified node; if it is **greater** than the given value, the analysis is terminated.

## Syntax

```text title="MaxDisplacement"
criterion MaxDisplacement (1) (2) (3) (4)
# (1) int, unique criterion tag
# (2) int, node
# (3) string, dof token
# (4) double, limit
```

## Background

The test reads the current global displacement of the first DoF matching the given token.
It emits a termination signal only for the strict inequality `current displacement > limit`.
If the node has no matching DoF, the criterion does nothing.

## Remarks

The limit is compared with a single signed displacement component, not with a magnitude.
The criterion must be active in the current step, as explained in [`Criterion`](Criterion.md).

## Example

```text
step static 1
criterion MaxDisplacement 1 2 2 .1
```
