# SimpleHysteresis

The `SimpleHysteresis` model is a simplified framework for defining arbitrary backbones with linear unloading/reloading behaviour.
The residual strain can be customised according to the specific rules.

## Theory

This class is the abstract engine shared by the origin-oriented and peak-oriented models, namely [BilinearOO](BilinearOO.md), [BilinearPO](BilinearPO.md), [MultilinearOO](MultilinearOO.md) and [MultilinearPO](MultilinearPO.md).
A derived class supplies a tension backbone, a compression backbone, the initial reverse points on the opposite signs, and a residual-strain rule for each sign.
The backbone functions return a stress and a tangent for a given strain and are evaluated whenever the material moves beyond the most extreme strain reached so far.
When the strain increment reverses, the current point becomes a reversal point and the residual strain $$\varepsilon_r$$ is computed from the residual rule.
Subsequent response follows a straight inner branch that connects the compression reversal point, an optional intermediate point and the tension reversal point, with the mirror construction on the compression side.
The intermediate branch is controlled by the dimensionless `middle_point` parameter $$m$$, which is clamped to $$[\epsilon,1]$$, and the built-in origin-oriented and peak-oriented models use $$m=1$$.
Five states, namely `NONE`, `TBACKBONE`, `CBACKBONE`, `TINNER` and `CINNER`, select the active curve, and the transitions between them are triggered when the strain crosses a stored reversal point.
The model is rate independent and returns the same loop for the same strain history.

!!! info "deviation from theory"
    The `middle_point` parameter is clamped to the interval $$[\epsilon,1]$$, and the origin-oriented and peak-oriented subclasses always use the value one.
    A freely adjustable intermediate branch point is therefore not exposed by the models built on this framework.

!!! warning "implementation limitation"
    All inner branches are straight segments with abrupt tangent changes at the reversal and residual points.
    The framework provides no smooth transition of Menegotto-Pinto type, no cyclic degradation and no isotropic hardening.

## Remarks

- This class is abstract and cannot be instantiated directly by a `material` command.
- Eight history variables are reserved, namely the extreme compression and tension strains, the strain and stress of each reversal point, and the two residual strains.
- The inner branches are straight lines, so the tangent is constant within a branch and the switches are detected from the strain alone.
- The origin-oriented residual rule returns zero, whereas the peak-oriented residual rule returns the elastic intercept.
  This single difference accounts for most of the visual difference between the two families.
- See [BilinearOO](BilinearOO.md) and [BilinearPO](BilinearPO.md) for the analytic bilinear forms and [MultilinearOO](MultilinearOO.md) and [MultilinearPO](MultilinearPO.md) for tabulated backbones.

## History Variable Layout

| location             | value                             |
|----------------------|-----------------------------------|
| `initial_history(0)` | maximum compression strain        |
| `initial_history(1)` | maximum tension strain            |
| `initial_history(2)` | last compression unloading strain |
| `initial_history(3)` | last compression unloading stress |
| `initial_history(4)` | last tension unloading strain     |
| `initial_history(5)` | last tension unloading stress     |
| `initial_history(6)` | residual compression strain       |
| `initial_history(7)` | residual tension strain           |

## References

- Ibarra, L. F., Medina, R. A. and Krawinkler, H. (2005), "Hysteretic models that incorporate strength and stiffness deterioration", Earthquake Engineering and Structural Dynamics, 34(12), 1489-1511, doi:10.1002/eqe.495.
