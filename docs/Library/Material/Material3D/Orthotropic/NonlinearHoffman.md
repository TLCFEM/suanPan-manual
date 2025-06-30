# NonlinearHoffman

Orthotropic Hoffman Material

## References

1. [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook/releases/download/latest/COOKBOOK.pdf)

## Theory

The `NonlinearHoffman` defines an orthotropic material using Hoffman yield criterion and associative plasticity.

The yield surface is defined as

$$
\begin{multline} F(\sigma,\bar\varepsilon_p)=C_1(\sigma_{11}-\sigma_{22})^2+C_2(\sigma_{22}-\sigma_{33})^2+C_3(
\sigma_{33}-\sigma_{11})^2+\\[4mm]
C_4\sigma_{12}^2+C_5\sigma_{23}^2+C_6\sigma_{13}^2+C_7\sigma_{11}+C_8\sigma_{22}+C_9\sigma_{33}-K^2(\bar\varepsilon_p)
\end{multline}
$$

with $$\sigma=[\sigma_{11}~\sigma_{22}~\sigma_{33}~\sigma_{12}~\sigma_{23}~\sigma_{13}]^\mathrm{T}$$ is the stress,
$$C_1$$ to $$C_9$$ are material constants. $$K(\bar\epsilon_p)$$ is the isotropic hardening function.

The constants are defined as follows.

$$
\begin{align*} C_1&=\dfrac{1}{2}(\dfrac{1}{\sigma_{11}^t\sigma_{11}^c}+\dfrac{1}{\sigma_{22}^t\sigma_
{22}^c}-\dfrac{1}{\sigma_{33}^t\sigma_{33}^c}),\\[4mm]
C_2&=\dfrac{1}{2}(\dfrac{1}{\sigma_{22}^t\sigma_{22}^c}+\dfrac{1}{\sigma_{33}^t\sigma_{33}^c}-\dfrac{1}{\sigma_
{11}^t\sigma_{11}^c}),\\[4mm]
C_3&=\dfrac{1}{2}(\dfrac{1}{\sigma_{33}^t\sigma_{33}^c}+\dfrac{1}{\sigma_{11}^t\sigma_{11}^c}-\dfrac{1}{\sigma_
{22}^t\sigma_{22}^c}),\\[4mm]
C_4&=\dfrac{1}{\sigma_{12}^0\sigma_{12}^0},\quad{}C_5=\dfrac{1}{\sigma_{23}^0\sigma_{23}^0},\quad{}C_6=\dfrac{1}{\sigma_
{13}^0\sigma_{13}^0},\\[4mm]
C_7&=\dfrac{\sigma_{11}^c-\sigma_{11}^t}{\sigma_{11}^t\sigma_{11}^c},\quad{}C_8=\dfrac{\sigma_{22}^c-\sigma_
{22}^t}{\sigma_{22}^t\sigma_{22}^c},\quad{}C_9=\dfrac{\sigma_{33}^c-\sigma_{33}^t}{\sigma_{33}^t\sigma_{33}^c}.
\end{align*}
$$

The Hoffman function allows different yield stresses for tension and compression. To recover the original Hill yield
function, simply set $$\sigma_{ii}^t=\sigma_{ii}^c$$ for $$i=1,~2,~3$$.

The hardening function $$K(\bar\varepsilon_p)$$ can be user defined. It shall be noted that $$K(0)=1$$. The following
method shall be implemented.

```cpp
virtual double compute_k(double) const = 0;
virtual double compute_dk(double) const = 0;
```

## History Layout

| location               | parameter                 |
|------------------------|---------------------------|
| `initial_history(0)`   | equivalent plastic strain |
| `initial_history(1:7)` | plastic strain            |
