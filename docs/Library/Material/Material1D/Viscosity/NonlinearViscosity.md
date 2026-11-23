# NonlinearViscosity

Nonlinear Viscosity Model

The `NonlinearViscosity` class is an abstract class that provides a general nonlinear framework for implementations of various viscous type materials, such as a dashpot.

The stress shall be computed by

$$
\sigma=\text{sign}\left(\dot\varepsilon\right)\cdot\eta\left(\varepsilon,\dot\varepsilon\right)
\cdot|\dot\varepsilon|^\alpha.
$$

The so-called viscosity $$\eta\left(\varepsilon,\dot\varepsilon\right)$$ can be a general function of strain and/or strain rate.

If the target material is not characterized by the classic power-law, it is possible to pass $$\alpha=0$$ to the `NonlinearViscosity` class so that the response becomes

$$
\sigma=\eta\left(\varepsilon,\dot\varepsilon\right)
$$

that can be purely determined by the derived class.

## Theory

Let $v=\dot\varepsilon$ denote the strain rate.
The base class represents a generalised nonlinear dashpot whose stress is

$$
\sigma=\operatorname{sign}(v)\,\eta\left(\varepsilon,v\right)\,|v|^\alpha,
$$

where $\eta$ is a viscosity that may depend on both strain and strain rate and $\alpha$ is the flow exponent.
For $\alpha=1$ the law reduces to the linear viscous dashpot $\sigma=\eta v$, while for $\alpha=0$ the power-law factor is suppressed and the derived class defines the whole stress law through $\eta$.
For $0<\alpha<1$ the function $|v|^\alpha$ has unbounded slope at the origin, which is regularised by a cubic polynomial on $|v|<L$, with $L$ the cut-off passed to the constructor.
The cubic coefficients are

$$
a=\left(\dfrac{\alpha}{2}-\dfrac{1}{2}\right)L^{\alpha-3},\qquad
b=\left(\dfrac{3}{2}-\dfrac{\alpha}{2}\right)L^{\alpha-1},
$$

so that the replacement $a v^2+b$ matches $|v|^{\alpha-1}$ in value and $\alpha|v|^{\alpha-1}$ in slope at $v=\pm L$.

!!! info "deviation from theory"
    The exact power law is replaced by a $C^1$ cubic only for $0<\alpha<1$ and $|v|<L$.
    Outside that window the exact power law is used, so the model is not a single power law over the full velocity range.

The trial stress and the two tangents are assembled as

$$
\sigma=\eta\,(a v^2+b)\,v,
$$

$$
k=\dfrac{\partial\eta}{\partial\varepsilon}\,(a v^2+b)\,v,\qquad
c=\eta\,(3a v^2+b)+\dfrac{\partial\eta}{\partial v}\,(a v^2+b)\,v.
$$

Outside the cut-off region, or for $\alpha\ge 1$, the exact power-law expressions $\sigma=\eta\,\operatorname{sign}(v)|v|^\alpha$ and $c=\eta\alpha|v|^{\alpha-1}+\partial\eta/\partial v\,\operatorname{sign}(v)|v|^\alpha$ are used.
For $\alpha=0$ the stress is simply $\eta$, with $k=\partial\eta/\partial\varepsilon$ and $c=\partial\eta/\partial v$.
For $\alpha=1$ the stress is $\eta v$, with $k=v\,\partial\eta/\partial\varepsilon$ and $c=\eta+v\,\partial\eta/\partial v$.

!!! warning "implementation limitation"
    For $\alpha=0$ the stress is $\eta$ directly and the sign of the strain rate is lost.
    This is a framework convention rather than a physical power-law dashpot.

!!! note "developer note"
    For $\alpha=0$ the base class sets the power-law factor to one.
    The convention is used by the derived classes.

## Things to Pass to Ctor

The default constructor is defined to be

```cpp
 NonlinearViscosity(unsigned, // tag
                    double,   // alpha
                    double    // cut-off
 );
```

The second parameter is the exponent $$\alpha$$.
The third parameter is a non-negative parameter that defines a segment of a cubic function that approximates the original exponential function to achieve a better numerical performance.

## Things to Override

Three private methods need to be overridden.

```cpp
 [[nodiscard]] virtual double compute_du(double, double) const = 0; // compute derivative w.r.t. strain
 [[nodiscard]] virtual double compute_dv(double, double) const = 0; // compute derivative w.r.t. strain rate
 [[nodiscard]] virtual double compute_damping_coefficient(double, double) const = 0; // compute \eta
```

All three methods take strain and strain rate to be two input arguments.

## Derived Material Models

1. [`Viscosity01`](Viscosity01.md)
2. [`Viscosity02`](Viscosity02.md)

## Remarks

This is an abstract base class and is not registered in the material parser, so it cannot be instantiated directly by a `material` command.
Both the exponent and the cut-off are converted to absolute values in the constructor.
The cut-off is only active for $0<\alpha<1$ and is ignored for $\alpha=0$ and $\alpha\ge1$.
A larger cut-off extends the smoothed region around zero velocity and improves robustness at the cost of deviating from the true power law at low rate.
The initial damping is evaluated from $\eta(0,0)$ scaled by the cubic constant $b$, so derived classes should return a finite viscosity at the origin.
The framework only implements the two-argument update that receives strain and strain rate, so derived materials must be attached to an element that supplies strain rate, such as [`Damper01`](../../../Element/Special/Damper01.md) or [`Damper02`](../../../Element/Special/Damper02.md).
Beyond the two built-in subclasses, [`BilinearViscosity`](BilinearViscosity.md) and [`CustomViscosity`](CustomViscosity.md) also use this framework with $\alpha=0$.
