# Tabular

The `Tabular` amplitude reads external tabular amplitude, interpolation is performed when necessary.

There should be exactly two columns in the external file. The first column is time point, and the second one shall be
the amplitude.

## Syntax

```
amplitude Tabular (1) (2)
# (1) int, unique amplitude tag
# (2) string, external file name
```