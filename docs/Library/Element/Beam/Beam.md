# Beam Element Overview

## Theory

A beam is a one-dimensional member whose transverse dimensions are small compared with its length, so that its state is described by resultants acting on the cross-section rather than by a full three-dimensional stress field.
Two classical kinematic theories appear in the beam finite element literature, and the beam elements documented here use Euler–Bernoulli kinematics.

### Euler–Bernoulli versus Timoshenko kinematics

In Euler–Bernoulli (Bernoulli) beam theory, a cross-section that is initially plane and normal to the neutral axis remains plane and normal to the deformed neutral axis.
Consequently the section rotation $\theta$ equals the slope of the deflection curve, $v'=\theta$, and the transverse shear strain vanishes, $\gamma=v'-\theta=0$.
The axial strain at a distance $y$ from the neutral axis is $\varepsilon_x=u'-y\,v''=u'-y\,\kappa$, where $\kappa=v''$ is the curvature and $u'$ is the axial strain of the centroidal axis.
For a linear elastic section this gives the resultants $N=EA\,u'$ and $M=EI\,\kappa$, with $E$ the elastic modulus, $A$ the area and $I$ the second moment of area.
The equilibrium equations of a prismatic beam under a distributed transverse load $q(x)$ are $N'=0$, $M'=V$ and $V'=-q$, where $V$ is the shear force.

In Timoshenko (Mindlin) beam theory the section rotation $\theta$ is an independent field and is not tied to the slope, so that $\gamma=v'-\theta\neq0$.
The shear force is then $V=\kappa_s GA\,\gamma$, where $G$ is the shear modulus and $\kappa_s$ is the shear correction factor accounting for the non-uniform shear stress over the section.
This additional compliance makes Timoshenko theory necessary for short or deep members and for sections with low transverse shear stiffness, whereas Euler–Bernoulli theory is adequate for slender members.

A two-node Euler–Bernoulli element interpolates the transverse deflection with cubic Hermite functions, so that the curvature is linear within the element and is exact only when the bending moment varies linearly.
In a displacement-based element this kinematic restriction makes the response overly stiff whenever curvature varies rapidly, and mesh refinement is needed to resolve plastic hinges.
A two-node Timoshenko element interpolates $v$ and $\theta$ with independent linear functions, which produces a constant shear strain over the element.
As the member becomes slender the true shear strain tends to zero, and the constant shear strain of the interpolation makes the shear energy dominate, so that the element locks.
This shear locking is avoided by reduced or selective integration, by assumed shear-strain fields, or by higher-order interpolation, as discussed by Malkus and Hughes and by Hughes.
None of the elements on this page contain a transverse shear deformation mode, so shear locking does not arise for them, but their cubic bending interpolation can still produce an overly stiff nonlinear response.

### Numerical integration: Gauss and Lobatto rules

Section resultants are evaluated at integration points along the element and assembled with $\mathbf K=\int_0^L\mathbf B^\mathrm T\mathbf D_s\mathbf B\,\mathrm dx\approx\sum_i\mathbf B_i^\mathrm T\mathbf D_{s,i}\mathbf B_i\,w_i$, where $\mathbf B_i$ maps nodal deformations to section strains, $\mathbf D_{s,i}$ is the section tangent stiffness and $w_i$ is the quadrature weight in physical coordinates.
An $n$-point Gauss–Legendre rule integrates polynomials of degree $2n-1$ exactly and places every point strictly inside the interval.
An $n$-point Lobatto rule integrates polynomials of degree $2n-3$ exactly and includes both end points $\xi=\pm1$ of the natural coordinate interval.
The displacement-based elements [`B21`](B21.md), [`B31`](B31.md) and [`B31OS`](B31OS.md) use Lobatto integration by default, which samples the two end sections where bending moments are largest and where hinges are most likely to form.
The elastic core of [`B21H`](B21H.md) uses a two-point Gauss rule instead, because only a constant-curvature contribution is required there.
The number of integration points controls where plasticity is sampled, so too few points can miss a localised plastic zone while too many points add cost without reducing the displacement interpolation error.

### Local deformations and section conjugation

