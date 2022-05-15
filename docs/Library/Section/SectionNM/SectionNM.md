# SectionNM

$$N$$-$$M$$ Interaction Abstract Section

## Reference

1. [10.1007/978-94-007-6573-3_3](http://dx.doi.org/10.1007/978-94-007-6573-3_3)
2. [10.1002/nme.1620371506](https://doi.org/10.1002/nme.1620371506)

Please note the formulation is similar but different from the one shown in the above references.

## Remarks

Apart from the provided sections, other interaction surfaces can be defined.

One can define a derived class based on either `SectionNM2D` or `SectionNM3D` and implement three methods.

```cpp
[[nodiscard]] double compute_f(const vec&) const override;
[[nodiscard]] vec compute_df(const vec&) const override;
[[nodiscard]] mat compute_ddf(const vec&) const override;
```

All three methods takes the shifted resistance $$\mathbf{s}=\mathbf{q}-\mathbf{\beta}$$ as input where $$\mathbf{q}$$ is
the nodal resistance and $$\mathbf{\beta}$$ is the back resistance which is similar to the concept of back stress.

The three methods return $$N$$-$$M$$ interaction surface and its derivatives with regard to $$\mathbf{s}$$.

For example, the [`NM2D2`](NM2D2.md) section implements the above three methods as follows.

```cpp
double NM2D2::compute_f(const vec& s) const {
	const auto p = s(0) / yield_force(0);
	const auto my = s(1) / yield_force(1);

	return 1.15 * pow(p, 2.) + pow(my, 2.) + 3.67 * pow(p * my, 2.) - c;
}

vec NM2D2::compute_df(const vec& s) const {
	const auto p = s(0) / yield_force(0);
	const auto my = s(1) / yield_force(1);

	vec df(2, fill::none);

	df(0) = p * (2.3 + 7.34 * pow(my, 2.));
	df(1) = my * (2. + 7.34 * pow(p, 2.));

	return df / yield_force;
}

mat NM2D2::compute_ddf(const vec& s) const {
	const auto p = s(0) / yield_force(0);
	const auto my = s(1) / yield_force(1);

	mat ddf(2, 2, fill::none);

	ddf(0, 0) = 2.3 + 7.34 * pow(my, 2.);
	ddf(1, 1) = 2. + 7.34 * pow(p, 2.);
	ddf(1, 0) = ddf(0, 1) = 14.68 * p * my;

	return ddf / (yield_force * yield_force.t());
}
```

New surfaces can be crafted on request. Please contact me.