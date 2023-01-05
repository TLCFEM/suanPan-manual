# Introduction

* [Introduction](README.md)

## Basic

* [Obtain Application](Basic/Obtain.md)
* [Configure Application](Basic/Config.md)
* [Perform Analysis](Basic/Analyze.md)
* [Model Syntax](Basic/Syntax.md)
* [Model Structure](Basic/Structure.md)
* [Tweak Performance](Basic/Performance.md)
* [Compile Application](Basic/Compile.md)
* [Build Documentation](Basic/Build.md)

## Example

* Developer
    * [element template](Example/Developer/element-template.md)
    * [material template](Example/Developer/material-template.md)
* Solid
    * [wave propagation](Example/Solid/wave-propagation.md)
* Geotechnical
    * [triaxial compression of sand](Example/Geotechnical/triaxial-compression-of-sand.md)
* Structural
    * Statics
        * [bending of a cantilever beam](Example/Structural/Statics/bending-of-a-cantilever-beam.md)
        * [bifurcation of a cantilever beam](Example/Structural/Statics/bifurcation-of-a-cantilever-beam.md)
        * [double-edge notched specimen](Example/Structural/Statics/double-edge-notched-specimen.md)
        * [lees frame](Example/Structural/Statics/lees-frame.md)
        * [notched beam under cyclic loading](Example/Structural/Statics/notched-beam-under-cyclic-loading.md)
        * [rc section analysis](Example/Structural/Statics/rc-section-analysis.md)
        * [truss roof](Example/Structural/Statics/truss-roof.md)
        * [uniform tension of a rubber specimen](Example/Structural/Statics/uniform-tension-of-a-rubber-specimen.md)
    * Dynamics
        * [bouncing of a ball](Example/Structural/Dynamics/bouncing-of-a-ball.md)
        * [mass-spring-dashpot system](Example/Structural/Dynamics/mass-spring-dashpot-system.md)
        * [dynamic analysis of a portal frame](Example/Structural/Dynamics/dynamic-analysis-of-a-portal-frame.md)
        * [particle collision](Example/Structural/Dynamics/particle-collision.md)
        * [response history analysis of an elastic coupled wall](Example/Structural/Dynamics/response-history-analysis-of-an-elastic-coupled-wall.md)
        * [multi-support excitation](Example/Structural/Dynamics/multi-support-excitation.md)
        * [triple pendulum](Example/Structural/Dynamics/triple-pendulum.md)
        * [computing response spectrum](Example/Structural/Dynamics/computing-response-spectrum.md)
    * Hybrid
        * [vibration of a displaced beam](Example/Structural/Hybrid/vibration-of-a-displaced-beam.md)
    * Buckling
        * [buckling analysis of a cantilever beam](Example/Structural/Buckling/buckling-analysis-of-a-cantilever-beam.md)
    * Contact
        * [contact between beam and block](Example/Structural/Contact/contact-between-beam-and-block.md)
        * [contact in 3d space](Example/Structural/Contact/contact-in-3d-space.md)
    * Optimization
        * [evolutionary structural optimization](Example/Structural/Optimization/evolutionary-structural-optimization.md)
    * Isogeometric Analysis
        * [linear analysis of a single element](Example/Structural/IGA/linear-analysis-of-a-single-element.md)
* Miscellaneous
    * [batch execution for automation](Example/Miscellaneous/batch-execution.md)

## Command Collection

* Define
    * [amplitude](Collection/Define/amplitude.md)
    * [bc](Collection/Define/bc.md)
    * [domain](Collection/Define/domain.md)
    * [element](Collection/Define/element.md)
    * [file](Collection/Define/file.md)
    * [generate](Collection/Define/generate.md)
    * [group](Collection/Define/group.md)
    * [import](Collection/Define/import.md)
    * [initial](Collection/Define/initial.md)
    * [load](Collection/Define/load.md)
    * [material](Collection/Define/material.md)
    * [modifier](Collection/Define/modifier.md)
    * [node](Collection/Define/node.md)
    * [recorder](Collection/Define/recorder.md)
    * [section](Collection/Define/section.md)
