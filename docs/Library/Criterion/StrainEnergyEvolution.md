# StrainEnergyEvolution

This `StrainEnergyEvolution` criterion implements the BSEO Method. It can be used in structural optimization. To define
one,

```
criterion StrainEnergyEvolution (1) (2) (3) [4] [5] [6] [7] [8]
# (1) int, unique criterion tag
# (2) int, increment of rejection level in percentage
# (3) int, target rejection level in percentage
# [4] double, weight of central element, used in averaging
# [5] int, number of iterations of averaging
# [6] int, reactivation rate in percentage
# [7] double, propagation weight
# [8] double, tolerance
```

## Caveat

1. It is recommended to use consecutive tags for elements starting from $$1$$. Large tags will increase memory usage.

## Theory

Readers can refer to the
monograph [Evolutionary Topology Optimization of Continuum Structures: Methods and Applications](https://doi.org/10.1002/9780470689486)
for detailed discussion of the **Bi-directional Evolutionary Structural Optimization Method**.

Here a brief introduction is presented to explain what the `StrainEnergyEvolution` criterion does to the model.

To perform optimization with `StrainEnergyEvolution`, a `Optimization` step shall be defined instead of a standard
static step.

```
step Optimization (1) [2]
# (1) int, unique step tag
# [2] double, step length, default: 1.0
```

The `ESO` step performs the complete static analysis step and calls the criterion to modify/update the model repeatedly
until an exit signal is received. The exit signal is often returned by a proper `criterion`.

### Collect Strain Energy

The first step is to collect the normalized strain energy of each element. If the element is currently inactive, the
corresponding strain energy will be set to zero. The normalization uses the characteristic length of the corresponding
element.

### Averaging

Instead of the original node based averaging procedure, which requires to compute the sensitivity parameter of the
connected nodes, the `StrainEnergyEvolution` criterion uses a *convolution filter* type process. The averaged strain
energy is updated by computing the weighted average of the strain energy of all connected elements. Say the target
element, denoted with subscript $$j$$, is connected to $$m=n-1$$ elements. Accounting for the target element itself,
there are $$n$$ elements under consideration. The strain energy of each element before averaging is denoted by
$$\alpha_i$$. Then the averaged strain energy of that element $$\bar\alpha$$ can be computed by

$$
\bar\alpha_j=\sum^{n}_{i=1}w_i\alpha_i,\qquad{}w_j=Ww_i\quad\text{for }i\neq{}j,\qquad\sum^{n}_{i=1}w_i=1.
$$

The parameter $$W$$ is controlled by the fourth input argument `[4]`.

For the above averaging process, each element can affect the adjacent elements, resulting in a smoothed distribution of
strain energy. Such a process can be repeated several times to further average the result. The number of the averaging
process is controlled by the fifth input argument `[5]`.

### Stabilization

Collect all averaged strain energy into a vector and denote it with $$\mathbf{\alpha}^k$$, it is stabilized by
considering the strain energy of the previous iteration $$\mathbf{\alpha}^{k-1}$$,

$$
\mathbf{\alpha}^k\leftarrow\left(1-w_p\right)\mathbf{\alpha}^{k-1}+w_p\dfrac{1}{2}\mathbf{\alpha}^k.
$$

So even if some elements are deleted in the current iteration by accident, they can be added back to the model in the
next iteration as the stabilized $$\mathbf{\alpha}^k$$ now has some memory. The parameter $$w_p$$ is controlled by input
parameter `[7]`.

### Addition/Deletion of Elements

The rejection ratio starts from zero with an increment of $$\Delta{}r$$ till reaching the target rejection ratio $$r_
{target}$$ and then stays unchanged. The increment $$\Delta{}r$$ is controlled by parameter `(2)` and the rejection
ratio $$r_{target}$$ is controlled by parameter `(3)`.

For the current rejection ratio $$r$$, $$r\%$$ of total elements will be removed in the current iteration. However,
before removing any elements, some already removed elements will be added first, called reactivation. The number of
reactivated elements is controlled by the reactivation ratio $$r_a$$, which is parameter `[6]`. So $$r_a\%$$ of already
removed elements will be added to the model.

After reactivation, the number of active elements is the sum of numbers of reactivated elements and already active
elements.

The averaged strain energy of all active elements will be sorted to determine which elements shall be removed. The
number of removed elements is the difference of current number of active elements and the current rejection ratio.

### Convergence

The convergence is achieved when the relative energy difference between two adjacent iterations is smaller than the
tolerance, which is controlled by parameter `[8]`.