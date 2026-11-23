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

1. By default, millimeter is used as length unit, if users want to switch to another unit, set `scale` to corresponding values.
   For example, to use meter, `scale=0.001`, to use inch, `scale=1/25.4=0.03937007874`.
2. Check [validation](EU.pdf) for accuracy validations.

## Adjusted Sections

The nominal `EU` registry uses the published nominal dimensions of each shape.
The rectangular I-section idealization ignores root fillets and flange taper, so the area, moments of inertia and section moduli computed from the nominal geometry differ from the values tabulated in EN 10365:2017.

The adjusted registry keeps the same designations but replaces the nominal dimensions with effective dimensions optimized against the tabulated section properties.
Use the `A` suffix to select the adjusted registry.

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

The arguments are identical to the corresponding `EU2D` and `EU3D` commands.
For example:

```text
section EU2DA HEA200 1 1
section EU3DA IPE300 2 1
section EU2DA UB203X133X25 3 1
section EU3DA UBP305X305X110 4 1
```

### What Is Changed

- The section properties are extracted from the Dlubal cross-section database ([HEA, HEB, HEM and IPE](https://www.dlubal.com/en/cross-section-properties/series-he-a-en-10365-2017-arcelormittal-2018,series-he-b-en-10365-2017-arcelormittal-2018,series-he-m-en-10365-2017-arcelormittal-2018,series-ipe-en-10365-2017-arcelormittal-2018) and [UB, UC and UBP](https://www.dlubal.com/en/cross-section-properties/series-ub-en-10365-2017-arcelormittal-2018,series-uc-en-10365-2017-arcelormittal-2018,series-ubp-en-10365-2017-arcelormittal-2018)), both EN 10365:2017, ArcelorMittal 2018.
- [`eu.csv`](eu.csv) contains the properties of all HEA, HEB, HEM, IPE, UB, UC and UBP designations.
  It stores the nominal dimensions `h`, `b`, `tw`, `tf`, the root radius `r1`, and the tabulated properties `A`, `I_strong`, `I_weak`, `W_strong`, `W_weak`, `Wpl_strong` and `Wpl_weak`.
  The strong/weak labels avoid the EN `y`/`z` axis naming, where `y` is the strong axis.
- `eu_registry_generator.py` adjusts the flange width, flange thickness, web depth and web thickness so that the rectangular idealization reproduces `A`, `Ix`, `Iy`, `Zx` and `Zy`.
  Equal flanges are kept equal.
- Every adjusted dimension stays within 10 % of its nominal value.
- The nominal `EU2D`/`EU3D` registries use the published nominal geometry.
- Dlubal reports the strong axis as `y` and the weak axis as `z`; in suanPan the strong axis is `x`.

### What Is Achieved

- For all 290 HEA, HEB, HEM, IPE, UB, UC and UBP sections, the error of the area and of the strong-axis properties (`A`, `Ix`, `Zx`) is below 0.8 %; it is below 0.4 % for the UB, UC and UBP series.
  The largest weak-axis error (`Iy`, `Zy`) is 1.0 %.
- The overall maximum property error is 1.0 %, compared with errors of several percent when the nominal dimensions are used directly.
- The adjusted dimensions remain close to the nominal geometry: the section depth changes by less than 1.5 % and the flange width by less than 3 %.

The adjusted dimensions are effective dimensions for the idealization, not a replacement for the EN 10365 geometry.
The computed properties still depend on the number of integration points; see the [validation](EU.pdf) for the numerical accuracy of the section integration.

## Supported Designations

The following tables list the designations taken from EN 10365:2017 (ArcelorMittal 2018).
The same designations are accepted by the nominal `EU2D`/`EU3D` and adjusted `EU2DA`/`EU3DA` commands.

### HEA, HEB, HEM and IPE

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

### UB

| UB | UB | UB | UB |
|:---|:---|:---|:---|
| UB127X76X13 | UB152X89X16 | UB178X102X19 | UB203X102X23 |
| UB203X133X25 | UB203X133X30 | UB254X102X22 | UB254X102X25 |
| UB254X102X28 | UB254X146X31 | UB254X146X37 | UB254X146X43 |
| UB305X102X25 | UB305X102X28 | UB305X102X33 | UB305X127X37 |
| UB305X127X42 | UB305X127X48 | UB305X165X40 | UB305X165X46 |
| UB305X165X54 | UB356X127X33 | UB356X127X39 | UB356X171X45 |
| UB356X171X51 | UB356X171X57 | UB356X171X67 | UB406X140X39 |
| UB406X140X46 | UB406X140X53 | UB406X178X54 | UB406X178X60 |
| UB406X178X67 | UB406X178X74 | UB406X178X85 | UB457X152X52 |
| UB457X152X60 | UB457X152X67 | UB457X152X74 | UB457X152X82 |
| UB457X191X67 | UB457X191X74 | UB457X191X82 | UB457X191X89 |
| UB457X191X98 | UB457X191X106 | UB533X165X66 | UB533X165X74 |
| UB533X165X85 | UB533X210X82 | UB533X210X92 | UB533X210X101 |
| UB533X210X109 | UB533X210X122 | UB533X210X138 | UB610X178X82 |
| UB610X178X92 | UB610X229X101 | UB610X229X113 | UB610X229X125 |
| UB610X229X140 | UB610X229X153 | UB610X305X149 | UB610X305X179 |
| UB610X305X238 | UB686X254X125 | UB686X254X140 | UB686X254X152 |
| UB686X254X170 | UB686X254X192 | UB762X267X134 | UB762X267X147 |
| UB762X267X173 | UB762X267X197 | UB762X267X220 | UB838X292X176 |
| UB838X292X194 | UB838X292X226 | UB838X292X251 | UB914X305X201 |
| UB914X305X224 | UB914X305X238 | UB914X305X253 | UB914X305X271 |
| UB914X305X289 | UB914X305X313 | UB914X305X345 | UB914X305X381 |
| UB914X305X425 | UB914X305X474 | UB914X305X521 | UB914X305X576 |
| UB920X420X344 | UB920X420X368 | UB920X420X390 | UB920X420X420 |
| UB920X420X449 | UB920X420X491 | UB920X420X537 | UB920X420X588 |
| UB920X420X656 | UB920X420X725 | UB920X420X787 | UB920X420X970 |
| UB920X420X1077 | UB920X420X1194 | UB920X420X1269 | UB920X420X1377 |
| UB1000X400X296 | UB1000X400X321 | UB1000X400X371 | UB1000X400X412 |
| UB1000X400X443 | UB1000X400X483 | UB1000X400X539 | UB1000X400X554 |
| UB1000X400X591 | UB1000X400X642 | UB1000X400X748 | UB1000X400X883 |
| UB1000X400X976 | UB1016X305X222 | UB1016X305X249 | UB1016X305X272 |
| UB1016X305X314 | UB1016X305X350 | UB1016X305X393 | UB1016X305X415 |
| UB1016X305X438 | UB1016X305X494 | UB1016X305X584 | UB1100X400X343 |
| UB1100X400X390 | UB1100X400X433 | UB1100X400X499 | UB1100X400X548 |
| UB1100X400X607 |  |  |  |

### UC

| UC | UC | UC |
|:---|:---|:---|
| UC152X152X23 | UC152X152X30 | UC152X152X37 |
| UC152X152X44 | UC152X152X51 | UC203X203X46 |
| UC203X203X52 | UC203X203X60 | UC203X203X71 |
| UC203X203X86 | UC203X203X100 | UC254X254X73 |
| UC254X254X89 | UC254X254X107 | UC254X254X132 |
| UC254X254X167 | UC305X305X97 | UC305X305X118 |
| UC305X305X137 | UC305X305X158 | UC305X305X198 |
| UC305X305X240 | UC305X305X283 | UC305X305X313 |
| UC305X305X342 | UC356X368X129 | UC356X368X153 |
| UC356X368X177 | UC356X368X202 | UC356X406X235 |
| UC356X406X287 | UC356X406X340 | UC356X406X393 |
| UC356X406X467 | UC356X406X509 | UC356X406X551 |
| UC356X406X592 | UC356X406X634 | UC356X406X677 |
| UC356X406X744 | UC356X406X818 | UC356X406X900 |
| UC356X406X990 | UC356X406X1086 | UC356X406X1202 |
| UC356X406X1299 |  |  |

### UBP

| UBP | UBP |
|:---|:---|
| UBP203X203X45 | UBP203X203X54 |
| UBP254X254X63 | UBP254X254X71 |
| UBP254X254X85 | UBP305X305X79 |
| UBP305X305X88 | UBP305X305X95 |
| UBP305X305X110 | UBP305X305X126 |
| UBP305X305X149 | UBP305X305X186 |
| UBP305X305X223 | UBP356X368X109 |
| UBP356X368X133 | UBP356X368X152 |
| UBP356X368X174 |  |

All designations are available through both the nominal `EU2D`/`EU3D` and the adjusted `EU2DA`/`EU3DA` commands.