* Configure
    * [analyze](Collection/Configure/analyze.md)
    * [converger](Collection/Configure/converger.md)
    * [criterion](Collection/Configure/criterion.md)
    * [integrator](Collection/Configure/integrator.md)
    * [precheck](Collection/Configure/precheck.md)
    * [step](Collection/Configure/step.md)
* Process
    * [benchmark](Collection/Process/benchmark.md)
    * [clear](Collection/Process/clear.md)
    * [command](Collection/Process/command.md)
    * [enable](Collection/Process/enable.md)
    * [exit](Collection/Process/exit.md)
    * [materialtest](Collection/Process/materialtest.md)
    * [materialtestbyload](Collection/Process/materialtestbyload.md)
    * [peek](Collection/Process/peek.md)
    * [plot](Collection/Process/plot.md)
    * [protect](Collection/Process/protect.md)
    * [pwd](Collection/Process/pwd.md)
    * [reset](Collection/Process/reset.md)
    * [save](Collection/Process/save.md)
    * [set](Collection/Process/set.md)
    * [upsampling](Collection/Process/upsampling.md)
    * [sdof_response](Collection/Process/sdof_response.md)
    * [response_spectrum](Collection/Process/response_spectrum.md)

## Model Library

### Amplitude

* [Amplitude](Library/Amplitude/Amplitude.md)
* Special
    * [NZStrongMotion](Library/Amplitude/Special/NZStrongMotion.md)
* Universal
    * [Combine](Library/Amplitude/Universal/Combine.md)
    * [Constant](Library/Amplitude/Universal/Constant.md)
    * [Decay](Library/Amplitude/Universal/Decay.md)
    * [Linear](Library/Amplitude/Universal/Linear.md)
    * [Modulated](Library/Amplitude/Universal/Modulated.md)
    * [Tabular](Library/Amplitude/Universal/Tabular.md)
    * [TabularSpline](Library/Amplitude/Universal/TabularSpline.md)
    * [Trig](Library/Amplitude/Universal/Trig.md)

### [Constraint](Library/Constraint/Constraint.md)

* [MPC](Library/Constraint/MPC.md)
* [ParticleCollision](Library/Constraint/ParticleCollision.md)
* [RigidWall](Library/Constraint/RigidWall.md)
* [RestitutionWall](Library/Constraint/RestitutionWall.md)
* [FixedLength](Library/Constraint/FixedLength.md)
* [NodeLine](Library/Constraint/NodeLine.md)
* [NodeFacet](Library/Constraint/NodeFacet.md)
* [Embed2D](Library/Constraint/Embed2D.md)
* [Embed3D](Library/Constraint/Embed3D.md)

### Converger

* [Converger](Library/Converger/Converger.md)
* Absolute
    * [AbsDisp](Library/Converger/Absolute/AbsDisp.md)
    * [AbsError](Library/Converger/Absolute/AbsError.md)
    * [AbsIncreDisp](Library/Converger/Absolute/AbsIncreDisp.md)
    * [AbsIncreAcc](Library/Converger/Absolute/AbsIncreAcc.md)
    * [AbsIncreEnergy](Library/Converger/Absolute/AbsIncreEnergy.md)
    * [AbsResidual](Library/Converger/Absolute/AbsResidual.md)
* Other
    * [FixedNumber](Library/Converger/Other/FixedNumber.md)
    * [Logic](Library/Converger/Other/Logic.md)
* Relative
    * [RelDisp](Library/Converger/Relative/RelDisp.md)
    * [RelError](Library/Converger/Relative/RelError.md)
    * [RelIncreDisp](Library/Converger/Relative/RelIncreDisp.md)
    * [RelIncreAcc](Library/Converger/Relative/RelIncreAcc.md)
    * [RelIncreEnergy](Library/Converger/Relative/RelIncreEnergy.md)
    * [RelResidual](Library/Converger/Relative/RelResidual.md)

