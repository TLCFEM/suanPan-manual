# TableCDP

The CDP Model With Tabular Data Support

The formulation is identical to that of the `CDP` model.

The tabular backbones and damage evolution are supported in this model to provide more flexibility in terms of customizing the response.

In total, four tables are required.

## Background

This model shares the return mapping, yield function, flow rule and damage treatment of [`CDP`](CDP.md).
The only difference is that the tension and compression backbones and their damage evolutions are read from tables instead of the built-in exponential functions, so the theoretical derivation is not repeated here.
The yield function is the Lubliner criterion modified by Lee and Fenves,

$$
F=\alpha I_1+\sqrt{3J_2}-\left(1-\alpha\right)\bar\sigma_c+\beta\left\langle\bar\sigma_{\max}\right\rangle,
$$

with $$\alpha=(\sigma_{b0}/\sigma_{c0}-1)/(2\sigma_{b0}/\sigma_{c0}-1)$$ and $$\beta=(1-\alpha)\bar\sigma_c/\bar\sigma_t-(1+\alpha)$$.
The internal variable $$\kappa$$ is the cumulative plastic work divided by the normalised fracture energy $$g_t$$ or $$g_c$$.

The parser converts the Abaqus-style plastic-strain input into this internal variable.
For each backbone the area under the stress--plastic-strain curve is integrated by the trapezoidal rule to give $$g$$, and the abscissa of each point is replaced by the cumulative area divided by $$g$$.
The damage table is interpolated onto the same $$\kappa$$ values, and the final point is extended to complete damage at $$\kappa=1$$ by an exponential tail that preserves the terminal slope of the backbone.
Consequently the tabulated curves are reparameterised internally, and the response can deviate slightly from the tabulated shape if the tables are too short or too coarse.

This variant fixes $$K_c=1$$, giving $$\zeta=0$$ in the yield function, exactly as [`CDP`](CDP.md) does.
The [`AbaqusCDP`](AbaqusCDP.md) variant is the counterpart that exposes $$K_c$$ and uses the Abaqus defaults for the dilatancy and recovery parameters.

!!! warning "implementation limitation"
    The tabulated plastic strain is not used directly as the internal variable; it is converted to cumulative plastic work by trapezoidal integration.
    A backbone without a decaying tail is rejected, and the appended exponential extension can distort the response near complete damage.
    As in [`CDP`](CDP.md), the potential is a linear cone with $$K_c=1$$ and there is a single recovery factor acting on tensile damage only.

## Syntax

```text title="TableCDP"
material TableCDP (1) (2) (3) (4) (5) (6) (7) [8] [9] [10] [11]
# (1) int, unique material tag
# (2) double, elastic modulus
# (3) double, Poisson's ratio
# (4) string, file name of tension backbone table
# (5) string, file name of compression backbone table
# (6) string, file name of tension damage table
# (7) string, file name of compression damage table
# [8] double, dilatancy parameter, default: 0.2
# [9] double, biaxial compression strength ratio, default: 1.16
# [10] double, stiffness recovery ratio, default: 0.5
# [11] double, density, default: 2400e-12
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
2. Beyond $$0.005$$, it asymptotically approaches unity at infinite plastic strain, that is $$\kappa_\aleph=1$$.

!!! warning "shape distortion"
    Because the mapping from $$\kappa_\aleph$$ to plastic strain is non-linear and includes an appended exponential tail, the actual material response slightly deviates from the defined curve.
    To minimize this error: 1) extend the input tables across a sufficiently wide plastic strain range, and 2) increase data point density to reduce linear interpolation distortion.

### Implementation notes

- The parser defaults are $$E=3\times10^4$$, $$\nu=0.2$$, $$\alpha_p=0.2$$, $$\sigma_{b0}/\sigma_{c0}=1.16$$, $$w=0.5$$ and density $$2400\times10^{-12}$$.
- The first column of every table is converted to its absolute value, and the first plastic strain must be zero.
- A backbone whose last two points do not form a decaying tail is rejected by the parser.
- The normalised energies $$g_t$$ and $$g_c$$ are computed from the tables and are not independent input arguments.
- The stiffness recovery factor applies only to the tensile damage index, and the compression damage index is never recovered.
- The four table file names are not interchangeable: the first two files must be the backbones and the last two the damage curves.

The above example can be defined using the following line.

```text
material TableCDP 1 3e4 .2 backbone backbone damage damage
```

The `backbone` file shall contain the following lines.

```text title="backbone"
0 1
0.001 1.5
0.002 1.3
0.003 .6
0.004 .2
0.005 .1
```

The `damage` file shall contain the following lines.

```text title="damage"
0 0
0.001 0.04
0.002 0.08
0.003 0.12
0.004 .16
0.005 .2
```

It can be tested via the following simple uniaxial loading setup.

```text title="tablecdp.sp"
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

## References

1. [10.1061/(ASCE)0733-9399(1998)124:8(892)](https://doi.org/10.1061/(ASCE)0733-9399(1998)124:8(892))
2. [10.1016/0020-7683(89)90050-4](https://doi.org/10.1016/0020-7683(89)90050-4)
