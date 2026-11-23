# Prestrain

Prestrain Wrapper

Wraps a uniaxial host material model so that a prestrain can be applied.
This may be useful for modelling prestressed reinforced concrete or similar multiphase materials.

## Background

An imposed or eigenstrain is a strain that develops without a corresponding stress in a free body, such as thermal expansion, shrinkage or the strain imposed by a tensioning operation.
The wrapper evaluates the host at a shifted strain,

$$
\varepsilon_{\mathrm{host}}(t)=\varepsilon_{\mathrm{element}}+\alpha(t)\,\varepsilon_0,
\qquad
\sigma=\sigma_{\mathrm{host}}\!\left(\varepsilon_{\mathrm{host}}\right),
\qquad
D=D_{\mathrm{host}}\!\left(\varepsilon_{\mathrm{host}}\right),
$$

where $\varepsilon_0$ is the magnitude `(4)`, $\alpha(t)$ is the value of the amplitude at the current trial time, and $\varepsilon_{\mathrm{element}}$ is the strain reported by the element.
The stress returned to the element is simply the host stress at the shifted strain, so a restrained bar develops stress while a free bar deforms by $-\alpha\varepsilon_0$ to cancel it.
Because the wrapper shifts the strain rather than the stress, any prescribed prestress must first be converted to an equivalent prestrain by a uniaxial calibration.
Setting the amplitude tag to zero selects a built-in ramp that grows linearly with time, and an unusable nonzero tag also falls back to a ramp with a warning.
The strain rate passed to a rate-dependent host is not shifted, only the strain itself.

## Syntax

```text title="Prestrain"
material Prestrain (1) (2) (3) (4)
# (1) int, unique material tag
# (2) int, underlying material tag
# (3) int, amplitude tag, set to 0 to use a ramp function
# (4) double, magnitude
```

## Remarks

It is necessary to attach an amplitude.
The amplitude is in charge of applying the designated prestrain (of the specified magnitude) to the underlying material in a controlled manner.

If only a prestress is available, one can always develop a uniaxial test model to compute the prestrain from the prestress.
Thus, we do not provide a `Prestress` counterpart.

The host must be a registered 1D material, and the wrapper inherits its density, stiffness and damping.
The amplitude is evaluated at the trial analysis time and multiplied by the magnitude, so the prestrain can be ramped, stepped or given any user-defined time history.
The wrapper adds the prestrain to the element strain before calling the host, so a positive magnitude produces a positive host stress at zero element strain and drives node 2 in the negative direction in the self-equilibrated example above.
Recorded quantities are forwarded to the host and therefore refer to the shifted strain state, not to the element strain alone.
Use a [Parallel](Parallel.md) container to combine a prestrained constituent with other 1D constituents, or [Sequential](Sequential.md) when the constituents must share a stress instead.

## Example

```text
node 1 0 0
node 2 1 0

material Elastic1D 1 100
material Prestrain 2 1 0 1E-2

element T2D2 1 1 2 1 10
element T2D2 2 1 2 2 10

fix2 1 1 1
fix2 2 2 1 2

step static 1
set ini_step_size .1

converger AbsIncreDisp 1 1E-4 10 1

analyze

peek node 2

exit
```

The above example is a simple demonstration.
The prestrain $$0.01$$ will be gradually (linearly increasing from zero to the specific magnitude) applied to the second element.
The system balances itself without any external load.

The final displacement of node 2 should be $$0.005$$ since both elements share the same section properties.

!!! warning "sign of the example displacement"
    Running this exact input with the suanPan binary gives a final displacement of $-0.005$ at node 2, not $+0.005$.
    The wrapper evaluates the host at $\varepsilon+\alpha\varepsilon_0$, so a positive amplitude drives the bar in the negative direction when no external load is applied.
    The magnitude $0.005$ is correct because the two identical bars share the imposed deformation equally, but the sign in the original statement is reversed.

## References

- [ISBN 978-90-247-3343-9](https://search.worldcat.org/search?q=bn:9789024733439)
- [ISBN 978-1-4398-0247-2](https://search.worldcat.org/search?q=bn:9781439802472)