### Criterion

* [Criterion](Library/Criterion/Criterion.md)
* [MaxDisplacement](Library/Criterion/MaxDisplacement.md)
* [MaxHistory](Library/Criterion/MaxHistory.md)
* [MaxResistance](Library/Criterion/MaxResistance.md)
* [MinDisplacement](Library/Criterion/MinDisplacement.md)
* [MinResistance](Library/Criterion/MinResistance.md)
* [StrainEnergyEvolution](Library/Criterion/StrainEnergyEvolution.md)

### Element

* Beam
    * [B21](Library/Element/Beam/B21.md)
    * [B21E](Library/Element/Beam/B21E.md)
    * [B21H](Library/Element/Beam/B21H.md)
    * [B31](Library/Element/Beam/B31.md)
    * [EB21](Library/Element/Beam/EB21.md)
    * [F21](Library/Element/Beam/F21.md)
    * [F21H](Library/Element/Beam/F21H.md)
    * [F31](Library/Element/Beam/F31.md)
    * [NMB21](Library/Element/Beam/NMB21.md)
    * [NMB21E](Library/Element/Beam/NMB21E.md)
    * [NMB31](Library/Element/Beam/NMB31.md)
    * [MVLEM](Library/Element/Beam/MVLEM.md)
    * [Orientation](Library/Element/Beam/Orientation.md)
* Cube
    * [C3D20](Library/Element/Cube/C3D20.md)
    * [C3D4](Library/Element/Cube/C3D4.md)
    * [C3D8](Library/Element/Cube/C3D8.md)
    * [C3D8I](Library/Element/Cube/C3D8I.md)
    * [CIN3D8](Library/Element/Cube/CIN3D8.md)
    * [DC3D4](Library/Element/Cube/DC3D4.md)
    * [DC3D8](Library/Element/Cube/DC3D8.md)
* Membrane
    * [Couple Stress](Library/Element/Membrane/CS.md)
    * Phase Field
        * [DCP3](Library/Element/Membrane/DCP3.md)
        * [DCP4](Library/Element/Membrane/DCP4.md)
    * Axisymmetric
        * [CAX3](Library/Element/Membrane/Axisymmetric/CAX3.md)
        * [CAX4](Library/Element/Membrane/Axisymmetric/CAX4.md)
        * [CAX8](Library/Element/Membrane/Axisymmetric/CAX8.md)
    * Plane
        * [CP3](Library/Element/Membrane/Plane/CP3.md)
        * [CP4](Library/Element/Membrane/Plane/CP4.md)
        * [CP4I](Library/Element/Membrane/Plane/CP4I.md)
        * [CP5](Library/Element/Membrane/Plane/CP5.md)
        * [CP6](Library/Element/Membrane/Plane/CP6.md)
        * [CP7](Library/Element/Membrane/Plane/CP7.md)
        * [CP8](Library/Element/Membrane/Plane/CP8.md)
    * Mixed
        * [PS](Library/Element/Membrane/Mixed/PS.md)
        * [QE2](Library/Element/Membrane/Mixed/QE2.md)
    * Drilling
        * [Allman](Library/Element/Membrane/Drilling/Allman.md)
        * [GCMQ](Library/Element/Membrane/Drilling/GCMQ.md)
        * [GQ12](Library/Element/Membrane/Drilling/GQ12.md)
    * Infinite
        * [CINP4](Library/Element/Membrane/Plane/CINP4.md)
    * Geotechnical
        * [PCPE4DC](Library/Element/Membrane/PCPE4DC.md)
    * [Membrane](Library/Element/Membrane/Membrane.md)
* Modifier
    * [Modifier](Library/Element/Modifier/Modifier.md)
