# Parallel

Container of Material Models In Parallel

## Syntax

```
material Parallel (1) (2...)
# (1) int, unique material tag
# (2...) int, material tags of 1D models need to be contained
```

## Caveat

Please do not include any viscosity related models into the wrapper. This container is only designed for
rate-independent hysteric models. The response of attached 1D material models will be output when recorded. The output
has the uniform size and data is arranged in the order as defined.
