# Beam Element Overview

## Local CS

The beam section possesses a local coordinate system that differs from the global coordinate system. The local
$$x$$-axis is aligned with beam cord. Strong axis is represented by local $$z$$-axis while weak axis is represented by
local $$y$$-axis. The local $$xyz$$ axes form a right-handed coordinate system.

## Orientation

For 2D beams, it is assumed that local $$z$$-axis coincides with global $$z$$-axis so that there is no need to
explicitly define any orientation for 2D beams.

For 3D beams, local $$z$$-axis shall be defined in the associated section orientation.

## Local Deformation

The local deformation vector consists of six components, namely,

$$
\mathbf{d}=\begin{bmatrix} u&\theta_{zi}&\theta_{zj}&\theta_{yi}&\theta_{yj}&\theta_{xj}-\theta_{xi} \end{bmatrix}.
$$

They correspond to axial elongation, strong axis rotation at first and second node, weak axis rotation at first and
second node, and torsion rotation.

For 2D beams, only the first three are present.

Any sections shall take the above deformation vector **over element length**, that is,

$$
\mathbf{d}/L
$$

as input and produce the corresponding force conjugates (section resistance) as the output. Please note the 
deformation vector is normalised by element length. This offers some convenience so that sections are independent 
of element properties. The same section can be used for different elements with different element lengths.

## Which Element To Be Used?

A few different general purpose beam elements are available.

### Displacement Based

The [`B21`](B21.md) and [`B31`](B31.md) are classic Bernoulli beam elements, which are probably the first beam 
elements introduced in any FEM textbooks. They are displacement based elements, meaning that the displacement 
profile along beam chord always follows the Hermite polynomial. This is fine for elastic analysis but may not be 
suitable for plastic analysis. The nonlinear response is often over stiff. Accuracy can be improved by mesh 
refinement, but it appears a bit cumbersome to define multiple elements within the same span/floor with interior 
nodes do not connect additional frames.

To model hinge connection at one of two ends, one can use [`B21E`](B21E.md) so that either the first or the second 
end has zero moment. To specify the explicit plastic hinge length, one can use [`B21H`](B21H.md). Plasticity is only 
allowed at ends with a fixed length while the interior remains elastic.

### Force Based

The force based beam elements appear to be superior in all cases. This category includes [`F21`](F21.md) and 
[`F31`](F31.md) elements. The moment distribution along beam chord is always linear in absence of distributed load. It 
is shown that force based elements result in less error with the same number of integration points, and converges 
faster with increasing number of integration points, see [`this paper`](https://doi.org/10.1061/(ASCE)0733-9445(1997)123:7(958)).

Typically, five to seven integration points would be sufficient for each element. Mesh refinement is often not 
necessary and can be alternatively replaced by adding more integration points to a single element.

### Generalised Plasticity Based

Without using sections, it is possible to model nonlinear beams at element level. The [`NMB21`](NMB21.md) and 
[`NMB31`](NMB31.md) are two examples of generalised plasticity based beam elements. The efficiency of this type of 
elements is the best of the three as there are no sections, no integration points. Only local plasticity iterations 
are performed. The applicability mainly depends on the nonlinear behaviour of [`NMSection`](../../Section/SectionNM/SectionNM.md).
