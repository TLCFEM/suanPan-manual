# Fibre3DOS

3D OS Fibre Section

## Reference

1. [Distributed plasticity analysis of steel building structural systems](https://www.proquest.com/dissertations-theses/distributed-plasticity-analysis-steel-building/docview/304696456/se-2)
2. [Analysis and Design of Elastic Beams: Computational Methods](https://doi.org/10.1002/9780470172667)

## Syntax

```
section Fibre3DOS (1) [(2)...]
# (1) int, unique section tag
# [(2)...] int, associated section tags
```

## Remarks

The associated sections need to be OS sections.

The section takes twelve quantities from the parent element, namely,

$$
\begin{bmatrix}
u'&v'&w'&v''&w''&\phi&\phi'&\phi''&\theta_{z,i}&\theta_{z,j}&\theta_{y,i}&\theta_{y,j}
\end{bmatrix}
$$

!!! Note
    All quantities ($$u$$, $$v$$, $$w$$ and $$\phi$$) are measured about the reference axis ($$y=z=0$$).
    Any offset/shift should be directly defined via section composition.

Then strain components are determined by the following equations:

$$
\begin{bmatrix}
\varepsilon_{11}\\
\gamma_{12}\\
\gamma_{13}
\end{bmatrix}=\begin{bmatrix}
u'-yv''-zw''+\omega\phi''+\left(zv''-yw''\right)\phi+\dfrac{1}{2}(y^2+z^2)\left(\phi'\right)
^2+\dfrac{1}{60}\mathbf{\theta}^\mathrm{T}\mathbf{X}\mathbf{\theta}\\
\left(\dfrac{\partial\omega}{\partial{}y}-z\right)\phi'\\
\left(\dfrac{\partial\omega}{\partial{}z}+y\right)\phi'
\end{bmatrix}
$$

The normal strain is defined according to Alemdar's thesis (Eq. 7.63).
The shear strains are defined according to Pilkey's book (Eq. 5.3).

Alemdar's thesis and its derivatives use $$\gamma=-2n\phi'$$ to define the shear strain.
This definition is acceptable for thin-walled sections, where a clear physical implication of parameter $$n$$ can be
found.
For arbitrary sections, such a definition would be problematic.
We use a general definition instead.
Then there are two shear components instead of one.
The remaining three strain components are zero.
The wrapper [`OS146`](../../Material/Wrapper/OS146.md) can be used to prepare compatible materials.

## Example

See [this](../../../Example/Structural/Statics/thin-walled-section.md) example.
