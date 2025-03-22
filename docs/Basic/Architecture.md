# Architecture

The MPI-based distributed design could take various forms in the context of OOP.

One approach is to serialize and send all associated data to another process, the receiving process deserialize the byte stream and create all necessary objects and perform the computation.
This involves intensive data exchange, and packing/unpacking associated data every iteration is not a light task.
This approach does not scale well as the analysis would quickly be bottlenecked by encoding/decoding message and latency.

An alternative is to create the same object on every process, the actual computation is done on one of the processes, and only the results are sent back to the root process.
With this approach, there is no need for object 'proxies', as all objects on all processes are complete, fully functional, homogenous objects.
They manage all necessary data internally, locally.
There is also no need to pack/unpack complex data structure, making the implementation extremely simple and maintainable.


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

        return {};
    }
};
```