* Patch
    * [Patch](Library/Element/Patch/Patch.md)
    * [PatchCube](Library/Element/Patch/PatchCube.md)
    * [PatchQuad](Library/Element/Patch/PatchQuad.md)
* Plate
    * [DKT3](Library/Element/Plate/DKT3.md)
    * [DKT4](Library/Element/Plate/DKT4.md)
    * [Mindlin](Library/Element/Plate/Mindlin.md)
* Shell
    * [DKTS3](Library/Element/Shell/DKTS3.md)
    * [DKTS4](Library/Element/Shell/DKTS4.md)
    * [S4](Library/Element/Shell/S4.md)
    * [SGCMS](Library/Element/Shell/SGCMS.md)
    * [ShellBase](Library/Element/Shell/ShellBase.md)
* Special
    * [Contact2D](Library/Element/Special/Contact2D.md)
    * [Contact3D](Library/Element/Special/Contact3D.md)
    * [Damper01](Library/Element/Special/Damper01.md)
    * [Damper02](Library/Element/Special/Damper02.md)
    * [Embedded2D](Library/Element/Special/Embedded2D.md)
    * [Embedded3D](Library/Element/Special/Embedded3D.md)
    * [Joint](Library/Element/Special/Joint.md)
    * [Mass](Library/Element/Special/Mass.md)
    * [SingleSection](Library/Element/Special/SingleSection.md)
    * [Spring01](Library/Element/Special/Spring01.md)
    * [Spring02](Library/Element/Special/Spring02.md)
    * [Tie](Library/Element/Special/Tie.md)
* Truss
    * [T2D2](Library/Element/Truss/T2D2.md)
    * [T2D2S](Library/Element/Truss/T2D2S.md)
    * [T3D2](Library/Element/Truss/T3D2.md)
    * [T3D2S](Library/Element/Truss/T3D2S.md)

### Integrator

* Implicit
    * [Linear](Library/Integrator/Linear.md)
    * [BatheTwoStep](Library/Integrator/BatheTwoStep.md)
    * [GeneralizedAlpha](Library/Integrator/GeneralizedAlpha.md)
    * [OALTS](Library/Integrator/OALTS.md)
    * [GSSSS](Library/Integrator/GSSSS.md)
    * Newmark
        * [LeeNewmark](Library/Integrator/Newmark/LeeNewmark.md)
        * [LeeNewmarkFull](Library/Integrator/Newmark/LeeNewmarkFull.md)
        * [Newmark](Library/Integrator/Newmark/Newmark.md)
        * [RayleighNewmark](Library/Integrator/Newmark/RayleighNewmark.md)
        * [WilsonPenzienNewmark](Library/Integrator/Newmark/WilsonPenzienNewmark.md)
* Explicit
    * [Tchamwa](Library/Integrator/Tchamwa.md)
    * [BatheExplicit](Library/Integrator/BatheExplicit.md)
    * [GeneralizedAlphaExplicit](Library/Integrator/GeneralizedAlphaExplicit.md)

### Material

* Guide
    * [Metal](Library/Material/Guide/Metal.md)
    * [Customisation](Library/Material/Guide/Customisation.md)
