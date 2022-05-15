# NonlinearDruckerPrager

Drucker-Prager Material Model

The Drucker-Prager model use the following function as the yield surface.

$$
F(\sigma,c)=\sqrt{J_2}+\eta_yp-\xi{}c
$$

in which $$J_2=\dfrac{1}{2}s:s$$ is the second invariant of stress $$\sigma$$, $$p=\dfrac{1}{3}(
\sigma_1+\sigma_2+\sigma_3)$$ is the hydrostatic stress, $$c(\bar{\varepsilon_p})$$ is cohesion, $$\eta_y$$ and $$\xi$$
are material constants.

Either associated or non-associated flow rule can be applied. The flow potential is defined as

$$
\Phi(\sigma,c)=\sqrt{J_2}+\eta_fp
$$

with $$\eta_f$$ is another material constant. If $$\eta_f=\eta_y$$, the associative plasticity is defined so that the
symmetry of stiffness matrix is recovered.

## History Variable Layout

| location             | parameter                  |
|----------------------|----------------------------|
| `initial_history(0)` | accumulated plastic strain |

## Decision of Material Constants

There are quite a lot of schemes to determine the material constants used in Drucker-Prager model. Here a few are
presented.

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

### Concrete, Rock, etc

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
