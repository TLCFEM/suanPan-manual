from pydantic import BaseModel, Field


class BaseModelSP(BaseModel):
    def generate_input(self):
        raise NotImplementedError


class Tagged(BaseModelSP):
    tag: int = Field(description="Tag.")
    alias: str | None = Field(None, description="Alias.")


class Node(Tagged):
    coordinates: list[float] = Field(
        description="Node coordinates.", min_length=1, max_length=3
    )

    def generate_input(self):
        command: str = f"node {self.tag}"
        for coord in self.coordinates:
            command += f" {coord}"
        return command


class Element(Tagged):
    nodes: list[int | Node] = Field(
        default_factory=list, description="Node connectivity.", min_length=1
    )
    type: str = Field(description="Element type.")

    def __init__(self, *args, **kwargs):
        kwargs["type"] = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def generate_input(self):
        command: str = f"element {self.type} {self.tag}"
        for node in self.nodes:
            command += f" {node if isinstance(node, int) else node.tag}"
        return command


class MaterialElement(Element):
    material: int = Field(description="Material tag.")

    def generate_input(self):
        return f"{super().generate_input()} {self.material}"


class SectionElement(Element):
    section: int = Field(description="Section tag.")

    def generate_input(self):
        return f"{super().generate_input()} {self.section}"


class CP4(MaterialElement):
    thickness: float = Field(1.0, description="Thickness of the element.")
    reduced_integration: bool = Field(
        False, description="Whether to use reduced integration."
    )
    nlgeom: bool = Field(False, description="Whether to use nonlinear geometry.")

    def generate_input(self):
        return f"{super().generate_input()} {self.thickness} {int(self.reduced_integration)} {int(self.nlgeom)}"


class Material(Tagged):
    pass


class Constraint(Tagged):
    pass


class Load(Tagged):
    pass


class Amplitude(Tagged):
    pass


class Integrator(Tagged):
    pass


class Solver(Tagged):
    pass


class Converger(Tagged):
    pass


class StepStorageConfig(BaseModelSP):
    banded: bool = Field(True, description="Whether to use banded storage.")
    symmetric: bool = Field(False, description="Whether to use symmetric storage.")
    sparse: bool = Field(False, description="Whether to use sparse storage.")

    def generate_input(self):
        command: list = []
        if self.sparse is not False:
            command.append("set sparse_mat true")
        else:
            if self.banded is False:
                command.append("set banded_mat false")
            if self.symmetric is True:
                command.append("set symm_mat true")

        return "\n".join(command)


class StepSizeConfig(BaseModelSP):
    initial: float | None = Field(
        None,
        gt=0,
        description="Initial step size, should be positive and smaller than the total duration of the step.",
    )
    min: float | None = Field(
        None,
        gt=0,
        description="Minimum step size, should be positive and smaller than the maximum step size.",
    )
    max: float | None = Field(
        None,
        gt=0,
        description="Maximum step size, should be greater than the minimum step size but smaller than the total duration.",
    )
    fixed: bool = Field(
        False, gt=0, description="Whether the step size is fixed or not."
    )

    def generate_input(self):
        command: list = []
        if self.initial is not None:
            command.append(f"set ini_step_size {self.initial}")
        if self.min is not None:
            command.append(f"set min_step_size {self.min}")
        if self.max is not None:
            command.append(f"set max_step_size {self.max}")
        if self.fixed:
            command.append("set fixed_step_size true")

        return "\n".join(command)


class StepConfig(BaseModelSP):
    storage: StepStorageConfig | None = Field(description="Storage configuration.")
    sizing: StepSizeConfig | None = Field(description="Step size configuration.")

    def generate_input(self):
        command: list = []
        if self.storage is not None:
            command.append(self.storage.generate_input())
        if self.sizing is not None:
            command.append(self.sizing.generate_input())

        return "\n".join(command)


class Step(Tagged):
    type: str = Field(description="Step type.")
    duration: float | None = Field(
        default=1, description="Duration of the analysis step."
    )

    config: StepConfig | None = Field(None, description="Solving configuration.")

    integrator: Integrator | None = Field(None, description="Integrator.")
    solver: Solver | None = Field(None, description="Solver.")
    converger: Converger | None = Field(None, description="Converger.")

    constraints: list[Constraint] = Field(
        default_factory=list, description="Constraints."
    )
    loads: list[Load] = Field(default_factory=list, description="Loads.")

    def __init__(self, *args, **kwargs):
        kwargs["type"] = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def generate_input(self):
        command: list = [
            f"step {self.type} {self.tag}"
            + (f" {self.duration}" if self.duration is not None else "")
        ]
        if self.config is not None:
            command.append(self.config.generate_input())
        for x in (self.integrator, self.solver, self.converger):
            if x is not None:
                command.append(x.generate_input())
        for x in (self.constraints, self.loads):
            command.extend([item.generate_input() for item in x])

        return "\n".join(command)


class Static(Step):
    pass


class ExplicitDynamic(Step):
    pass


class ImplicitDynamic(Step):
    pass


class Domain(Tagged):
    nodes: dict[int, Node] = Field(default_factory=dict, description="Nodes.")
    elements: dict[int, Element] = Field(default_factory=dict, description="Elements.")
    materials: dict[int, Material] = Field(
        default_factory=dict, description="Materials."
    )
    steps: dict[int, Step] = Field(default_factory=dict, description="Steps.")

    def add(self, item):
        if isinstance(item, Node):
            self.nodes[item.tag] = item
        elif isinstance(item, Element):
            self.elements[item.tag] = item
        elif isinstance(item, Material):
            self.materials[item.tag] = item
        elif isinstance(item, Step):
            self.steps[item.tag] = item
        else:
            raise ValueError(f"Invalid item type: {type(item)}.")

    def generate_input(self):
        commands: list = [f"domain {self.tag}"]
        for x in (self.nodes, self.elements, self.materials, self.steps):
            commands.extend([item.generate_input() for item in x.values()])
        return "\n".join(commands)


class Bead(BaseModelSP):
    domains: list[Domain] = Field(default_factory=list, description="Domains.")


if __name__ == "__main__":
    domain = Domain(tag=1)
    domain.add(Node(tag=1, coordinates=[0, 0, 0]))
    domain.add(Node(tag=2, coordinates=[1, 0, 0]))
    domain.add(Node(tag=3, coordinates=[1, 1, 0]))
    domain.add(Node(tag=4, coordinates=[0, 1, 0]))
    domain.add(CP4(tag=1, nodes=[1, 2, 3, 4], material=1, thickness=0.1, nlgeom=True))

    domain.add(
        Static(
            tag=1,
            duration=2,
            config=StepConfig(
                storage=StepStorageConfig(sparse=True),
                sizing=StepSizeConfig(initial=0.1, fixed=True),
            ),
        )
    )

    print(domain.generate_input())
