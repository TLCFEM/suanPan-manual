# Combine

The `Combine` amplitude can combine multiple amplitudes together by multiplication so that

$$
A(t)=\Pi_{i=1}^nA_i(t)\quad\text{for}\quad{}t>t_0.
$$

## Syntax

```
amplitude Combine (1) [(2)...]
# (1) int, unique amplitude tag
# [(2)...] int, tags of amplitude that need to be combined
```