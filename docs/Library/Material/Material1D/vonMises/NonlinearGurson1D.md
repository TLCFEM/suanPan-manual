# NonlinearGurson1D

Uniaxial Nonlinear General Gurson Porous Model

## Theory

The yield function, hardening rule, flow rule are identical to those of the 3D version.
Please check the [`NonlinearGurson`](../../Material3D/vonMises/NonlinearGurson.md) model for details.

See also the corresponding section in [Constitutive Modelling Cookbook](https://github.com/TLCFEM/constitutive-modelling-cookbook/releases/download/latest/COOKBOOK.pdf).

The uniaxial version assumes the stress tensor possesses the following Voigt form.

$$
\sigma=\begin{bmatrix}\sigma_1&0&0&0&0&0\end{bmatrix},
$$

meaning that the elastic strain $$\varepsilon^e$$ is always

$$
\varepsilon^e=\varepsilon_1^e\begin{bmatrix}1&-\nu&-\nu&0&0&0\end{bmatrix},
$$

where $$\nu$$ is Poisson's ratio.

### Stress State and Yield Function

With only $$\sigma_1$$ nonzero, the hydrostatic stress and the von Mises equivalent stress reduce to

$$
p=\dfrac{\sigma_1}{3},\qquad q=|\sigma_1|,\qquad s=\dfrac{\sigma_1}{3}\begin{bmatrix}2&-1&-1&0&0&0\end{bmatrix}.
$$

Substituting these into the three-dimensional Gurson criterion gives the one-dimensional yield function

$$
\Phi=\sigma_1^2+\sigma_y^2\left[2q_1f\cosh\left(\dfrac{q_2\sigma_1}{2\sigma_y}\right)-q_1^2f^2-1\right]=0,
$$

where $$f$$ is the void volume fraction, $$\sigma_y(\varepsilon_m^p)$$ is the matrix yield stress and $$\varepsilon_m^p$$ is the matrix equivalent plastic strain.
The constants $$q_1$$ and $$q_2$$ are the Tvergaard correction factors and the quadratic term uses $$q_3=q_1^2$$.
Setting $$q_1=q_2=1$$ recovers the original Gurson criterion, while $$q_1=0$$ removes the hydrostatic sensitivity and recovers von Mises plasticity.
The bulk modulus used in the volumetric part is $$K=E/[3(1-2\nu)]$$.

!!! warning "implementation limitation"
    The coefficient of the $$f^2$$ term is fixed to $$q_3=q_1^2$$ and cannot be set independently.
    Only the uniaxial stress state $$\sigma_2=\sigma_3=0$$ is represented, so multiaxial triaxiality effects cannot be prescribed directly.

!!! note "developer note"
    The matrix hardening law is not defined in this class but must be supplied by a derived class.

### Flow Rule and Damage Evolution

The associated flow rule gives the axial plastic strain increment and the plastic volumetric increment,

$$
\Delta\varepsilon_1^p=\Delta\gamma\left[2\sigma_1+q_1q_2f\sigma_y\sinh\left(\dfrac{q_2\sigma_1}{2\sigma_y}\right)\right],
$$

$$
\Delta\varepsilon_v^p=3q_1q_2f\Delta\gamma\,\sigma_y\sinh\left(\dfrac{q_2\sigma_1}{2\sigma_y}\right)=\dfrac{\sigma_1^\text{tr}-\sigma_1}{3K}.
$$

Plastic work equivalence defines the evolution of the matrix equivalent plastic strain,

$$
\left(1-f\right)\sigma_y\Delta\varepsilon_m^p=\sigma:\Delta\varepsilon^p=\Delta\gamma\left[2\sigma_1^2+q_1q_2f\sigma_1\sigma_y\sinh\left(\dfrac{q_2\sigma_1}{2\sigma_y}\right)\right].
$$

The void fraction grows by both growth of existing voids and strain-controlled nucleation,

$$
\Delta f=\Delta f_g+\Delta f_n,\qquad \Delta f_g=(1-f)\Delta\varepsilon_v^p,\qquad \Delta f_n=A_N\Delta\varepsilon_m^p,
$$

with the normal nucleation distribution

$$
A_N=\dfrac{f_N}{s_N\sqrt{2\pi}}\exp\left[-\dfrac{1}{2}\left(\dfrac{\varepsilon_m^p-\varepsilon_N}{s_N}\right)^2\right].
$$

Here $$f_N$$ is the total nucleated void fraction, $$s_N$$ its standard deviation and $$\varepsilon_N$$ the mean nucleation strain.
There is no void coalescence term in this implementation.

!!! warning "implementation limitation"
    The standard Gurson--Tvergaard--Needleman model adds a coalescence acceleration once the void fraction exceeds a critical value.
    This implementation stops at growth and nucleation, and there is no fracture or element-deletion criterion.
    The void fraction is clamped to $$[0,1]$$ after each Newton update to prevent overshoot.

### Implicit Integration

The return mapping treats the plastic multiplier $$\gamma$$, the matrix equivalent plastic strain $$\varepsilon_m^p$$, the void fraction $$f$$ and the axial stress $$\sigma_1$$ as unknowns.
The four residuals solved by Newton iteration are

$$
\begin{aligned}
R_1&=\sigma_1^2+\sigma_y^2\left[2q_1f\cosh\left(\dfrac{q_2\sigma_1}{2\sigma_y}\right)-q_1^2f^2-1\right],\\
R_2&=(1-f)\sigma_y\left(\varepsilon_m^p-\varepsilon_{m,n}^p\right)-2\gamma\sigma_1^2+\dfrac{\sigma_1\left(\sigma_1-\sigma_1^\text{tr}\right)}{9K},\\
R_3&=f-f_n+(1-f)\dfrac{\sigma_1-\sigma_1^\text{tr}}{3K}-A_N\left(\varepsilon_m^p-\varepsilon_{m,n}^p\right),\\
R_4&=\sigma_1-\sigma_1^\text{tr}+9K\gamma q_1q_2f\sigma_y\sinh\left(\dfrac{q_2\sigma_1}{2\sigma_y}\right).
\end{aligned}
$$

The hardening pair $$(\sigma_y,\mathrm{d}\sigma_y/\mathrm{d}\varepsilon_m^p)$$ is supplied by the derived class.
The consistent tangent is obtained by solving the Jacobian once more with the derivative of the residuals with respect to the trial strain as the right-hand side.

!!! note "developer note"
    The first iteration tests the yield function with the trial stress and returns immediately with an elastic answer if it is negative.
    The Newton loop is capped at 20 iterations and returns a failure code if the system does not converge.
    A single four-by-four linear solve is used per iteration, so a singular Jacobian terminates the step.

## Remarks

The Poisson's ratio must stay below 0.5 for a finite bulk modulus.
With the default $$f_N=0$$ and a zero initial void fraction, no voids nucleate or grow and the response reduces to ordinary von Mises plasticity.
A nonzero initial void fraction can be prescribed with the [`initial`](../../../../Collection/Define/initial.md) `material history` command.
The void fraction is clamped to the interval $$[0,1]$$ after every Newton update.
Typical calibrated values are $$q_1\approx1.5$$ and $$q_2\approx1$$, although both default to unity here.
Damage is recorded through the `VF` output type below, and there is no built-in element deletion or fracture criterion.
The four-unknown Newton system requires a reasonable step size, so reduce the increment if convergence fails.
For the exponential matrix hardening law use [`ExpGurson1D`](ExpGurson1D.md), and for a user-defined law use [`CustomGurson1D`](CustomGurson1D.md).
The full three-dimensional formulation is available as [`NonlinearGurson`](../../Material3D/vonMises/NonlinearGurson.md).

## References

1. [10.1115/1.3443401](https://doi.org/10.1115/1.3443401)
2. [10.1016/0001-6160(84)90213-X](https://doi.org/10.1016/0001-6160(84)90213-X)

## Recording

This model supports the following additional history variables to be recorded.

| variable label | physical meaning |
|----------------|------------------|
| VF             | volume fraction  |
