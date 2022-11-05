# response_spectrum

Compute Response Spectrum of a Given Accelerogram

Minimum version: v2.6

Reference:

1. [https://doi.org/10.1016/S0267-7261(05)80015-6](https://doi.org/10.1016/S0267-7261(05)80015-6)

Please note the following.

1. **Only applies to elastic system.**
2. **Only trivial initial conditions are accounted for.**

## Syntax

### Form A

For accelerogram record stored in single column plain text file. The following syntax can be used.

```text
response_spectrum (1) (2) (3) (4)
# (1) string, file path of the accelerogram file
# (2) string, file path of the period file
# (3) double, sampling interval
# (4) double, damping ratio
```

The accelerogram stores discrete acceleration amplitudes in the first column of the file.

The desired period points where the response spectrum is computed are stored in the first column of the period
file. The period file itself can have multiple columns, but only the first column is used.

As the accelerogram only provides the amplitudes, the sampling interval must be provided as the `(3)` argument.

### Form B

For accelerogram record stored in double column plain text file. The following syntax can be used.

```text
response_spectrum (1) (2) (3)
# (1) string, file path of the accelerogram file
# (2) string, file path of the period file
# (3) double, damping ratio
```

The accelerogram stores the time and acceleration amplitudes in the first and second columns of the file.

The time series _**must**_ be equally spaced.

The desired period points where the response spectrum is computed are stored in the first column of the period
file. The period file itself can have multiple columns, but only the first column is used.

## Remarks

The sampling interval is provided as the `(3)` argument in Form A, and is computed from the time series in Form B.

The same sampling interval is used in Lee's algorithm to compute the response histories. If the provided interval is 
large, the response spectra may be inaccurate. One can use the [`upsampling`](upsampling.md) command to process the 
accelerogram before using the `response_spectrum` command.

## Example

See [this example](../../Example/Structural/Dynamics/computing-response-spectrum.md).