* [Material1D](Library/Material/Material1D/Material1D.md)
    * Concrete
        * [ConcreteCM](Library/Material/Material1D/Concrete/ConcreteCM.md)
        * [ConcreteExp](Library/Material/Material1D/Concrete/ConcreteExp.md)
        * [ConcreteTsai](Library/Material/Material1D/Concrete/ConcreteTsai.md)
    * Degradation
        * [Degradation](Library/Material/Material1D/Degradation/Degradation.md)
    * Elastic
        * [BilinearElastic1D](Library/Material/Material1D/Elastic/BilinearElastic1D.md)
        * [Elastic1D](Library/Material/Material1D/Elastic/Elastic1D.md)
        * [MultilinearElastic1D](Library/Material/Material1D/Elastic/MultilinearElastic1D.md)
        * [PolyElastic1D](Library/Material/Material1D/Elastic/PolyElastic1D.md)
        * [NLE1D01](Library/Material/Material1D/Elastic/NLE1D01.md)
        * [Sinh1D](Library/Material/Material1D/Elastic/Sinh1D.md)
        * [Tanh1D](Library/Material/Material1D/Elastic/Tanh1D.md)
    * Hysteresis
        * [AFC](Library/Material/Material1D/Hysteresis/AFC.md)
        * [AFCN](Library/Material/Material1D/Hysteresis/AFCN.md)
        * [BilinearOO](Library/Material/Material1D/Hysteresis/BilinearOO.md)
        * [BilinearPO](Library/Material/Material1D/Hysteresis/BilinearPO.md)
        * [BoucWen](Library/Material/Material1D/Hysteresis/BoucWen.md)
        * [BWBN](Library/Material/Material1D/Hysteresis/BWBN.md)
        * [Flag](Library/Material/Material1D/Hysteresis/Flag.md)
        * [MPF](Library/Material/Material1D/Hysteresis/MPF.md)
        * [MultilinearOO](Library/Material/Material1D/Hysteresis/MultilinearOO.md)
        * [MultilinearPO](Library/Material/Material1D/Hysteresis/MultilinearPO.md)
        * [RambergOsgood](Library/Material/Material1D/Hysteresis/RambergOsgood.md)
        * [SimpleHysteresis](Library/Material/Material1D/Hysteresis/SimpleHysteresis.md)
        * [SlipLock](Library/Material/Material1D/Hysteresis/SlipLock.md)
        * [SteelBRB](Library/Material/Material1D/Hysteresis/SteelBRB.md)
        * [Trivial](Library/Material/Material1D/Hysteresis/Trivial.md)
    * Viscosity
        * [Kelvin](Library/Material/Material1D/Viscosity/Kelvin.md)
        * [Maxwell](Library/Material/Material1D/Viscosity/Maxwell.md)
        * [NonlinearViscosity](Library/Material/Material1D/Viscosity/NonlinearViscosity.md)
        * [Viscosity01](Library/Material/Material1D/Viscosity/Viscosity01.md)
        * [Viscosity02](Library/Material/Material1D/Viscosity/Viscosity02.md)
        * [CoulombFriction](Library/Material/Material1D/Viscosity/CoulombFriction.md)
    * vonMises
        * [ArmstrongFrederick1D](Library/Material/Material1D/vonMises/ArmstrongFrederick1D.md)
        * [Bilinear1D](Library/Material/Material1D/vonMises/Bilinear1D.md)
        * [BilinearMises1D](Library/Material/Material1D/vonMises/BilinearMises1D.md)
        * [ExpGurson1D](Library/Material/Material1D/vonMises/ExpGurson1D.md)
        * [ExpMises1D](Library/Material/Material1D/vonMises/ExpMises1D.md)
        * [Mises1D](Library/Material/Material1D/vonMises/Mises1D.md)
        * [Multilinear1D](Library/Material/Material1D/vonMises/Multilinear1D.md)
        * [NonlinearGurson1D](Library/Material/Material1D/vonMises/NonlinearGurson1D.md)
        * [VAFCRP1D](Library/Material/Material1D/vonMises/VAFCRP1D.md)
* Material2D
    * [AxisymmetricElastic](Library/Material/Material2D/AxisymmetricELastic.md)
    * [Bilinear2D](Library/Material/Material2D/Bilinear2D.md)
    * [Concrete21](Library/Material/Material2D/Concrete21.md)
    * [Concrete22](Library/Material/Material2D/Concrete22.md)
    * [Elastic2D](Library/Material/Material2D/Elastic2D.md)
    * [Rebar2D](Library/Material/Material2D/Rebar2D.md)
