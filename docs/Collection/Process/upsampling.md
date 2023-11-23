# upsampling

Upsample a Given Seismogram

Minimum version: v2.6

## Syntax

```text
upsampling (1) (2) [3] [4]
# (1) string, file path of the seismogram file
# (2) integer, upsampling rate
# [3] string, window type, default: 'Hamming'
# [4] integer, window length, default: 0
```

## Remarks

The seismogram _**must**_ be stored in double column plain text file. The first column stores the time series, and the
second column stores the acceleration amplitudes.

The time series _**must**_ be equally spaced.

The window type can be one of the following:

- Hamming
- Hann
- Blackman
- BlackmanNuttall
- BlackmanHarris
- FlatTop

If the upsampling rate is denoted as $$L$$, the window length is $$nL+1$$.
The parameter $$n$$ is controlled by the last parameter.
