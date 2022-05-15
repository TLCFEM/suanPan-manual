# Trigonometric

The amplitude is computed based on the following summation.

For `Sine`,

$$
A(t)=\sum{}a_i\sin(i\dfrac{2\pi}{T_0}(t-t_0)=\sum{}a_i\sin(if_0(t-t_0))\quad\text{for}\quad{}t>t_0.
$$

For `Cosine`,

$$
A(t)=\sum{}a_i\cos(i\dfrac{2\pi}{T_0}(t-t_0))=\sum{}a_i\cos(if_0(t-t_0))\quad\text{for}\quad{}t>t_0.
$$

In above equations, $$T_0$$ is the base period and $$f_0$$ is base frequency accordingly. In the above definition,
$$t_0$$ is the (pseudo) start time of the step in which the amplitude is defined.

## Syntax

```
amplitude Sine (1) (2) (3) [(4)...]
amplitude Cosine (1) (2) (3) [(4)...]
# (1) int, unique tag
# (2) double, base period T_0
# (3) double, amplitude at base period/frequency a_0
# [(4)...] double, optional amplitudes at higher periods a_i
```

## Example

```
amplitude Sine 1 10. 2.
```

$$
A(t)=2\sin(\dfrac{\pi}{5}(t-t_0)).
$$

```
amplitude Sine 1 10. 2. 4.
```

$$
A(t)=2\sin(0.2\pi{}(t-t_0))+4\sin(0.4\pi{}(t-t_0)).
$$