* [Material3D](Library/Material/Material3D/Material3D.md)
    * CamClay
        * [BilinearCC](Library/Material/Material3D/Clay/CamClay/BilinearCC.md)
        * [ExpCC](Library/Material/Material3D/Clay/CamClay/ExpCC.md)
        * [NonlinearCamClay](Library/Material/Material3D/Clay/CamClay/NonlinearCamClay.md)
        * [ParabolicCC](Library/Material/Material3D/Clay/CamClay/ParabolicCC.md)
    * Concrete
        * [CDP](Library/Material/Material3D/Concrete/CDP.md)
        * [CDPM2](Library/Material/Material3D/Concrete/CDPM2.md)
        * [Rebar3D](Library/Material/Material3D/Concrete/Rebar3D.md)
        * [TableCDP](Library/Material/Material3D/Concrete/TableCDP.md)
    * Damage
        * [IsotropicDamage](Library/Material/Material3D/Damage/IsotropicDamage.md)
        * [LinearDamage](Library/Material/Material3D/Damage/LinearDamage.md)
    * DruckerPrager
        * [BilinearDP](Library/Material/Material3D/DruckerPrager/BilinearDP.md)
        * [ExpDP](Library/Material/Material3D/DruckerPrager/ExpDP.md)
        * [NonlinearDruckerPrager](Library/Material/Material3D/DruckerPrager/NonlinearDruckerPrager.md)
    * Elastic
        * [BlatzKo](Library/Material/Material3D/Elastic/BlatzKo.md)
        * [IsotropicElastic3D](Library/Material/Material3D/Elastic/IsotropicElastic3D.md)
        * [IsotropicNonlinearElastic3D](Library/Material/Material3D/Elastic/IsotropicNonlinearElastic3D.md)
        * [MooneyRivlin](Library/Material/Material3D/Elastic/MooneyRivlin.md)
        * [NLE3D01](Library/Material/Material3D/Elastic/NLE3D01.md)
        * [OrthotropicElastic3D](Library/Material/Material3D/Elastic/OrthotropicElastic3D.md)
        * [Yeoh](Library/Material/Material3D/Elastic/Yeoh.md)
    * Hoffman
        * [BilinearHoffman](Library/Material/Material3D/Hoffman/BilinearHoffman.md)
        * [ExpHoffman](Library/Material/Material3D/Hoffman/ExpHoffman.md)
        * [NonlinearHill](Library/Material/Material3D/Hoffman/NonlinearHill.md)
        * [NonlinearHoffman](Library/Material/Material3D/Hoffman/NonlinearHoffman.md)
    * Sand
        * [SimpleSand](Library/Material/Material3D/Sand/SimpleSand.md)
        * [DafalisaManzari](Library/Material/Material3D/Sand/DafaliasManzari.md)
    * vonMises
        * [ArmstrongFrederick](Library/Material/Material3D/vonMises/ArmstrongFrederick.md)
        * [BilinearJ2](Library/Material/Material3D/vonMises/BilinearJ2.md)
        * [BilinearPeric](Library/Material/Material3D/vonMises/BilinearPeric.md)
        * [ExpGurson](Library/Material/Material3D/vonMises/ExpGurson.md)
        * [ExpJ2](Library/Material/Material3D/vonMises/ExpJ2.md)
        * [MultilinearJ2](Library/Material/Material3D/vonMises/MultilinearJ2.md)
        * [NonlinearGurson](Library/Material/Material3D/vonMises/NonlinearGurson.md)
        * [NonlinearJ2](Library/Material/Material3D/vonMises/NonlinearJ2.md)
        * [NonlinearPeric](Library/Material/Material3D/vonMises/NonlinearPeric.md)
        * [PolyJ2](Library/Material/Material3D/vonMises/PolyJ2.md)
        * [VAFCRP](Library/Material/Material3D/vonMises/VAFCRP.md)
