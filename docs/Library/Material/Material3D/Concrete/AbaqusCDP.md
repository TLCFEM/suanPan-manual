# AbaqusCDP

The Abaqus CDP Model

This model offers a flavor of the CDP model that resembles the one implemented in Abaqus.

In total, four tables are required.

## Syntax

```text title="AbaqusCDP"
material AbaqusCDP (1) (2) (3) (4) (5) (6) (7) [8] [9] [10] [11] [12]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, poisson's ratio
# (4) string, file name of tension backbone table
# (5) string, file name of compression backbone table
# (6) string, file name of tension damage table
# (7) string, file name of compression damage table
# [8] double, dilatancy parameter, default: 0.6
# [9] double, biaxial compression strength ratio, default: 1.16
# [10] double, ratio between tensile and compressive meridian stresses, default: 0.667
# [11] double, stiffness recovery ratio, default: 0
# [12] double, density, default: 2400e-12
```

## Remarks

The definitions and usages of tables are identical to that of the [`TableCDP`](TableCDP.md) model.
Compared to the [`TableCDP`](TableCDP.md) model, the following differences shall be noted.

1. An additional parameter `[10]` is required, this is the ratio between tensile and compressive meridian stresses, in Abaqus' notation, it is $$K$$ or $$K_c$$.
   According to [10.1016/0020-7683(89)90050-4](https://doi.org/10.1016/0020-7683(89)90050-4), typical values range from $$0.6$$ to $$0.8$$ and a default value is $$2/3$$.
   This only affects the triaxial compression cases.
2. The stiffness recovery ratio `[11]` defaults to $$0$$ to meet the same default beahviour in Abaqus.
3. The dilatancy parameter `[8]` defaults to $$0.6$$, which corresponds to about $$31\text{\degree}$$ dilatancy angle.
   Neither this value nor the original value $$0.2$$ would be universal, one may still need to choose a proper value to meet the specific shear demand.

Compared to the original Abaqus' CDP implementation, the following features are **not** implemented.

1. Abaqus supports input tables of various format, this `AbaqusCDP` model only accepts tables using plastic strain as the x-axis.
2. Abaqus supports both tension and compression damage recovery, this `AbaqusCDP` model only account for tensiion stiffness recovery (via parameter `[11]`).
3. Abaqus has an eccentricity parameter in the plastic flow potential, this is not considered in this `AbaqusCDP` model.
   This parameter only affects a small region around the apex and is introduced to ensure the surface is smooth to remove the sigularity.
   The gain is not significant while accounting for this parameter would significantly complicate the implementation.
