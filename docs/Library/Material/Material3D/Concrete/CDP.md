# CDP

Concrete Damage Plasticity Model

## References

1. [10.1061/(ASCE)0733-9399(1998)124:8(892)](https://doi.org/10.1061/(ASCE)0733-9399(1998)124:8(892))
2. [10.1002/(SICI)1096-9845(199809)27:9<937::AID-EQE764>3.0.CO;2-5](https://doi.org/10.1002/(SICI)1096-9845(199809)27:9%3C937::AID-EQE764%3E3.0.CO;2-5)
3. [10.1002/1097-0207(20010120)50:2<487::AID-NME44>3.0.CO;2-N](https://doi.org/10.1002/1097-0207(20010120)50:2%3C487::AID-NME44%3E3.0.CO;2-N)
4. [10.1016/0020-7683(89)90050-4](https://doi.org/10.1016/0020-7683(89)90050-4)

## Outline

The CDP model supports stiffness degradation. The backbone envelops are defined as exponential functions in terms of
plastic strain [4]. Apart from the listed references, readers can also refer to the corresponding section
in [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook/releases/download/latest/COOKBOOK.pdf).

## Syntax

```text
material CDP (1) (2) (3) (4) (5) (6) (7) (8) (9) (10) (11) (12) (13) (14) [15]
# (1) int, unique tag
# (2) double, elastic modulus
# (3) double, poissons ratio
# (4) double, crack stress f_t
# (5) double, crush stress f_c
# (6) double, normalized crack energy g_t
# (7) double, normalized crush energy g_c
# (8) double, initial tension hardening a_t<1
# (9) double, initial compression hardening a_c>1
# (10) double, damage factor at half crack stress d_t
# (11) double, damage factor at peak crush stress d_c
# (12) double, dilatancy parameter
# (13) double, biaxial compression ratio
# (14) double, initial stiffness recovery factor
# [15] double, density, default: 2400E-12
```

## Remarks

1. Poisson's ratio shall be smaller than $$0.5$$, a typical value for concrete is around $$0.2$$.
2. Crack stress shall be greater than zero while crush stress shall be smaller than zero. But the program automatically
   set the signs for both stresses.
3. Normalized crack energy $$g_t=G_F/l_c$$ equals the first mode crack energy $$G_F$$ over the characteristic length
   $$l_c$$. For SI (millimeter) unit system, typical values are of order $$10^{-3}$$. The compression conjugate $$g_c$$
   is typically greater than $$g_t$$ by the order of $$10^2$$.
4. Hardening parameters controls tension degradation slope and compression hardening shape. Values $$a_t\approx0.5$$ and
   $$a_c\approx2$$ to $$a_c\approx5$$ give good results.
5. Dilatancy parameter can be set to $$0.2$$. Comparisons can be seen in Lee's doctoral dissertation.
6. Biaxial compression ratio is defined as the ratio between biaxial and uniaxial compression strengths. According to
   Kupfer et al. (1969), a value of $$1.16$$ is recommended.
7. Initial stiffness recovery factor controls the amount of stiffness recovery when loading direction changes.
8. Theoretically, $$g_t$$ and $$g_c$$ shall be scaled according to the size of mesh grid. Practically, they cannot be
   arbitrarily small due to numerical stability issues, meaning that the mesh grid cannot be arbitrarily large.

## History Layout

| location               | parameter      |
|------------------------|----------------|
| `initial_history(0)`   | $$d_t$$        |
| `initial_history(1)`   | $$d_c$$        |
| `initial_history(2)`   | $$\kappa_t$$   |
| `initial_history(3)`   | $$\kappa_c$$   |
| `initial_history(4-9)` | plastic strain |

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning              |
|----------------|-------------------------------|
| DT             | tensile damage                |
| DC             | compressive damage            |
