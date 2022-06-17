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

## Restrictions

1. For backbone tables, the slope between the last two points **cannot** be zero. The last stress value shall be as
   close to zero as possible.
2. For damage tables, the first point must be $$(0,0)$$, the last point does not have to be $$(1,1)$$ but shall stay in
   the unit square.
