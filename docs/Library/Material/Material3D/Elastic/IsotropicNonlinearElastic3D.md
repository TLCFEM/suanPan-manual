# IsotropicNonlinearElastic3D

General Nonlinear Elastic Isotropic 3D Material Framework

The `IsotropicNonlinearElastic3D` class is an abstract general purpose framework.

It offers an interface to allow users to define arbitrary strain energy potential based on volumetric strain and
equivalent strain (squared), that is

$$
W=f\left(\varepsilon_v,\varepsilon_p^2\right),
$$

where

$$
\varepsilon_v=\text{trace}\left(\varepsilon\right),\qquad\varepsilon_p=\sqrt{\dfrac{2}{3}\varepsilon_d:
\varepsilon_d}.
$$

Note it is normally expressed in terms of equivalent strain rather than its square. However, the derivation of tangent
stiffness would be too cumbersome.

## Overridden Method

The `IsotropicNonlinearElastic3D` provides a method that shall be overridden.

```cpp
virtual vec compute_derivative(double, double) = 0;
```

The first argument is $$\varepsilon_v$$. The second argument is $$\varepsilon_s=\varepsilon_p^2$$.

The method shall return a vector of size six with following values computed.

| **index** | **value**                                                           |
|:----------|:--------------------------------------------------------------------|
| $$0$$     | $$\dfrac{\partial{}W}{\partial\varepsilon_v}$$                      |
| $$1$$     | $$\dfrac{\partial{}W}{\partial\varepsilon_s}$$                      |
| $$2$$     | $$\dfrac{\partial^2W}{\partial\varepsilon_v^2}$$                    |
| $$3$$     | $$\dfrac{\partial^2W}{\partial\varepsilon_s^2}$$                    |
| $$4$$     | $$\dfrac{\partial^2W}{\partial\varepsilon_v\partial\varepsilon_s}$$ |
| $$5$$     | $$\dfrac{\partial^2W}{\partial\varepsilon_s\partial\varepsilon_v}$$ |
