# NonlinearJ2

Nonlinear General J2 Plasticity Model

## Summary

This is an abstract material class thus cannot be used directly. This class defines a general plasticity model using J2
yielding criterion with associated flow rule and mixed hardening rule. The isotropic/kinematic hardening response can be
customized.

To use this model, a derived class shall be defined first.

```cpp
class YourJ2 final : public NonlinearJ2 {
// class definition
}
```

The derived class only needs to implement four pure virtual methods that define the isotropic and kinematic hardening
rules.

```cpp
virtual double compute_k(double) const = 0; // isotropic hardening
virtual double compute_dk(double) const = 0; // derivative isotropic
virtual double compute_h(double) const = 0; // kinematic hardening
virtual double compute_dh(double) const = 0; // derivative kinematic
```

All four methods take equivalent plastic strain as the input argument, on output, the corresponding quantities shall be
provided.

The isotropic hardening function $$K(\bar\varepsilon_p)$$ defines the isotropic hardening rule, there are some
requirements:

1. $$K(\bar\varepsilon_p)$$ should be non-negative,
2. $$K(\bar\varepsilon_p=0)=\sigma_y$$ where $$\sigma_y$$ is the initial yielding stress.

There is no requirement for the kinematic hardening function $$H(\bar\varepsilon_p)$$. Both hardening rules can coexist.
However, to successfully solve the trial status, there is an additional constraint that shall be applied on the model:

$$
E+H'(\bar\varepsilon_p)+K'(\bar\varepsilon_p)\geqslant0~\text{for all}~\bar\varepsilon_p
$$

Otherwise, the local Newton iteration will fail.

## Brief On Theory

The `NonlinearJ2` abstract class defines an associative plasticity framework using the von Mises yield criterion, which
is defined as follows.

$$
F(\sigma,\bar\varepsilon_p)=\sqrt{\dfrac{3}{2}(s-\beta(\bar\varepsilon_p)):(s-\beta(\bar\varepsilon_p))}-\sigma_y(
\bar\varepsilon_p)
$$

where $$\beta(\bar\varepsilon_p)$$ is the back stress depends on the equivalent plastic strain $$\bar\varepsilon_p$$ and
$$\sigma_y(\bar\varepsilon_p)$$ is the yield stress. Note

$$
\sqrt{3J_2}=\sqrt{\dfrac{3}{2}(s-\beta(\bar\varepsilon_p)):(s-\beta(\bar\varepsilon_p))}
$$

It is also called J2 plasticity model. A detailed discussion can be seen elsewhere. $$\beta(\bar\varepsilon_p)=H(
\bar\varepsilon_p)$$ and $$\sigma_y(\bar\varepsilon_p)=K(\bar\varepsilon_p)$$.

## History Layout

| location               | paramater                  |
|------------------------|----------------------------|
| `initial_history(0)`   | accumulated plastic strain |
| `initial_history(1-6)` | back stress                |

## Kinematic Hardening

The back stress $$\beta(\bar{\varepsilon}_p)$$ defines a kinematic hardening response. For example a linear kinematic
hardening could be defined as:

$$
\beta(\bar\varepsilon_p)=E_K\bar\varepsilon_p
$$

and the derivative

$$
\dfrac{\mathrm{d}\beta(\bar\varepsilon_p)}{\mathrm{d}\bar\varepsilon_p}=E_K
$$

in which $$E_K$$ is the kinematic hardening stiffness.

In this case, user shall override the corresponding two methods with such an implmentation.

```cpp
double SampleJ2::compute_h(const double p_strain) const { return e_kin * p_strain; }
double SampleJ2::compute_dh(const double) const { return e_kin; }
```

Of course, a nonlinear relationship could also be defined.

## Isotropic Hardening

The isotropic hardening is defined by function $$\sigma_y(\bar\varepsilon_p)$$. The value $$\sigma_y(0)$$ should be the
initial yield stress. Also, for a bilinear isotropic hardening response, user shall override the following two methods.

```cpp
double SampleJ2::compute_k(const double p_strain) const { return e_iso * p_strain + yield_stress; }
double SampleJ2::compute_dk(const double) const { return e_iso; }
```

Here another polynomial based isotropic hardening function is shown as an additional example. The function is defined as

$$
\sigma_y=\sigma_0(1+\sum_{i=1}^{n}a_i\bar\varepsilon_p^i)
$$

where $$a_i$$ are material constants. It is easy to see $$\sigma_y|_{\bar\varepsilon_p=0}=\sigma_0$$. The derivative is

$$
\dfrac{\mathrm{d}\sigma_y}{\mathrm{d}\bar\varepsilon_p}=\sigma_0\sum_{i=1}^{n}ia_i\bar\varepsilon_p^{i-1}
$$

To define such a hardening behavior, a vector shall be used to store all constants.

```cpp
// PolyJ2.h
const vec poly_para; // poly_para is a vector stores a_i
```

The methods could be written as follows.

```cpp
// PolyJ2.cpp
double PolyJ2::compute_k(const double p_strain) const {
 vec t_vec(poly_para.n_elem);

 t_vec(0) = 1.;
 for(uword I = 1; I < t_vec.n_elem; ++I) t_vec(I) = t_vec(I - 1) * p_strain;

 return yield_stress * dot(poly_para, t_vec);
}

double PolyJ2::compute_dk(const double p_strain) const {
 vec t_vec(poly_para.n_elem);

 t_vec(0) = 0.;
 t_vec(1) = 1.;
 for(uword I = 2; I < t_vec.n_elem; ++I) t_vec(I) = (double(I) + 1.) * pow(p_strain, double(I));

 return yield_stress * dot(poly_para, t_vec);
}
```

## Example

A few different models are shown as examples. User can define arbitrary models.
