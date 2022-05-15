# TableCDP

The CDP Model With Tabular Data Support

The formulation is identical to that of the `CDP` model.

The tabular backbones and damage evolution are supported in this model to provide more flexibility in terms of
customizing the response.

In total, four tables are required.

## Restrictions

1. For backbone tables, the slope between the last two points **cannot** be zero. The last stress value shall be as
   close to zero as possible.
2. For damage tables, the first point must be $$(0,0)$$, the last point does not have to be $$(1,1)$$ but shall stay in
   the unit square.
