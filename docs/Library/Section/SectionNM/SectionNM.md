# SectionNM

$$N$$-$$M$$ Interaction Abstract Section

## Reference

1. [10.1007/978-94-007-6573-3_3](http://dx.doi.org/10.1007/978-94-007-6573-3_3)
2. [10.1002/nme.1620371506](https://doi.org/10.1002/nme.1620371506)

Please note the formulation is similar but different from the one shown in the above references.

## Remarks

Apart from the provided sections, other interaction surfaces can be defined.

One can define a derived class based on `NonlinearNM` and implement methods.

```cpp
[[nodiscard]] virtual double compute_f(const vec&, double) const = 0;
[[nodiscard]] virtual double compute_dh(const vec&, double) const = 0;
[[nodiscard]] virtual vec compute_df(const vec&, double) const = 0;
[[nodiscard]] virtual mat compute_ddf(const vec&, double) const = 0;
```

All methods take the normalised shifted resistance $$\mathbf{s}=\mathbf{q}-\mathbf{\beta}$$ and equivalent plastic 
strain $$\alpha$$ as input where $$\mathbf{q}$$ is the normalised nodal resistance and $$\mathbf{\beta}$$ is the back 
resistance which is similar to the concept of back stress.

For example, the [`NM2D2`](NM2D2.md) section implements the above methods as follows.

```cpp
double NM2D2::compute_f(const vec& s, const double alpha) const {
    const auto iso_factor = std::max(datum::eps, 1. + h * alpha);

    const auto p = s(0) / iso_factor;
    const auto ms = s(1) / iso_factor;

    auto f = -c;
    for(auto I = 0llu; I < para_set.n_rows; ++I) f += evaluate(p, ms, para_set.row(I));

    return f;
}

double NM2D2::compute_dh(const vec& s, const double alpha) const {
    const auto iso_factor = std::max(datum::eps, 1. + h * alpha);

    const auto p = s(0) / iso_factor;
    const auto ms = s(1) / iso_factor;

    vec df(2, fill::zeros);

    for(auto I = 0llu; I < para_set.n_rows; ++I) for(auto J = 0llu; J < df.n_elem; ++J) df(J) += evaluate(p, ms, differentiate(para_set.row(I), J, 1));

    return -h * pow(iso_factor, -2.) * dot(df, s);
}

vec NM2D2::compute_df(const vec& s, const double alpha) const {
    const auto iso_factor = std::max(datum::eps, 1. + h * alpha);

    const auto p = s(0) / iso_factor;
    const auto ms = s(1) / iso_factor;

    vec df(2, fill::zeros);

    for(auto I = 0llu; I < para_set.n_rows; ++I) for(auto J = 0llu; J < df.n_elem; ++J) df(J) += evaluate(p, ms, differentiate(para_set.row(I), J, 1));

    return df / iso_factor;
}

mat NM2D2::compute_ddf(const vec& s, const double alpha) const {
    const auto iso_factor = std::max(datum::eps, 1. + h * alpha);

    const auto p = s(0) / iso_factor;
    const auto ms = s(1) / iso_factor;

    mat ddf(2, 2, fill::zeros);

    for(auto I = 0llu; I < para_set.n_rows; ++I)
        for(auto J = 0llu; J < ddf.n_rows; ++J) {
            const auto dfj = differentiate(para_set.row(I), J, 1);
            for(auto K = 0llu; K < ddf.n_cols; ++K) ddf(J, K) += evaluate(p, ms, differentiate(dfj, K, 1));
        }

    return ddf * pow(iso_factor, -2.);
}
```

New surfaces can be crafted on request. Please contact me.