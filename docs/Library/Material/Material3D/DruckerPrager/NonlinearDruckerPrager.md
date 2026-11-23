# NonlinearDruckerPrager

Drucker-Prager Material Model

The Drucker-Prager model uses the following function as the yield surface.

$$
F(\sigma,c)=\sqrt{J_2}+\eta_yp-\xi{}c
$$

in which $$J_2=\dfrac{1}{2}s:s$$ is the second invariant of stress $$\sigma$$, $$p=\dfrac{1}{3}(\sigma_1+\sigma_2+\sigma_3)$$ is the hydrostatic stress, $$c(\bar{\varepsilon_p})$$ is cohesion, $$\eta_y$$ and $$\xi$$ are material constants.

Either associated or non-associated flow rule can be applied.
The flow potential is defined as

$$
\Phi(\sigma,c)=\sqrt{J_2}+\eta_fp
$$

where $$\eta_f$$ is another material constant.
If $$\eta_f=\eta_y$$, the associative plasticity is defined so that the symmetry of stiffness matrix is recovered.

The accumulated plastic strain $$\bar{\varepsilon_p}$$ is defined as

$$
\dot{\bar{\varepsilon_p}}=\xi\gamma,
$$

where $$\gamma$$ is the plasticity multiplier.

## History Variable Layout

| location             | parameter                  |
|----------------------|----------------------------|
| `initial_history(0)` | accumulated plastic strain |

## Determination of Material Constants

There are quite a lot of schemes to determine the material constants used in Drucker-Prager model.
Here a few are presented.

### Geomaterials

The friction angle $$\phi$$ and initial cohesion $$c_0$$ shall be determined by experiments.

#### Outer Mohr-Coulomb

$$
\eta_y=\dfrac{6\sin\phi}{\sqrt{3}(3-\sin\phi)},\qquad\xi=\dfrac{6\cos\phi}{\sqrt{3}(3-\sin\phi)}
$$

#### Inner Mohr-Coulomb

$$
\eta_y=\dfrac{6\sin\phi}{\sqrt{3}(3+\sin\phi)},\qquad\xi=\dfrac{6\cos\phi}{\sqrt{3}(3+\sin\phi)}
$$

#### Plane Strain Fitting

$$
\eta_y=\dfrac{3\tan\phi}{\sqrt{9+12\tan^2\phi}},\qquad\xi=\dfrac{3}{\sqrt{9+12\tan^2\phi}}
$$

### Concrete, Rock, etc.

To fit uniaxial tension and compression strength, the friction angle and cohesion shall be computed as

$$
\phi=\sin^{-1}\dfrac{f_c-f_t}{f_c+f_t},\qquad{}c=\dfrac{f_cf_t}{f_c-f_t}\tan\phi
$$

in which $$f_t\ge0$$ and $$f_c\ge0$$ are tension and compression strength respectively.

#### Uniaxial Tension/Compression

$$
\eta_y=\dfrac{3\sin\phi}{\sqrt{3}},\qquad\xi=\dfrac{2\sin\phi}{\sqrt{3}}
$$

#### Biaxial Tension/Compression

$$
\eta_y=\dfrac{3\sin\phi}{2\sqrt{3}},\qquad\xi=\dfrac{2\sin\phi}{\sqrt{3}}
$$

## Implementation

The class is the abstract base of the Drucker--Prager family and is not registered as a `material` token.
The instantiable variants are [`BilinearDP`](BilinearDP.md), [`ExpDP`](ExpDP.md) and [`CustomDP`](CustomDP.md), which supply the cohesion function $c(\bar\varepsilon_p)$ and its derivative.
The elastic trial stress uses the isotropic stiffness with $G=E/[2(1+\nu)]$ and $K=E/[3(1-2\nu)]$, and the trial yield value is $\sqrt{J_2}+\eta_y p$.

The return mapping solves a scalar consistency equation for the plastic multiplier $\gamma$,

