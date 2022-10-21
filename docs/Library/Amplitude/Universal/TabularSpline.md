# TabularSpline

The `TabularSpline` amplitude reads external tabular amplitude, interpolation is performed when necessary.

There should be exactly two columns in the external file. The first column is time point, and the second one shall be
the amplitude.

The **cubic spline interpolation** is used. The first derivatives of two ends (of the interpolated curve) are set to 
zero. See [this page](https://en.wikiversity.org/wiki/Cubic_Spline_Interpolation) for more details.

## Syntax

```
amplitude TabularSpline (1) (2)
# (1) int, unique amplitude tag
# (2) string, external file name
```
