# Yeoh

Regularized Yeoh Material For Compressible Rubbers

The following strain energy density is used.

$$
W=\sum_{i=1}^nC_{i0}(J_1-3)^i+\sum_{i=1}^nC_{i1}(J_3-1)^{2i}.
$$

where $$C_{i0}$$ and $$C_{i1}$$ are material constants. $$J_1$$ and $$J_3$$ are reduced invariants of the right
Cauchy-Green deformation tensor.

## Syntax

```
material Yeoh (1) (2...)
# (1) int, unique material tag
# (2...) double, material constants with possible density
```

## Remarks

1. The above command takes input list of arbitrary length ($$\ge2$$, excluding tag).
2. If the number of double inputs is odd, the last one is interpreted as density.
3. If the number of double inputs is even, the density is assumed to be zero.
4. The first half of double inputs is read as $$C_{i0}$$ and the second half $$C_{i1}$$.

## Examples

For $$i=1$$, let $$C_{10}=20$$ and $$C_{11}=4000$$, the strain energy density is

$$
W=20(J_1-3)+4000(J_3-1)^2.
$$

The following command shall be used.

```
material Yeoh 1 20 4000
```

If density is nonzero, say for example $$\rho=10^{-4}$$, then the following command shall be used.

```
material Yeoh 1 20 4000 1E-4
```

For $$i=3$$, let $$C_{10}=20$$, $$C_{20}=30$$, $$C_{30}=40$$, $$C_{11}=2000$$,$$C_{21}=3000$$ and $$C_{31}=4000$$, the
strain energy density is

$$
W=20(J_1-3)+30(J_1-3)^2+40(J_1-3)^3+2000(J_3-1)^2+3000(J_3-1)^4+4000(J_3-1)^6.
$$

The following command shall be used.

```
material Yeoh 1 20 30 40 2000 3000 4000
```
