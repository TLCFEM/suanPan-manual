# TabularSpline

The `TabularSpline` amplitude reads external tabular amplitude, interpolation is performed when necessary.

There should be exactly two columns in the external file. The first column is time point, and the second one shall be
the amplitude.

The **cubic spline interpolation** is used. The first derivatives of two ends (of the interpolated curve) are set to 
zero. See [this page](https://en.wikiversity.org/wiki/Cubic_Spline_Interpolation) for more details.

## Reference

1. [10.1080/13632469.2024.2372814](https://doi.org/10.1080/13632469.2024.2372814)

## Syntax

```text
amplitude TabularSpline (1) (2)
# (1) int, unique amplitude tag
# (2) string, external file name
```

## Remarks

This amplitude implementation changes the original piece-wise linear amplitude defined in the provided table.
This thus results in a slightly different shape compared to the original one.

This shall exclusively used in seismic analysis and apply to ground motions.

The main motivation is to curb the unwanted potential spurious responses in the final results.
The technical details have been extensively discussed in [this paper](https://doi.org/10.1080/13632469.2024.2372814).

This shall only be used if filtering the original record is not feasible.
Otherwise, filtering as showcased in the paper is always preferred in order to obtain results of better quality.
