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
Consequently, the backbone stress and the corresponding damage index are evaluated at identical plastic strain samplings $$\varepsilon_p$$ and consolidated into two tables.

## Example

In the following, a basic example illustrates the required table formats for defining a `TableCDP` model.
In the original formulation, an internal variable $$\kappa_\aleph$$ governs the evolution of the apparent backbone, effective backbone, and damage index.
However, mapping $$\kappa_\aleph$$ to the corresponding plastic strain is not straightforward.

In `TableCDP`, we adopt the ABAQUS framework: all tables are formulated as functions of plastic strain $$\varepsilon_p$$.
Because the table definitions for tension and compression are functionally identical, the following single example applies to both regimes.

<iframe src="https://www.desmos.com/calculator/fwvthokom8?embed" width="800" height="400" style="border: 1px solid #ccc" frameborder=0></iframe>

The green curve represents the actual stress backbone, yielding several key properties:

1. The stress at zero plastic strain is $$1$$, establishing the initial yield surface size.
2. Peak stress occurs at $$0.001$$; hence, this response resembles a compressive backbone (unlike tension, which typically exhibits no strain hardening).
3. Post-peak stress decays to $$0.1$$ at $$0.005$$.
4. Beyond $$0.005$$, an exponential decay tail is appended to ensure the backbone remains well-defined across all plastic strain levels.

The red curve depicts the damage index evolution:

1. It initiates at zero and rises to $$0.2$$ at $$0.005$$.
2. Beyond $$0.005$$, it asymptotically approaches unity at infinite plastic strain ($$\kappa_\aleph=1$$).

!!! warning "shape distortion"
    Because the mapping from $$\kappa_\aleph$$ to plastic strain is non-linear and includes an appended exponential tail, the actual material response slightly deviates from the defined curve.
    To minimize this error: 1) extend the input tables across a sufficiently wide plastic strain range, and 2) increase data point density to reduce linear interpolation distortion.

The above example can be defined using the following line.

```text
material TableCDP 1 3e4 .2 backbone backbone damage damage
```

The `backbone` file shall contain the following lines.

```text
0 1
0.001 1.5
0.002 1.3
0.003 .6
0.004 .2
0.005 .1
```

The `damage` file shall contain the following lines.

```text
0 0
0.001 0.04
0.002 0.08
0.003 0.12
0.004 .16
0.005 .2
```

It can be tested via the following simple uniaxial loading setup.

```text
# A TEST MODEL FOR TABLECDP MATERIAL

node 1 .5 -.5 0
node 2 .5 .5 0
node 3 -.5 .5 0
node 4 -.5 -.5 0
node 5 .5 -.5 1.0
node 6 .5 .5 1.0
node 7 -.5 .5 1.0
node 8 -.5 -.5 1.0

material TableCDP 1 3e4 .2 backbone backbone damage damage

element C3D8 1 1 2 3 4 5 6 7 8 1 G

recorder 1 hdf5 Element E33 1
recorder 2 hdf5 Element S33 1
recorder 3 hdf5 Element DT 1
recorder 4 hdf5 Element DC 1
recorder 5 hdf5 Element PE33 1

fix 1 1 1 2 5 6
fix 2 2 1 4 5 8
fix 3 3 1 2 3 4

displacement 1 0 1e-2 3 5 6 7 8

step static 1
set fixed_step_size 1
set ini_step_size 1e-2
set symm_mat 0

converger AbsIncreDisp 1 1E-11 10 1

analyze

save recorder 1 2 3 4 5

exit
```