# NonlinearViscosity

Nonlinear Viscosity Model

The `NonlinearViscosity` class is an abstract class that provides a general nonlinear framework for implementations of
various viscous type material, such as a dashpot.

The stress shall be computed by

$$
\sigma=\text{sign}\left(\dot\varepsilon\right)\cdot\eta\left(\varepsilon,\dot\varepsilon\right)
\cdot|\dot\varepsilon|^\alpha.
$$

The so-called viscosity $$\eta\left(\varepsilon,\dot\varepsilon\right)$$ can be a general function of strain and/or
strain rate.

If the target material is not characterized by the classic power-law, it is possible to pass $$\alpha=0$$ to
the `NonlinearViscosity` class so that the response becomes

$$
\sigma=\eta\left(\varepsilon,\dot\varepsilon\right)
$$

that can be purely determined by the derived class.

## Things to Pass to Ctor

The default constructor is defined to be

```cpp
 NonlinearViscosity(unsigned, // tag
                    double,   // alpha
                    double    // cut-off
 );
```

The second parameter is the exponent $$\alpha$$. The third parameter is a non-negative parameter that defines a segment
of cubic function that approximates the original exponential function to achieve a better numerical performance.

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