$$
\sqrt{J_2}+\eta_y p-\left(G+K\eta_f\eta_y\right)\gamma-\xi\,c(\bar\varepsilon_p)=0,
$$

so the effective plastic slope is $G+K\eta_f\eta_y$.
The accumulated plastic strain is $\bar\varepsilon_p=\xi\gamma$, and the Newton update divides the residual by $G+K\eta_f\eta_y+\xi^2\,\mathrm{d}c/\mathrm{d}\bar\varepsilon_p$.
When $\eta_f=\eta_y$ the plastic potential equals the yield function and the consistent tangent is symmetric; otherwise the plastic part of the tangent is nonsymmetric and a nonsymmetric solver is advisable.
The parameter $\eta_f$ controls the dilatancy independently of the yield strength: $\eta_f=\eta_y$ gives associative flow, while $|\eta_f|<|\eta_y|$ gives a weaker volumetric response.
A separate apex-return branch is used when $\sqrt{J_2}$ is too small to complete the radial correction; in that branch the stress is hydrostatic.
There is no independent tension-cutoff surface, so the apex of the cone is the only tension limit.

!!! info "deviation from theory"
    Classical plasticity often measures hardening against the equivalent plastic strain $\sqrt{2\Delta\boldsymbol\varepsilon^p:\Delta\boldsymbol\varepsilon^p/3}$.
    This implementation instead accumulates $\bar\varepsilon_p=\xi\gamma$, so the cohesion slope must be calibrated against this scaled internal variable.

!!! note "developer note"
    The consistency slope is $G+K\eta_f\eta_y$, so the pressure coupling enters the plastic multiplier directly.

!!! warning "implementation limitation"
    The cone has no compression cap, and no Rankine tension cutoff is available.

!!! note "developer note"
    The apex-return branch handles the singular radial correction but does not add a tensile strength limit.

The Drucker--Prager cone has a circular deviatoric section and therefore ignores the Lode angle.
The "outer Mohr--Coulomb" fitting chooses the circle through the compression corners of the Mohr--Coulomb hexagon, while the "inner" fitting passes through the tension corners.
The outer fit overestimates the shear strength for general stress states, whereas the inner fit is conservative.
The plane-strain fitting listed above is the intermediate choice that reproduces the Mohr--Coulomb strength for plane-strain conditions.
For frictional materials $\phi$ and $c_0$ should come from triaxial or direct shear tests; for concrete and rock they may instead be back-computed from the uniaxial tensile and compressive strengths with the relations given above.

## Remarks

- The sign convention is tension positive, so $p$ is negative in compression and $\eta_y$ and $\xi$ are entered as positive numbers.
- Setting $\eta_y=\eta_f=0$ recovers the von Mises criterion with associative flow, as detailed on the [`BilinearDP`](BilinearDP.md) page.
- No material density or extra options are parsed by this base class; each derived model adds its own arguments, with density defaulting to zero.
- The yield function is linear in $p$ and $\sqrt{J_2}$, so the yield surface is a right circular cone with no cap on the compression side.
- Hardening or softening affects only the cohesion intercept through $c(\bar\varepsilon_p)$; the friction coefficient $\eta_y$ stays constant.
- Continuous softening to zero cohesion leaves a frictional cone through the origin, which is the expected residual-strength state for many geomaterials.
- The local Newton iteration is limited to 20 steps and reports a failure if convergence is not reached.
- No additional history variables are recorded by this class; use the derived models or the [`Substepping`](../../Wrapper/Substepping.md) wrapper if a smaller load step is needed during rapid hardening.

## References

1. Mechanics of thermo-elastic-plastic materials with a thermoelastic-plastic change in
2. [ISBN 978-1-932159-75-2](https://search.worldcat.org/search?q=bn:9781932159752)
3. [10.1016/j.mechrescom.2011.04.001](https://doi.org/10.1016/j.mechrescom.2011.04.001)
