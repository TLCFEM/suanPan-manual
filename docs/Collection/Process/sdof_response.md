# sdof_response

Compute Response of a Single Degree of Freedom Oscillator to a Given Acceleration Record

Minimum version: v2.6

Reference:

1. [https://doi.org/10.1016/S0267-7261(05)80015-6](https://doi.org/10.1016/S0267-7261(05)80015-6)

Please note the following.

1. **Only applies to elastic system.**
2. **Only trivial initial conditions are accounted for.**

## Syntax

**The frequency of the oscillator is used. Its unit is Hertz (Hz).**

Please note the natural frequency shall **not** be passed to the command. The natural frequency has a unit of radian per
second (rad/s).

### Form A

For accelerogram record stored in single column plain text file. The following syntax can be used.

```text
sdof_response (1) (2) (3) (4)
# (1) string, file path of the accelerogram file
# (2) double, sampling interval
# (3) double, frequency of the system
# (4) double, damping ratio
```

The accelerogram stores discrete acceleration amplitudes in the first column of the file.

As the accelerogram only provides the amplitudes, the sampling interval must be provided as the `(2)` argument.

### Form B

For accelerogram record stored in double column plain text file. The following syntax can be used.

```text
response_spectrum (1) (2) (3)
# (1) string, file path of the accelerogram file
# (2) double, frequency of the system
# (3) double, damping ratio
```

The accelerogram stores the time and acceleration amplitudes in the first and second columns of the file.

The time series _**must**_ be equally spaced.

## Example

See [this example](../../Example/Structural/Dynamics/computing-response-spectrum.md).