* Wrapper
    * [Axisymmetric](Library/Material/Wrapper/Axisymmetric.md)
    * [Laminated](Library/Material/Wrapper/Laminated.md)
    * [Parallel](Library/Material/Wrapper/Parallel.md)
    * [PlaneStrain](Library/Material/Wrapper/PlaneStrain.md)
    * [PlaneSymmetric](Library/Material/Wrapper/PlaneSymmetric.md)
    * [PlaneStress](Library/Material/Wrapper/PlaneStress.md)
    * [Rotation2D](Library/Material/Wrapper/Rotation2D.md)
    * [Rotation3D](Library/Material/Wrapper/Rotation3D.md)
    * [Sequential](Library/Material/Wrapper/Sequential.md)
    * [Stacked](Library/Material/Wrapper/Stacked.md)
    * [Uniaxial](Library/Material/Wrapper/Uniaxial.md)

### Recorder

* [Recorder](Library/Recorder/Recorder.md)
* [OutputType](Library/Recorder/OutputType.md)

### Section

* Code
    * [EU](Library/Section/Code/EU.md)
    * [NZ](Library/Section/Code/NZ.md)
    * [US](Library/Section/Code/US.md)
* Section1D
    * [Circle1D](Library/Section/Section1D/Circle1D.md)
    * [Fibre1D](Library/Section/Section1D/Fibre1D.md)
    * [Rectangle1D](Library/Section/Section1D/Rectangle1D.md)
    * [TrussSection](Library/Section/Section1D/TrussSection.md)
* Section2D
    * [Bar2D](Library/Section/Section2D/Bar2D.md)
    * [Box2D](Library/Section/Section2D/Box2D.md)
    * [Circle2D](Library/Section/Section2D/Circle2D.md)
    * [CircularHollow2D](Library/Section/Section2D/CircularHollow2D.md)
    * [Fibre2D](Library/Section/Section2D/Fibre2D.md)
    * [HSection2D](Library/Section/Section2D/HSection2D.md)
    * [ISection2D](Library/Section/Section2D/ISection2D.md)
    * [Rectangle2D](Library/Section/Section2D/Rectangle2D.md)
    * [TSection2D](Library/Section/Section2D/TSection2D.md)
* Section3D
    * [Bar3D](Library/Section/Section3D/Bar3D.md)
    * [Box3D](Library/Section/Section3D/Box3D.md)
    * [Circle3D](Library/Section/Section3D/Circle3D.md)
    * [CircularHollow3D](Library/Section/Section3D/CircularHollow3D.md)
    * [Fibre3D](Library/Section/Section3D/Fibre3D.md)
    * [ISection3D](Library/Section/Section3D/ISection3D.md)
    * [Rectangle3D](Library/Section/Section3D/Rectangle3D.md)
    * [TSection3D](Library/Section/Section3D/TSection3D.md)
* SectionNM
    * [SectionNM](Library/Section/SectionNM/SectionNM.md)
    * [NM2D1](Library/Section/SectionNM/NM2D1.md)
    * [NM2D2](Library/Section/SectionNM/NM2D2.md)
    * [NM3D1](Library/Section/SectionNM/NM3D1.md)
    * [NM3D2](Library/Section/SectionNM/NM3D2.md)

### Solver

* [BFGS](Library/Solver/BFGS.md)
* [MPDC](Library/Solver/MPDC.md)
* [Newton](Library/Solver/Newton.md)
* [Ramm](Library/Solver/Ramm.md)

### Step

* [ArcLength](Library/Step/ArcLength.md)
* [Buckle](Library/Step/Buckle.md)
* [Dynamic](Library/Step/Dynamic.md)
* [Frequency](Library/Step/Frequency.md)
* [Optimization](Library/Step/Optimization.md)
* [Static](Library/Step/Static.md)

## Developer

* [Prerequisites](Developer/Prerequisites.md)
* C Style Interface
    * [material](Developer/C/material.md)
* CPP Style Interface
    * [material](Developer/CPP/material.md)
    * [element](Developer/CPP/element.md)
    * [constraint](Developer/CPP/constraint.md)