Global nodal displacements are first transformed into a local deformation vector that contains only strain-like quantities, so that one section can be reused by elements of different lengths.
For a two-dimensional beam the six nodal DoFs $(U_1,U_2,UR_3)$ at the two ends reduce to $\mathbf d=\begin{bmatrix}u&\theta_{zi}&\theta_{zj}\end{bmatrix}$, where $u$ is the axial elongation and $\theta_{zi}$, $\theta_{zj}$ are the end rotations measured relative to the chord.
For a three-dimensional beam the twelve nodal DoFs reduce to $\mathbf d=\begin{bmatrix}u&\theta_{zi}&\theta_{zj}&\theta_{yi}&\theta_{yj}&\theta_{xj}-\theta_{xi}\end{bmatrix}$, adding weak-axis bending and the relative torsional rotation.
Here the local $x$-axis follows the chord, the local $z$-axis is the strong axis and the local $y$-axis is the weak axis, forming the right-handed triad described under [Local CS](#local-cs).
Sections receive the deformation vector divided by the element length, $\mathbf d/L$, and return the conjugate section forces, so that a section object is independent of the element length.
Work conjugacy gives $\delta W=\mathbf s^\mathrm T\delta(\mathbf d/L)\,L=\mathbf s^\mathrm T\delta\mathbf d$, which confirms that the returned forces are the axial force and bending moments, and that the warping conjugate in open sections is the bimoment.

### Displacement-based and force-based formulations

In a displacement-based element the displacement field is interpolated first and the section strains follow by differentiation, so the bending moment inherits the linear curvature of the Hermite interpolation.
In a force-based (mixed) element the section forces are interpolated instead, typically as a linear function of the natural coordinate in the absence of distributed load, and the section deformations follow from the section flexibility.
Because equilibrium is satisfied in the strong form, force-based elements need far fewer integration points for the same accuracy and converge faster as points are added, as shown by Spacone, Filippou and Taucer.
The force-based counterparts in suanPan are [`F21`](F21.md) and [`F31`](F31.md), for which five to seven integration points are usually sufficient.

### Corotational formulation

A corotational formulation separates a rigid-body motion from a small-strain deformation by attaching a local frame to the element chord and measuring all section strains in that frame.
For a two-dimensional beam the chord stretch is $u=L-L_0$ and the local end rotations are $\Theta_i=\theta_i+\beta_0-\beta$, where $L_0$ and $L$ are the initial and current chord lengths, $\beta_0$ and $\beta$ are the initial and current chord inclinations, and $\theta_i$ are nodal rotations.
For arbitrarily large rotations the difference is evaluated robustly via $\tan\Theta_i=\dfrac{\sin\theta_i\cos\beta-\cos\theta_i\sin\beta}{\cos\theta_i\cos\beta+\sin\theta_i\sin\beta}$, which avoids subtracting nearly equal angles.
The global resistance and consistent tangent follow from $\mathbf f=\mathbf B_l^\mathrm T\mathbf f_l$ and $\mathbf K=\mathbf B_l^\mathrm T\mathbf K_l\mathbf B_l+\sum_i f_{l,i}\,\partial^2\Theta_i/\partial\mathbf v^2$, where $\mathbf B_l$ maps global nodal displacements to local deformations and the second term is the geometric stiffness contribution.
The two- and three-dimensional corotational transformations in suanPan follow Crisfield's work with the modifications of de Souza, as summarised on the [`Orientation`](Orientation.md) page.
The mass matrix is deliberately not corotated, so it remains constant during the analysis.

!!! warning "implementation limitation"
    Because the mass matrix is not transformed with the corotational frame, the formulation is not energy preserving for large rotations and is mainly intended for earthquake-engineering applications.

### Membrane locking and warping of open sections

Thin-walled open sections such as I, channel and angle sections warp under torsion, so that the torsional response involves the St. Venant torque $T_{sv}=GJ\phi'$ together with the warping contribution $B=-EI_w\phi''$, where $\phi$ is the twist, $J$ is the torsional constant and $I_w$ is the warping constant.
The conjugates are the bimoment $B$ and the Wagner stress resultant, and the coupled torsion–warping stiffness is implemented in [`B31OS`](B31OS.md) and [`EB31OS`](EB31OS.md).
Interpolating the warping displacement with a low-order polynomial can introduce spurious constraints in thin-walled members and cause membrane locking.
The interpolation used by [`B31OS`](B31OS.md) adopts Hermite functions for the twist $\phi$, which removes this locking as reported by Alemdar.

## Local CS

The beam section possesses a local coordinate system that differs from the global coordinate system.
The local $$x$$-axis is aligned with beam chord.
Strong axis is represented by local $$z$$-axis while weak axis is represented by local $$y$$-axis.
The local $$xyz$$ axes form a right-handed coordinate system.

## Orientation

For 2D beams, it is assumed that local $$z$$-axis coincides with global $$z$$-axis so that there is no need to explicitly define any orientation for 2D beams.

For 3D beams, local $$z$$-axis shall be defined in the associated section orientation.

## Local Deformation

The local deformation vector consists of six components, namely,

$$
\mathbf{d}=\begin{bmatrix} u&\theta_{zi}&\theta_{zj}&\theta_{yi}&\theta_{yj}&\theta_{xj}-\theta_{xi} \end{bmatrix}.
$$

They correspond to axial elongation, strong axis rotation at first and second node, weak axis rotation at first and second node, and torsion rotation.

For 2D beams, only the first three are present.

Any sections shall take the above deformation vector **over element length**, that is,

$$
\mathbf{d}/L
$$

as input and produce the corresponding force conjugates (section resistance) as the output.
Please note the deformation vector is normalised by element length.
This offers some convenience so that sections are independent of element properties.
The same section can be used for different elements with different element lengths.

## Which Element To Be Used?

A few different general purpose beam elements are available.

### Displacement Based

The [`B21`](B21.md) and [`B31`](B31.md) are classic Bernoulli beam elements, which are probably the first beam elements introduced in any FEM textbooks.
They are displacement based elements, meaning that the displacement profile along beam chord always follows the Hermite polynomial.
This is fine for elastic analysis but may not be suitable for plastic analysis.
The nonlinear response is often overly stiff.
Accuracy can be improved by mesh refinement, but it appears a bit cumbersome to define multiple elements within the same span/floor with interior nodes that do not connect additional frames.

To model hinge connection at one of two ends, one can use [`B21E`](B21E.md) so that either the first or the second end has zero moment.
To specify the explicit plastic hinge length, one can use [`B21H`](B21H.md).
Plasticity is only allowed at ends with a fixed length while the interior remains elastic.

### Force Based

The force based beam elements appear to be superior in all cases.
This category includes [`F21`](F21.md) and [`F31`](F31.md) elements.
The moment distribution along beam chord is always linear in absence of distributed load.
It is shown that force based elements result in less error with the same number of integration points, and converges faster with increasing number of integration points, see [`this paper`](https://doi.org/10.1061/(ASCE)0733-9445(1997)123:7(958)).

Typically, five to seven integration points would be sufficient for each element.
Mesh refinement is often not necessary and can be alternatively replaced by adding more integration points to a single element.

### Generalised Plasticity Based

Without using sections, it is possible to model nonlinear beams at element level.
The [`NMB21`](NMB21.md) and [`NMB31`](NMB31.md) are two examples of generalised plasticity based beam elements.
The efficiency of this type of elements is the best of the three as there are no sections, no integration points.
Only local plasticity iterations are performed.
The applicability mainly depends on the nonlinear behaviour of [`NMSection`](../../Section/SectionNM/SectionNM.md).

## Remarks

The displacement-based elements [`B21`](B21.md) and [`B31`](B31.md) integrate a linear curvature and therefore tend to overpredict stiffness in nonlinear analyses, whereas [`F21`](F21.md) and [`F31`](F31.md) interpolate the force distribution instead.
The [`B31`](B31.md) element does not integrate torsion from the section and uses a large penalty stiffness instead, so use [`B31OS`](B31OS.md) when torsion or warping matters.

!!! info "deviation from theory"
    The penalty replaces the physically based torsional stiffness entirely, so the torsional deformation of [`B31`](B31.md) carries no St. Venant or warping stiffness and cannot represent torsional plasticity.

The constructors of [`B21`](B21.md), [`B31`](B31.md) and [`B31OS`](B31OS.md) cap the requested number of integration points at 20.
For purely elastic members use [`EB21`](EB21.md) or [`EB31OS`](EB31OS.md), which need no section definition and are assembled from closed-form stiffness matrices.

## References

1. T. J. R. Hughes, *The Finite Element Method: Linear Static and Dynamic Finite Element Analysis*, Dover Publications, 2000, ISBN 978-0-486-41181-1.
2. O. C. Zienkiewicz and R. L. Taylor, *The Finite Element Method*, 5th edition, Butterworth–Heinemann, 2000.
3. D. S. Malkus and T. J. R. Hughes, "Mixed finite element methods — reduced and selective integration techniques: a unification of concepts", *Computer Methods in Applied Mechanics and Engineering*, 15(1):63–81, 1978, [doi:10.1016/0045-7825(78)90013-0](https://doi.org/10.1016/0045-7825(78)90013-0).
4. E. Spacone, F. C. Filippou and F. F. Taucer, "Fibre beam-column model for non-linear analysis of R/C frames: Part I. Formulation", *Earthquake Engineering and Structural Dynamics*, 25(7):711–725, 1996, [doi:10.1002/(SICI)1096-9845(199607)25:7<711::AID-EQE576>3.0.CO;2-9](https://doi.org/10.1002/(SICI)1096-9845(199607)25:7%3C711::AID-EQE576%3E3.0.CO;2-9).
5. M. A. Crisfield, *Non-Linear Finite Element Analysis of Solids and Structures, Volume 1: Essentials*, John Wiley & Sons, 1991, ISBN 0-471-92956-5.
6. V. Z. Vlasov, *Thin-Walled Elastic Beams*, 2nd edition, Israel Program for Scientific Translations, 1961.
7. R. M. de Souza, *Force-based Finite Element for Large Displacement Inelastic Analysis of Structures*, PhD thesis, University of California at Berkeley, 2000.
