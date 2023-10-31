# NonlinearGurson1D

Uniaxial Nonlinear General Gurson Porous Model

## Theory

The yield function, hardening rule, flow rule are identical to that of the 3D version. Please check the **
NonlinearGurson** model for details.

The uniaxial version assumes the stress tensor possesses the following voigt form.

$$
\sigma=\begin{bmatrix}\sigma_1&0&0&0&0&0\end{bmatrix},
$$

meaning that the elastic strain $$\varepsilon^e$$ is always

$$
\varepsilon^e=\varepsilon_1^e\begin{bmatrix}1&-\nu&-\nu&0&0&0\end{bmatrix},
$$

where $$\nu$$ is Poisson's ratio.

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning |
|----------------|------------------|
| VF             | volume fraction  |
