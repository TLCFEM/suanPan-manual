# Logic

Multiple criteria can be combined to emit a termination signal under certain logical conditions.

## Syntax

```text title="Logic"
criterion LogicAll (1) [(2)...]
criterion LogicAny (1) [(2)...]
# (1) int, unique criterion tag
# [(2)...] int, tag of criteria in logical operation
```

## Background

`LogicAll` emits a termination signal only when every referenced criterion returns one.
`LogicAny` emits it as soon as at least one referenced criterion returns one.
If any referenced criterion fails to process, the error is propagated and the combined criterion fails as well.

## Remarks

Each referenced criterion is copied when the logic criterion is initialised, so its tag must already exist.
See [`Criterion`](Criterion.md) for the activation rule: a criterion must be defined inside the step that uses it, or referenced from a logic criterion defined there.

## Example

```text
criterion MaxDisplacement 1 11 2 5.
criterion MinResistance 2 11 2 -10.

step static 1
criterion LogicAny 3 1 2
```
