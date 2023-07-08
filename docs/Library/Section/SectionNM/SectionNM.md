# SectionNM

$$N$$-$$M$$ Interaction Abstract Section

## Reference

1. [10.1061/JSENDH/STENG-12176](http://dx.doi.org/10.1061/JSENDH/STENG-12176)
2. [10.1007/978-94-007-6573-3_3](http://dx.doi.org/10.1007/978-94-007-6573-3_3)
3. [10.1002/nme.1620371506](https://doi.org/10.1002/nme.1620371506)

Please note the formulation is based on the first reference, which is a revised version of the one shown in the last two references.

## Remarks

Apart from the provided sections, other interaction surfaces can be defined.

One can define a derived class based on, for example, `SurfaceNM2D`, and implement methods.

```cpp
[[nodiscard]] double compute_sf(const vec&, const vec&) const;
[[nodiscard]] vec compute_dsf(const vec&, const vec&) const;
[[nodiscard]] mat compute_ddsf(const vec&, const vec&) const;
```

All methods take the normalised shifted resistance $$\mathbf{s}=\mathbf{q}-\mathbf{\beta}$$ and equivalent plastic 
strain $$\alpha$$ as input where $$\mathbf{q}$$ is the normalised nodal resistance and $$\mathbf{\beta}$$ is the back 
resistance which is similar to the concept of back stress.
