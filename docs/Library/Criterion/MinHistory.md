# MinHistory

The `MinHistory` criterion tests the specified historical variable, if it **exceeds** (be smaller than) the given value, the corresponding
element is disabled.

## Syntax

```text title="MinHistory"
criterion MinHistory (1) (2) (3) [(4)...]
# (1) int, unique criterion tag
# (2) string, history variable type
# (3) double, limit
# (4) int, optional indices
```

## Remarks

If the optional indices are not given, this criterion goes through all target quantities an element can record, if any values exceed the limit, the element is disabled.

If the optional indices are given, the element is disabled if all values at valid indices exceed the limit for any integration points.
