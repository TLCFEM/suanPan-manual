# Architecture Design

The MPI-based distributed design could take various forms in the context of OOP.

## A Straightforward Method
One approach is to serialize and send all associated data to another process, the receiving process deserializes the byte stream and creates all necessary objects and performs the computation.
This involves intensive data exchange, and packing/unpacking associated data every iteration is not a light task.
This approach does not scale well as the analysis would quickly be bottlenecked by encoding/decoding message and latency.

This is unfortunately the approach used by OpenSees.
OpenSees is outdated in terms of both shared-memory parallelism (which does not exist at all) and distributed-memory parallelism (which is too fine aggregated and lacks both performance and flexibility).
OpenSees effectively requires every class that needs to be distributed to provide a schema, in order to serialize/deserialize objects, manually, as there is a lack of reflection mechanism.
Imaging for general nonlinear problems, in order to update the status of an element, it needs to send element history variable sets and that of associated material objects over the network.
However, if it is an elastic step, the trial status can be simply computed by a matrix multiplication, the cost of messaging passing is disproportional and thus kills performance.
It does not scale well by the nature of its design.

## Remote Objects with P2P Communication

An alternative is to create the same object on every process, the actual computation is done on one of the processes, and only the results are sent back to the root process.
With this approach, there is no need for object 'proxies', as all objects on all processes are complete, fully functional, homogenous objects.
They manage all necessary data internally, locally.
There is also no need to pack/unpack complex data structure, making the implementation extremely simple and maintainable.
The only message to communicate is the elemental matrices (stiffness, mass, etc.) and the corresponding resistance vector.
The size is significantly smaller than the previous approach.

To illustrate, consider the following class definition.
Based on different `obj_tag`, the `assign_process` method labels each object with a process rank.
For each process, it can be queried whether a specific object `is_local` or not.
The computation logic can be triggered based on this flag, and calling the `gather` method will collect the designated quantity on the root process.

```cpp
class Distributed {
    static constexpr int root_rank{0};

    static auto assign_process(const int obj_tag) { return obj_tag % comm_size; }

    const int tag, process_rank;

public:
    const bool is_local;

    explicit Distributed(const int obj_tag)
        : tag(obj_tag)
        , process_rank(assign_process(tag))
        , is_local(comm_rank == process_rank) {}

    template<mpl_data_t DT> std::optional<mpl::irequest> gather(const Mat<DT>& object) {
        if(root_rank == comm_rank) {
            if(!is_local) return comm_world.irecv(const_cast<DT*>(object.memptr()), mpl::contiguous_layout<DT>{object.n_elem}, process_rank, mpl::tag_t{tag});
        }
        else if(is_local) return comm_world.isend(object.memptr(), mpl::contiguous_layout<DT>{object.n_elem}, root_rank, mpl::tag_t{tag});

        return std::nullopt;
    }
};
```

With such an approach, in the context of FEM, elements can be distributed on the process grid, and only elemental resistances and matrices need to be communicated.
This minimises the data to be circulated as all other associated data (e.g., element and material internal states) can be kept on local processes.

This approach only requires three MPI primitives: `MPI_Send`, `MPI_Recv` and `MPI_Bcast`, excluding the part of solving the global system.
This approach initiates MPI communication per element per iteration.
The number of messages is related to the number of elements in the problem.

However, the number of messages does **not** change and latency is still a problem.

## Collective Communication

At the cost of communicating larger messages, it is possible to drastically reduce the number of calls to MPI functions.
Given that elements are distributed on the process grid, each process handles a subset of elements.
The corresponding resistances and matrices (of those elements that are `is_local` to the specific process) can be assembled locally into the local copy of the global vectors/matrices.

Then all local copies can be reduced to formulate the complete global quantities via `MPI_Reduce` or `MPI_Allreduce`.
In most cases, reducing to the root process is enough so that there is no need to further broadcast to other processes.

For example, the following code assembles local elemental stiffness into local global stiffness, which is then reduced.

```cpp
void Domain::assemble_trial_stiffness() const {
    factory->clear_stiffness();

    for(const auto& I : element_pond.get()) {
        if(I->is_local) factory->assemble_stiffness(I->get_trial_stiffness(), I->get_dof_encoding(), I->get_dof_mapping());
    }

    factory->get_stiffness()->allreduce();
}
```

The `allreduce()` method calls the `MPI_Allreduce` under the hood.

```cpp
void DenseMat::allreduce() override {
    comm_world.allreduce(mpl::plus<T>(), memory.get(), mpl::contiguous_layout<T>{this->n_elem});
}
```

This approach only requires two MPI primitives: `MPI_Reduce`/`MPI_Allreduce` and `MPI_Bcast`, excluding the part of solving the global system.
This approach initiates MPI communication per iteration.
The number of messages is related to the number of processes in the process grid.

Given that it is preferable to communicate fewer but larger messages, this collective approach is preferable.
