# EU

Eurocode 3 Sections

**See [Eccentricity](../Eccentricity.md) for more details.**

```
section EU2D (1) (2) (3) [4] [5] [6]
# (1) string, designation
# (2) int, unique tag
# (3) int, material model tag
# [4] double, scale, default: 1.0
# [5] int, number of integration points, default: 6
# [6] double, eccentricity, default: 0.0

section EU3D (1) (2) (3) [4] [5] [6] [7]
# (1) string, designation
# (2) int, unique tag
# (3) int, material model tag
# [4] double, scale, default: 1.0
# [5] int, number of integration points, default: 6
# [6] double, eccentricity of y axis, default: 0.0
# [7] double, eccentricity of z axis, default: 0.0
```

## Remarks

1. By default, millimeter is used as length unit, if users want to switch to another unit, set `scale` to corresponding
   values. For example, to use meter, `scale=0.001`, to use inch, `scale=1/25.4=0.03937007874`.

## Supported Designations

| HEA     | HEB     | HEM     | IPE    |
|:--------|:--------|:--------|:-------|
| HEA100  | HEB100  | HEM100  | IPE80  |
| HEA120  | HEB120  | HEM120  | IPE100 |
| HEA140  | HEB140  | HEM140  | IPE120 |
| HEA160  | HEB160  | HEM160  | IPE140 |
| HEA180  | HEB180  | HEM180  | IPE160 |
| HEA200  | HEB200  | HEM200  | IPE180 |
| HEA220  | HEB220  | HEM220  | IPE200 |
| HEA240  | HEB240  | HEM240  | IPE220 |
| HEA260  | HEB260  | HEM260  | IPE240 |
| HEA280  | HEB280  | HEM280  | IPE270 |
| HEA300  | HEB300  | HEM300  | IPE300 |
| HEA320  | HEB320  | HEM320  | IPE330 |
| HEA340  | HEB340  | HEM340  | IPE360 |
| HEA360  | HEB360  | HEM360  | IPE400 |
| HEA400  | HEB400  | HEM400  | IPE450 |
| HEA450  | HEB450  | HEM450  | IPE500 |
| HEA500  | HEB500  | HEM500  | IPE550 |
| HEA550  | HEB550  | HEM550  | IPE600 |
| HEA600  | HEB600  | HEM600  |        |
| HEA650  | HEB650  | HEM650  |        |
| HEA700  | HEB700  | HEM700  |        |
| HEA800  | HEB800  | HEM800  |        |
| HEA900  | HEB900  | HEM900  |        |
| HEA1000 | HEB1000 | HEM1000 |        |
