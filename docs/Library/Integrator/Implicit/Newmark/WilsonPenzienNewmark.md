# WilsonPenzienNewmark

The `WilsonPenzienNewmark` incorporates the Wilson-Penzien damping model.

**For the moment, MPC cannot be considered in all global damping models.**

## Syntax

```
integrator WilsonPenzienNewmark (1) (2) (3) [4...]
# (1) int, unique integrator tag
# (2) double, alpha (beta in some references) in Newmark method, normally 0.25
# (3) double, beta (gamma in some references) in Newmark method, normally 0.5
# [4...] double, damping ratios on the first n modes
```

## Theory

The Wilson-Penzien damping model is defined by using global mode shapes. For the generalized eigenvalue problem, the
natural frequencies $$\omega$$ and mode shapes $$\mathbf{\phi}$$ are defined to be

$$
\mathbf{K\phi}=\omega^2\mathbf{M\phi}.
$$

The damping matrix is defined to be

$$
\mathbf{C}=\mathbf{\theta{}D}\mathbf{\theta}^\mathrm{T},
$$

where $$\mathbf{D}$$ is the diagonal matrix with diagonal entries to be $$\dfrac{2\xi_n\omega_n}{M_n}$$, and
$$\mathbf{\theta}=\mathbf{M\phi}$$.

However, the damping matrix is not explicitly formed, since $$\mathbf{C}$$ is fully populated while $$\mathbf{K}$$ and
$$\mathbf{M}$$ may be stored in a banded or even sparse scheme.

## Implementation

In order to implement the algorithm, the Woodbury identity is utilized. The global solving equation is

$$
\mathbf{K}_e\mathbf{\Delta{}U}=\mathbf{R},
$$

with $$\mathbf{K}_e=\mathbf{K}+c_0\mathbf{M}+c_1\mathbf{C}$$ to be the effective stiffness matrix. By denoting
$$\mathbf{K}+c_0\mathbf{M}+c_1\mathbf{C}_v$$ to be $$\mathbf{\bar{K}}$$, then

$$
\mathbf{K}_e\mathbf{\Delta{}U}=(\mathbf{\bar{K}}+c_1\mathbf{C})\mathbf{\Delta{}U}=\mathbf{R},
$$

$$
\mathbf{\Delta{}U}=(\mathbf{\bar{K}}+\mathbf{\theta{}}\mathbf{\bar{D}}\mathbf{\theta}^\mathrm{T})^{-1}\mathbf{R},
$$

where $$\mathbf{\bar{D}}=c_1\mathbf{D}$$. Note $$c_0$$ and $$c_1$$ are the corresponding parameters used in Newmark
algorithm. Note $$\mathbf{C}_v$$ is used to denote the additional viscous damping effect due to viscous devices such as
dampers. This part does not contribute the formulation of global damping matrix.

By using the Woodbury identity, one could obtain

$$
\mathbf{\Delta{}U}=(\mathbf{\bar{K}}+\mathbf{\theta{}}\mathbf{\bar{D}}\mathbf{\theta}^\mathrm{T})
^{-1}\mathbf{R},
$$

$$
\mathbf{\Delta{}U}=(\mathbf{\bar{K}}^{-1}-\mathbf{\bar{K}}^{-1}\mathbf{\theta{}}(
\mathbf{\bar{D}}^{-1}+\mathbf{\theta}^\mathrm{T}\mathbf{\bar{K}}^{-1}\mathbf{\theta})
^{-1}\mathbf{\theta}^\mathrm{T}\mathbf{\bar{K}}^{-1})\mathbf{R}.
$$

Note $$\mathbf{\bar{D}}^{-1}$$ can be conveniently formulated as it is simply a diagonal matrix.

The above formula requires two additional function calls to matrix solver. If the factorization can be stored, this
reduces to two backward substitutions.
