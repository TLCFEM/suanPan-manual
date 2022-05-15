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

Any sections shall take the above deformation vector as input and produce the corresponding force conjugates as the
output.
