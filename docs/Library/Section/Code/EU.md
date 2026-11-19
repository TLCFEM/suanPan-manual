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
2. Check [validation](EU.pdf) for accuracy validations.

## Adjusted Sections

The nominal `EU` registry uses the published nominal dimensions of each shape. The rectangular I-section idealization
ignores root fillets and flange taper, so the area, moments of inertia and section moduli computed from the nominal
geometry differ from the values tabulated in EN 10365:2017.

The adjusted registry keeps the same designations but replaces the nominal dimensions with effective dimensions
optimized against the tabulated section properties. Use the `A` suffix to select the adjusted registry.

```text title="Adjusted EU"
section EU2DA (1) (2) (3) [4] [5] [6]
section EU3DA (1) (2) (3) [4] [5] [6] [7]
# (1) string, designation
# (2) int, unique tag
# (3) int, material model tag
# [4] double, scale, default: 1.0
# [5] int, number of integration points, default: 6
# [6] double, eccentricity (eccentricity of y axis for 3D), default: 0.0
# [7] double, eccentricity of z axis, default: 0.0
```

The arguments are identical to the corresponding `EU2D` and `EU3D` commands. For example:

```text
section EU2DA HEA200 1 1
section EU3DA IPE300 2 1
```

### What Is Changed

- The section properties are extracted from the [Dlubal cross-section database](https://www.dlubal.com/en/cross-section-properties/series-he-a-en-10365-2017-arcelormittal-2018,series-he-b-en-10365-2017-arcelormittal-2018,series-he-m-en-10365-2017-arcelormittal-2018,series-ipe-en-10365-2017-arcelormittal-2018)
  (EN 10365:2017, ArcelorMittal 2018) and stored in [`EU-Sections.csv`](EU-Sections.csv).
- The CSV contains the nominal dimensions `h`, `b`, `tw`, `tf`, the root radius `r1`, and the tabulated properties
  `A`, `I_strong`, `I_weak`, `W_strong`, `W_weak`, `Wpl_strong` and `Wpl_weak` for all HEA, HEB, HEM and IPE
  designations. The strong/weak labels avoid the EN `y`/`z` axis naming, where `y` is the strong axis.
- `eu_registry_generator.py` adjusts the flange width, flange thickness, web depth and web thickness so that the
  rectangular idealization reproduces `A`, `Ix`, `Iy`, `Zx` and `Zy`. Equal flanges are kept equal.
- Every adjusted dimension stays within 10 % of its nominal value.
- The nominal `EU2D`/`EU3D` registries are unchanged and still use the published nominal geometry.
- Dlubal reports the strong axis as `y` and the weak axis as `z`; in suanPan the strong axis is `x`.

### What Is Achieved

- For all 90 HEA, HEB, HEM and IPE sections, the error of the area and of the strong-axis properties (`A`, `Ix`, `Zx`)
  is below 0.8 %. The largest weak-axis error (`Iy`, `Zy`) is 1.0 %.
- The overall maximum property error is 1.0 %, compared with errors of several percent when the nominal dimensions
  are used directly.
- The adjusted dimensions remain close to the nominal geometry: the section depth changes by less than 1.5 % and the
  flange width by less than 3 %.

The adjusted dimensions are effective dimensions for the idealization, not a replacement for the EN 10365 geometry.
The computed properties still depend on the number of integration points; see the [validation](EU.pdf) for the
numerical accuracy of the section integration.

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

The same designations are accepted by the adjusted `EU2DA` and `EU3DA` commands.
