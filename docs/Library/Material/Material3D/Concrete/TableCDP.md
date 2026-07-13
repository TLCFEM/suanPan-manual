# TableCDP

The CDP Model With Tabular Data Support

The formulation is identical to that of the `CDP` model.

The tabular backbones and damage evolution are supported in this model to provide more flexibility in terms of
customizing the response.

In total, four tables are required.

## Syntax

```text
material TableCDP (1) (2) (3) (4) (5) (6) (7) [8] [9] [10] [11]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, poisson's ratio
# (4) string, file name of tension backbone table
# (5) string, file name of compression backbone table
# (6) string, file name of tension damage table
# (7) string, file name of compression damage table
# [8] double, dilatancy parameter, default: 0.2
# [9] double, biaxial compression strength ratio, default: 1.16
# [10] double, stiffness recovery ratio, default: 0.5
# [11] double, density, default: 0
```

## Remarks

1. The backbone tables define curves between plastic strain $$\varepsilon_p$$ (first column) and stress backbone $$f$$ or $$\sigma$$ (second column).
2. The damage tables define curves between plastic strain $$\varepsilon_p$$ (first column) and damage variable $$D$$ (second column).
3. The first point of plastic strain $$\varepsilon_p$$ shall be zero.
4. For backbone tables, the last point shall have a sufficiently small (close to zero) stress value at a sufficiently large plastic strain.
5. For damage tables, the first point must be $$(0,0)$$, the last damage value shall not exceed one.

The backbone tables represent the functions illustrated in Fig. 1 of [10.1016/0020-7683(89)90050-4](https://doi.org/10.1016/0020-7683(89)90050-4).
To maintain consistency, the damage tables shall share the same primary column as their corresponding backbone tables.
Consequently, the backbone stress and the corresponding damage index are evaluated at identical plastic strain samplings $\varepsilon_p$ and consolidated into two tables.
