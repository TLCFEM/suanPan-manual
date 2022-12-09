# GeneralizedAlpha

The generalized-$$\alpha$$ method provides second order accuracy with controllable algorithmic damping on high frequency
response.

## Syntax

Two forms are available.

```
integrator GeneralisedAlpha (1) [2]
integrator GeneralizedAlpha (1) [2]
# (1) int, unique tag
# [2] double, spectral radius at infinite frequency, default: 0.5

integrator GeneralisedAlpha (1) (2) (3)
integrator GeneralizedAlpha (1) (2) (3)
# (1) int, unique tag
# (2) double, \alpha_f
# (3) double, \alpha_m
```

## Governing Equation

The generalized alpha method assumes that the displacement $$d$$ and the velocity $$v$$ are integrated as such,

$$
d_{n+1}=d_n+\Delta{}tv_n+\Delta{}t^2\left(\left(\dfrac{1}{2}-\beta\right)a_n+\beta{}a_{n+1}\right)
,
$$

$$
v_{n+1}=v_n+\Delta{}t\left(1-\gamma\right)a_n+\Delta{}t\gamma{}a_{n+1}.
$$

The equation of motion is expressed at somewhere between $$t_n$$ and $$t_{n+1}$$.

$$
Ma_{n+1-\alpha_m}+Cv_{n+1-\alpha_f}+Kd_{n+1-\alpha_f}=F_{n+1-\alpha_f},
$$

which can also be explicitly shown as

$$
M\left(\left(1-\alpha_m\right)a_{n+1}+\alpha_ma_n\right)+C\left(\left(1-\alpha_f\right)v_{n+1}+\alpha_fv_n\right)
+K\left(\left(1-\alpha_f\right)d_{n+1}+\alpha_fd_n\right)=\left(1-\alpha_f\right)F_{n+1}+\alpha_fF_n,
$$

where $$\alpha_m$$ and $$\alpha_f$$ are two additional parameters.

## Default Parameters

To obtain an unconditionally stable algorithm, the following conditions shall be satisfied.

$$
\alpha_m\le\alpha_f\le\dfrac{1}{2},\quad\beta\ge\dfrac{1}{4}+\dfrac{1}{2}\left(\alpha_f-\alpha_m\right).
$$

Only one parameter is required, the spectral radius $$\rho_\infty$$ that ranges from zero to one.

The following expressions are used to determine the values of all constants used.

$$
\alpha_f=\dfrac{\rho_\infty}{\rho_\infty+1},\quad \alpha_m=\dfrac{2\rho_\infty-1}{\rho_\infty+1},\quad
\gamma=\dfrac{1}{2}-\dfrac{\rho_\infty-1}{\rho_\infty+1},\quad \beta=\dfrac{1}{\left(\rho_\infty+1\right)^2}.
$$

So that the resulting algorithm is unconditionally stable and has a second order accuracy. The target numerical damping
for high frequencies is achieved while that of low frequencies is minimized.

The recommended values of the spectral radius $$\rho_\infty$$ range from $$0.5$$ to $$0.8$$.

Some special parameters can be chosen.

| $$\alpha_f$$ | $$\alpha_M$$ | method         |
|--------------|--------------|----------------|
| $$0.0$$      | $$0.0$$      | Newmark        |
| -            | $$0.0$$      | HHT-$$\alpha$$ |
| $$0.0$$      | -            | WBZ-$$\alpha$$ |