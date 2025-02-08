## AISC

A collection of `W`, `M`, `S`, `HP`, `WT`, `MT`, `ST` sections are predefined using inch as default length unit.

**See [Eccentricity](../Eccentricity.md) for more details.**

## Syntax

To define a section, users can use the following commands.

```
section US2D (1) (2) (3) [4] [5] [6]
# (1) string, designation
# (2) int, unique tag
# (3) int, material model tag
# [4] double, scale, default: 1.0
# [5] int, number of integration points along web height, default: 6
# [6] double, eccentricity, default: 0.0

section US3D (1) (2) (3) [4] [5] [6] [7]
# (1) string, designation
# (2) int, unique tag
# (3) int, material model tag
# [4] double, scale, default: 1.0
# [5] int, number of integration points along web height and flange width, default: 6
# [6] double, eccentricity of y axis, default: 0.0
# [7] double, eccentricity of z axis, default: 0.0
```

[available from v3.2]

Some T-sections are placed at the centre of the web, which is not always desired. Use `US2DC` and `US3DC` to automatically recenter the section to its barycenter.

```
section US2DC (1) (2) (3) [4] [5]
section US3DC (1) (2) (3) [4] [5]
# (1) string, designation
# (2) int, unique tag
# (3) int, material model tag
# [4] double, scale, default: 1.0
# [5] int, number of integration points along web height (and flange width for 3D), default: 6
```

## Remarks

1. By default, inch is used as length unit, if users want to switch to another unit, set `scale` to corresponding
   values. For example, to use millimeter, `scale=25.4`.
2. For 2D sections, the number of integration points is set to two using Gauss quadrature for flange.
3. For 3D sections, along web/flange thickness, one integration point is used. along flange width and web height, the
   same number of integration points is used as defined by user.

**There will be discrepancies between design section properties and numerical section properties.**
**Use with caution and check the [validation](US.pdf).**

## Supported Designations

The following designations from [AISC Shapes Database v16.0](https://www.aisc.org/publications/steel-construction-manual-resources/16th-ed-steel-construction-manual/aisc-shapes-database-v16.0/) is supported.

| W       | M          | S        | HP       | WT           | MT         | ST          | HSS (Rectangle)     | HSS (Circle)    |
|:--------|:-----------|:---------|:---------|:-------------|:-----------|:------------|:--------------------|:----------------|
| W44X408 | M12.5X12.4 | S24X121  | HP18X204 | WT22X167.5   | MT6.25X6.2 | ST12X60.5   | HSS34X10X1          | HSS28.000X1.000 |
| W44X368 | M12.5X11.6 | S24X106  | HP18X181 | WT22X145     | MT6.25X5.8 | ST12X53     | HSS34X10X7/8        | HSS28.000X0.875 |
| W44X335 | M12X11.8   | S24X100  | HP18X157 | WT22X131     | MT6X5.9    | ST12X50     | HSS34X10X3/4        | HSS28.000X0.750 |
| W44X290 | M12X10.8   | S24X90   | HP18X135 | WT22X115     | MT6X5.4    | ST12X45     | HSS34X10X5/8        | HSS28.000X0.625 |
| W44X262 | M12X10     | S24X80   | HP16X183 | WT20X327.5   | MT6X5      | ST12X40     | HSS30X10X1          | HSS28.000X0.500 |
| W44X230 | M10X9      | S20X96   | HP16X162 | WT20X296.5   | MT5X4.5    | ST10X48     | HSS30X10X7/8        | HSS28.000X0.375 |
| W40X655 | M10X8      | S20X86   | HP16X141 | WT20X251.5   | MT5X4      | ST10X43     | HSS30X10X3/4        | HSS26.000X0.750 |
| W40X593 | M10X7.5    | S20X75   | HP16X121 | WT20X215.5   | MT5X3.75   | ST10X37.5   | HSS30X10X5/8        | HSS26.000X0.625 |
| W40X503 | M8X6.5     | S20X66   | HP16X101 | WT20X198.5   | MT4X3.25   | ST10X33     | HSS30X10X1/2        | HSS26.000X0.500 |
| W40X431 | M8X6.2     | S18X70   | HP16X88  | WT20X186     | MT4X3.1    | ST9X35      | HSS24X20X3/4        | HSS26.000X0.375 |
| W40X397 | M6X4.4     | S18X54.7 | HP14X117 | WT20X181     | MT3X2.2    | ST9X27.35   | HSS24X20X5/8        | HSS26.000X0.313 |
| W40X372 | M6X3.7     | S15X50   | HP14X102 | WT20X162     | MT3X1.85   | ST7.5X25    | HSS24X20X1/2        | HSS24.000X1.000 |
| W40X362 | M5X18.9    | S15X42.9 | HP14X89  | WT20X148.5   | MT2.5X9.45 | ST7.5X21.45 | HSS24X20X3/8        | HSS24.000X0.875 |
| W40X324 | M4X6       | S12X50   | HP14X73  | WT20X138.5   | MT2X3      | ST6X25      | HSS24X20X5/16       | HSS24.000X0.750 |
| W40X297 | M4X4.08    | S12X40.8 | HP12X89  | WT20X124.5   |            | ST6X20.4    | HSS24X18X3/4        | HSS24.000X0.625 |
| W40X277 | M3X2.9     | S12X35   | HP12X84  | WT20X107.5   |            | ST6X17.5    | HSS24X18X5/8        | HSS24.000X0.500 |
| W40X249 | MT6.25X6.2 | S12X31.8 | HP12X74  | WT20X99.5    |            | ST6X15.9    | HSS24X18X1/2        | HSS24.000X0.375 |
| W40X215 | MT6.25X5.8 | S10X35   | HP12X63  | WT20X196     |            | ST5X17.5    | HSS24X18X3/8        | HSS24.000X0.313 |
| W40X199 | MT6X5.9    | S10X25.4 | HP12X53  | WT20X165.5   |            | ST5X12.7    | HSS24X18X5/16       | HSS22.000X0.750 |
| W40X392 | MT6X5.4    | S8X23    | HP10X57  | WT20X163.5   |            | ST4X11.5    | HSS24X16X3/4        | HSS22.000X0.625 |
| W40X331 | MT6X5      | S8X18.4  | HP10X42  | WT20X147     |            | ST4X9.2     | HSS24X16X5/8        | HSS22.000X0.500 |
| W40X327 | MT5X4.5    | S6X17.25 | HP8X36   | WT20X139     |            | ST3X8.6     | HSS24X16X1/2        | HSS22.000X0.375 |
| W40X294 | MT5X4      | S6X12.5  |          | WT20X132     |            | ST3X6.25    | HSS24X16X3/8        | HSS22.000X0.313 |
| W40X278 | MT5X3.75   | S5X10    |          | WT20X117.5   |            | ST2.5X5     | HSS24X16X5/16       | HSS20.000X1.000 |
| W40X264 | MT4X3.25   | S4X9.5   |          | WT20X105.5   |            | ST2X4.75    | HSS24X14X3/4        | HSS20.000X0.875 |
| W40X235 | MT4X3.1    | S4X7.7   |          | WT20X91.5    |            | ST2X3.85    | HSS24X14X5/8        | HSS20.000X0.750 |
| W40X211 | MT3X2.2    | S3X7.5   |          | WT20X83.5    |            | ST1.5X3.75  | HSS24X14X1/2        | HSS20.000X0.625 |
| W40X183 | MT3X1.85   | S3X5.7   |          | WT20X74.5    |            | ST1.5X2.85  | HSS24X14X3/8        | HSS20.000X0.500 |
| W40X167 | MT2.5X9.45 |          |          | WT18X462.5   |            |             | HSS24X14X5/16       | HSS20.000X0.375 |
| W40X149 | MT2X3      |          |          | WT18X426.5   |            |             | HSS24X14X1/4        | HSS20.000X0.313 |
| W36X925 |            |          |          | WT18X401     |            |             | HSS24X12X1          | HSS20.000X0.250 |
| W36X853 |            |          |          | WT18X361.5   |            |             | HSS24X12X7/8        | HSS18.000X1.000 |
| W36X802 |            |          |          | WT18X326     |            |             | HSS24X12X3/4        | HSS18.000X0.875 |
| W36X723 |            |          |          | WT18X264.5   |            |             | HSS24X12X5/8        | HSS18.000X0.750 |
| W36X652 |            |          |          | WT18X243.5   |            |             | HSS24X12X1/2        | HSS18.000X0.625 |
| W36X529 |            |          |          | WT18X220.5   |            |             | HSS24X12X3/8        | HSS18.000X0.500 |
| W36X487 |            |          |          | WT18X197.5   |            |             | HSS24X12X5/16       | HSS18.000X0.375 |
| W36X441 |            |          |          | WT18X180.5   |            |             | HSS24X12X1/4        | HSS18.000X0.313 |
| W36X395 |            |          |          | WT18X165     |            |             | HSS24X8X1/2         | HSS18.000X0.250 |
| W36X361 |            |          |          | WT18X151     |            |             | HSS24X8X3/8         | HSS16.000X1.000 |
| W36X330 |            |          |          | WT18X141     |            |             | HSS24X8X5/16        | HSS16.000X0.875 |
| W36X302 |            |          |          | WT18X131     |            |             | HSS24X8X1/4         | HSS16.000X0.750 |
| W36X282 |            |          |          | WT18X123.5   |            |             | HSS22X22X1          | HSS16.000X0.625 |
| W36X262 |            |          |          | WT18X115.5   |            |             | HSS22X22X7/8        | HSS16.000X0.500 |
| W36X247 |            |          |          | WT18X128     |            |             | HSS22X22X3/4        | HSS16.000X0.438 |
| W36X231 |            |          |          | WT18X116     |            |             | HSS22X22X5/8        | HSS16.000X0.375 |
| W36X387 |            |          |          | WT18X105     |            |             | HSS22X22X1/2        | HSS16.000X0.312 |
| W36X350 |            |          |          | WT18X97      |            |             | HSS22X20X3/4        | HSS16.000X0.250 |
| W36X318 |            |          |          | WT18X91      |            |             | HSS22X20X5/8        | HSS14.000X1.000 |
| W36X286 |            |          |          | WT18X85      |            |             | HSS22X20X1/2        | HSS14.000X0.875 |
| W36X256 |            |          |          | WT18X80      |            |             | HSS22X20X3/8        | HSS14.000X0.750 |
| W36X232 |            |          |          | WT18X75      |            |             | HSS22X20X5/16       | HSS14.000X0.625 |
| W36X210 |            |          |          | WT18X67.5    |            |             | HSS22X18X3/4        | HSS14.000X0.500 |
| W36X194 |            |          |          | WT16.5X193.5 |            |             | HSS22X18X5/8        | HSS14.000X0.375 |
| W36X182 |            |          |          | WT16.5X177   |            |             | HSS22X18X1/2        | HSS14.000X0.312 |
| W36X170 |            |          |          | WT16.5X159   |            |             | HSS22X18X3/8        | HSS14.000X0.250 |
| W36X160 |            |          |          | WT16.5X145.5 |            |             | HSS22X18X5/16       | HSS14.000X0.188 |
| W36X150 |            |          |          | WT16.5X131.5 |            |             | HSS22X16X3/4        | HSS13.375X0.625 |
| W36X135 |            |          |          | WT16.5X120.5 |            |             | HSS22X16X5/8        | HSS13.375X0.500 |
| W33X387 |            |          |          | WT16.5X110.5 |            |             | HSS22X16X1/2        | HSS13.375X0.375 |
| W33X354 |            |          |          | WT16.5X100.5 |            |             | HSS22X16X3/8        | HSS13.375X0.313 |
| W33X318 |            |          |          | WT16.5X84.5  |            |             | HSS22X16X5/16       | HSS13.375X0.250 |
| W33X291 |            |          |          | WT16.5X76    |            |             | HSS22X16X1/4        | HSS13.375X0.188 |
| W33X263 |            |          |          | WT16.5X70.5  |            |             | HSS22X14X3/4        | HSS12.750X0.750 |
| W33X241 |            |          |          | WT16.5X65    |            |             | HSS22X14X5/8        | HSS12.750X0.625 |
| W33X221 |            |          |          | WT16.5X59    |            |             | HSS22X14X1/2        | HSS12.750X0.500 |
| W33X201 |            |          |          | WT15X195.5   |            |             | HSS22X14X3/8        | HSS12.750X0.375 |
| W33X169 |            |          |          | WT15X178.5   |            |             | HSS22X14X5/16       | HSS12.750X0.250 |
| W33X152 |            |          |          | WT15X163     |            |             | HSS22X14X1/4        | HSS12.750X0.188 |
| W33X141 |            |          |          | WT15X146     |            |             | HSS22X10X5/8        | HSS12.000X0.625 |
| W33X130 |            |          |          | WT15X130.5   |            |             | HSS22X10X1/2        | HSS12.000X0.500 |
| W33X118 |            |          |          | WT15X117.5   |            |             | HSS22X10X3/8        | HSS12.000X0.375 |
| W30X391 |            |          |          | WT15X105.5   |            |             | HSS22X10X5/16       | HSS12.000X0.250 |
| W30X357 |            |          |          | WT15X95.5    |            |             | HSS22X10X1/4        | HSS11.750X0.625 |
| W30X326 |            |          |          | WT15X86.5    |            |             | HSS20X20X1          | HSS11.750X0.500 |
| W30X292 |            |          |          | WT15X74      |            |             | HSS20X20X7/8        | HSS11.750X0.375 |
| W30X261 |            |          |          | WT15X66      |            |             | HSS20X20X3/4        | HSS11.750X0.337 |
| W30X235 |            |          |          | WT15X62      |            |             | HSS20X20X5/8        | HSS11.750X0.250 |
| W30X211 |            |          |          | WT15X58      |            |             | HSS20X20X1/2        | HSS10.750X0.625 |
| W30X191 |            |          |          | WT15X54      |            |             | HSS20X20X3/8        | HSS10.750X0.500 |
| W30X173 |            |          |          | WT15X49.5    |            |             | HSS20X20X5/16       | HSS10.750X0.375 |
| W30X148 |            |          |          | WT15X45      |            |             | HSS20X16X3/4        | HSS10.750X0.313 |
| W30X132 |            |          |          | WT13.5X269.5 |            |             | HSS20X16X5/8        | HSS10.750X0.250 |
| W30X124 |            |          |          | WT13.5X184   |            |             | HSS20X16X1/2        | HSS10.750X0.188 |
| W30X116 |            |          |          | WT13.5X168   |            |             | HSS20X16X3/8        | HSS10.000X0.625 |
| W30X108 |            |          |          | WT13.5X153.5 |            |             | HSS20X16X5/16       | HSS10.000X0.500 |
| W30X99  |            |          |          | WT13.5X140.5 |            |             | HSS20X16X1/4        | HSS10.000X0.375 |
| W30X90  |            |          |          | WT13.5X129   |            |             | HSS20X12X1          | HSS10.000X0.312 |
| W27X539 |            |          |          | WT13.5X117.5 |            |             | HSS20X12X7/8        | HSS10.000X0.250 |
| W27X368 |            |          |          | WT13.5X108.5 |            |             | HSS20X12X3/4        | HSS10.000X0.188 |
| W27X336 |            |          |          | WT13.5X97    |            |             | HSS20X12X5/8        | HSS9.625X0.625  |
| W27X307 |            |          |          | WT13.5X89    |            |             | HSS20X12X1/2        | HSS9.625X0.500  |
| W27X281 |            |          |          | WT13.5X80.5  |            |             | HSS20X12X3/8        | HSS9.625X0.375  |
| W27X258 |            |          |          | WT13.5X73    |            |             | HSS20X12X5/16       | HSS9.625X0.312  |
| W27X235 |            |          |          | WT13.5X64.5  |            |             | HSS20X8X1           | HSS9.625X0.250  |
| W27X217 |            |          |          | WT13.5X57    |            |             | HSS20X8X7/8         | HSS9.625X0.188  |
| W27X194 |            |          |          | WT13.5X51    |            |             | HSS20X8X3/4         | HSS8.625X0.625  |
| W27X178 |            |          |          | WT13.5X47    |            |             | HSS20X8X5/8         | HSS8.625X0.500  |
| W27X161 |            |          |          | WT13.5X42    |            |             | HSS20X8X1/2         | HSS8.625X0.375  |
| W27X146 |            |          |          | WT12X185     |            |             | HSS20X8X3/8         | HSS8.625X0.322  |
| W27X129 |            |          |          | WT12X167.5   |            |             | HSS20X8X5/16        | HSS8.625X0.250  |
| W27X114 |            |          |          | WT12X153     |            |             | HSS20X6X5/8         | HSS8.625X0.188  |
| W27X102 |            |          |          | WT12X139.5   |            |             | HSS20X6X1/2         | HSS7.500X0.500  |
| W27X94  |            |          |          | WT12X125     |            |             | HSS20X6X3/8         | HSS7.500X0.375  |
| W27X84  |            |          |          | WT12X114.5   |            |             | HSS20X6X5/16        | HSS7.500X0.312  |
| W24X370 |            |          |          | WT12X103.5   |            |             | HSS20X6X1/4         | HSS7.500X0.250  |
| W24X335 |            |          |          | WT12X96      |            |             | HSS20X4X1/2         | HSS7.500X0.188  |
| W24X306 |            |          |          | WT12X88      |            |             | HSS20X4X3/8         | HSS7.000X0.500  |
| W24X279 |            |          |          | WT12X81      |            |             | HSS20X4X5/16        | HSS7.000X0.375  |
| W24X250 |            |          |          | WT12X73      |            |             | HSS20X4X1/4         | HSS7.000X0.312  |
| W24X229 |            |          |          | WT12X65.5    |            |             | HSS18X18X1          | HSS7.000X0.250  |
| W24X207 |            |          |          | WT12X58.5    |            |             | HSS18X18X7/8        | HSS7.000X0.188  |
| W24X192 |            |          |          | WT12X52      |            |             | HSS18X18X3/4        | HSS7.000X0.125  |
| W24X176 |            |          |          | WT12X51.5    |            |             | HSS18X18X5/8        | HSS6.875X0.375  |
| W24X162 |            |          |          | WT12X47      |            |             | HSS18X18X1/2        | HSS6.875X0.312  |
| W24X146 |            |          |          | WT12X42      |            |             | HSS18X18X3/8        | HSS6.875X0.250  |
| W24X131 |            |          |          | WT12X38      |            |             | HSS18X18X5/16       | HSS6.875X0.188  |
| W24X117 |            |          |          | WT12X34      |            |             | HSS18X18X1/4        | HSS6.625X0.500  |
| W24X104 |            |          |          | WT12X31      |            |             | HSS18X10X5/8        | HSS6.625X0.432  |
| W24X103 |            |          |          | WT12X27.5    |            |             | HSS18X10X1/2        | HSS6.625X0.375  |
| W24X94  |            |          |          | WT10.5X137.5 |            |             | HSS18X10X3/8        | HSS6.625X0.312  |
| W24X84  |            |          |          | WT10.5X124   |            |             | HSS18X10X5/16       | HSS6.625X0.280  |
| W24X76  |            |          |          | WT10.5X111.5 |            |             | HSS18X10X1/4        | HSS6.625X0.250  |
| W24X68  |            |          |          | WT10.5X100.5 |            |             | HSS18X8X5/8         | HSS6.625X0.188  |
| W24X62  |            |          |          | WT10.5X91    |            |             | HSS18X8X1/2         | HSS6.625X0.125  |
| W24X55  |            |          |          | WT10.5X83    |            |             | HSS18X8X3/8         | HSS6.000X0.500  |
| W21X275 |            |          |          | WT10.5X73.5  |            |             | HSS18X8X5/16        | HSS6.000X0.375  |
| W21X248 |            |          |          | WT10.5X66    |            |             | HSS18X8X1/4         | HSS6.000X0.312  |
| W21X223 |            |          |          | WT10.5X61    |            |             | HSS18X6X3/4         | HSS6.000X0.280  |
| W21X201 |            |          |          | WT10.5X55.5  |            |             | HSS18X6X5/8         | HSS6.000X0.250  |
| W21X182 |            |          |          | WT10.5X50.5  |            |             | HSS18X6X1/2         | HSS6.000X0.188  |
| W21X166 |            |          |          | WT10.5X46.5  |            |             | HSS18X6X3/8         | HSS6.000X0.125  |
| W21X147 |            |          |          | WT10.5X41.5  |            |             | HSS18X6X5/16        | HSS5.563X0.500  |
| W21X132 |            |          |          | WT10.5X36.5  |            |             | HSS18X6X1/4         | HSS5.563X0.375  |
| W21X122 |            |          |          | WT10.5X34    |            |             | HSS16X16X1          | HSS5.563X0.258  |
| W21X111 |            |          |          | WT10.5X31    |            |             | HSS16X16X7/8        | HSS5.563X0.188  |
| W21X101 |            |          |          | WT10.5X27.5  |            |             | HSS16X16X3/4        | HSS5.563X0.134  |
| W21X93  |            |          |          | WT10.5X24    |            |             | HSS16X16X5/8        | HSS5.500X0.500  |
| W21X83  |            |          |          | WT10.5X28.5  |            |             | HSS16X16X1/2        | HSS5.500X0.375  |
| W21X73  |            |          |          | WT10.5X25    |            |             | HSS16X16X3/8        | HSS5.500X0.258  |
| W21X68  |            |          |          | WT10.5X22    |            |             | HSS16X16X5/16       | HSS5.000X0.500  |
| W21X62  |            |          |          | WT9X155.5    |            |             | HSS16X16X1/4        | HSS5.000X0.375  |
| W21X55  |            |          |          | WT9X141.5    |            |             | HSS16X12X1          | HSS5.000X0.312  |
| W21X48  |            |          |          | WT9X129      |            |             | HSS16X12X7/8        | HSS5.000X0.258  |
| W21X57  |            |          |          | WT9X117      |            |             | HSS16X12X3/4        | HSS5.000X0.250  |
| W21X50  |            |          |          | WT9X105.5    |            |             | HSS16X12X5/8        | HSS5.000X0.188  |
| W21X44  |            |          |          | WT9X96       |            |             | HSS16X12X1/2        | HSS5.000X0.125  |
| W18X311 |            |          |          | WT9X87.5     |            |             | HSS16X12X3/8        | HSS4.500X0.375  |
| W18X283 |            |          |          | WT9X79       |            |             | HSS16X12X5/16       | HSS4.500X0.337  |
| W18X258 |            |          |          | WT9X71.5     |            |             | HSS16X10X5/8        | HSS4.500X0.237  |
| W18X234 |            |          |          | WT9X65       |            |             | HSS16X10X1/2        | HSS4.500X0.188  |
| W18X211 |            |          |          | WT9X59.5     |            |             | HSS16X10X3/8        | HSS4.500X0.125  |
| W18X192 |            |          |          | WT9X53       |            |             | HSS16X10X5/16       | HSS4.000X0.313  |
| W18X175 |            |          |          | WT9X48.5     |            |             | HSS16X10X1/4        | HSS4.000X0.250  |
| W18X158 |            |          |          | WT9X43       |            |             | HSS16X8X7/8         | HSS4.000X0.237  |
| W18X143 |            |          |          | WT9X38       |            |             | HSS16X8X3/4         | HSS4.000X0.226  |
| W18X130 |            |          |          | WT9X35.5     |            |             | HSS16X8X5/8         | HSS4.000X0.220  |
| W18X119 |            |          |          | WT9X32.5     |            |             | HSS16X8X1/2         | HSS4.000X0.188  |
| W18X106 |            |          |          | WT9X30       |            |             | HSS16X8X3/8         | HSS4.000X0.125  |
| W18X97  |            |          |          | WT9X27.5     |            |             | HSS16X8X5/16        | HSS3.500X0.313  |
| W18X86  |            |          |          | WT9X25       |            |             | HSS16X8X1/4         | HSS3.500X0.300  |
| W18X76  |            |          |          | WT9X23       |            |             | HSS16X6X5/8         | HSS3.500X0.250  |
| W18X71  |            |          |          | WT9X20       |            |             | HSS16X6X1/2         | HSS3.500X0.216  |
| W18X65  |            |          |          | WT9X17.5     |            |             | HSS16X6X3/8         | HSS3.500X0.203  |
| W18X60  |            |          |          | WT8X50       |            |             | HSS16X6X5/16        | HSS3.500X0.188  |
| W18X55  |            |          |          | WT8X44.5     |            |             | HSS16X6X1/4         | HSS3.500X0.125  |
| W18X50  |            |          |          | WT8X38.5     |            |             | HSS16X6X3/16        | HSS3.000X0.250  |
| W18X46  |            |          |          | WT8X33.5     |            |             | HSS16X4X5/8         | HSS3.000X0.216  |
| W18X40  |            |          |          | WT8X28.5     |            |             | HSS16X4X1/2         | HSS3.000X0.203  |
| W18X35  |            |          |          | WT8X25       |            |             | HSS16X4X3/8         | HSS3.000X0.188  |
| W16X100 |            |          |          | WT8X22.5     |            |             | HSS16X4X5/16        | HSS3.000X0.152  |
| W16X89  |            |          |          | WT8X20       |            |             | HSS16X4X1/4         | HSS3.000X0.134  |
| W16X77  |            |          |          | WT8X18       |            |             | HSS16X4X3/16        | HSS3.000X0.125  |
| W16X67  |            |          |          | WT8X15.5     |            |             | HSS14X14X1          | HSS2.875X0.250  |
| W16X57  |            |          |          | WT8X13       |            |             | HSS14X14X7/8        | HSS2.875X0.203  |
| W16X50  |            |          |          | WT7X436.5    |            |             | HSS14X14X3/4        | HSS2.875X0.188  |
| W16X45  |            |          |          | WT7X404      |            |             | HSS14X14X5/8        | HSS2.875X0.125  |
| W16X40  |            |          |          | WT7X365      |            |             | HSS14X14X1/2        | HSS2.500X0.250  |
| W16X36  |            |          |          | WT7X332.5    |            |             | HSS14X14X3/8        | HSS2.500X0.188  |
| W16X31  |            |          |          | WT7X302.5    |            |             | HSS14X14X5/16       | HSS2.500X0.125  |
| W16X26  |            |          |          | WT7X275      |            |             | HSS14X14X1/4        | HSS2.375X0.250  |
| W14X873 |            |          |          | WT7X250      |            |             | HSS14X12X5/8        | HSS2.375X0.218  |
| W14X808 |            |          |          | WT7X227.5    |            |             | HSS14X12X1/2        | HSS2.375X0.188  |
| W14X730 |            |          |          | WT7X213      |            |             | HSS14X12X3/8        | HSS2.375X0.154  |
| W14X665 |            |          |          | WT7X199      |            |             | HSS14X12X5/16       | HSS2.375X0.125  |
| W14X605 |            |          |          | WT7X185      |            |             | HSS14X12X1/4        | HSS1.900X0.188  |
| W14X550 |            |          |          | WT7X171      |            |             | HSS14X10X7/8        | HSS1.900X0.145  |
| W14X500 |            |          |          | WT7X155.5    |            |             | HSS14X10X3/4        | HSS1.900X0.120  |
| W14X455 |            |          |          | WT7X141.5    |            |             | HSS14X10X5/8        | HSS1.660X0.140  |
| W14X426 |            |          |          | WT7X128.5    |            |             | HSS14X10X1/2        |                 |
| W14X398 |            |          |          | WT7X116.5    |            |             | HSS14X10X3/8        |                 |
| W14X370 |            |          |          | WT7X105.5    |            |             | HSS14X10X5/16       |                 |
| W14X342 |            |          |          | WT7X96.5     |            |             | HSS14X10X1/4        |                 |
| W14X311 |            |          |          | WT7X88       |            |             | HSS14X8X5/8         |                 |
| W14X283 |            |          |          | WT7X79.5     |            |             | HSS14X8X1/2         |                 |
| W14X257 |            |          |          | WT7X72.5     |            |             | HSS14X8X3/8         |                 |
| W14X233 |            |          |          | WT7X66       |            |             | HSS14X8X5/16        |                 |
| W14X211 |            |          |          | WT7X60       |            |             | HSS14X8X1/4         |                 |
| W14X193 |            |          |          | WT7X54.5     |            |             | HSS14X8X3/16        |                 |
| W14X176 |            |          |          | WT7X49.5     |            |             | HSS14X6X5/8         |                 |
| W14X159 |            |          |          | WT7X45       |            |             | HSS14X6X1/2         |                 |
| W14X145 |            |          |          | WT7X41       |            |             | HSS14X6X3/8         |                 |
| W14X132 |            |          |          | WT7X37       |            |             | HSS14X6X5/16        |                 |
| W14X120 |            |          |          | WT7X34       |            |             | HSS14X6X1/4         |                 |
| W14X109 |            |          |          | WT7X30.5     |            |             | HSS14X6X3/16        |                 |
| W14X99  |            |          |          | WT7X26.5     |            |             | HSS14X4X5/8         |                 |
| W14X90  |            |          |          | WT7X24       |            |             | HSS14X4X1/2         |                 |
| W14X82  |            |          |          | WT7X21.5     |            |             | HSS14X4X3/8         |                 |
| W14X74  |            |          |          | WT7X19       |            |             | HSS14X4X5/16        |                 |
| W14X68  |            |          |          | WT7X17       |            |             | HSS14X4X1/4         |                 |
| W14X61  |            |          |          | WT7X15       |            |             | HSS14X4X3/16        |                 |
| W14X53  |            |          |          | WT7X13       |            |             | HSS12X12X1          |                 |
| W14X48  |            |          |          | WT7X11       |            |             | HSS12X12X7/8        |                 |
| W14X43  |            |          |          | WT6X168      |            |             | HSS12X12X3/4        |                 |
| W14X38  |            |          |          | WT6X152.5    |            |             | HSS12X12X5/8        |                 |
| W14X34  |            |          |          | WT6X139.5    |            |             | HSS12X12X1/2        |                 |
| W14X30  |            |          |          | WT6X126      |            |             | HSS12X12X3/8        |                 |
| W14X26  |            |          |          | WT6X115      |            |             | HSS12X12X5/16       |                 |
| W14X22  |            |          |          | WT6X105      |            |             | HSS12X12X1/4        |                 |
| W12X336 |            |          |          | WT6X95       |            |             | HSS12X12X3/16       |                 |
| W12X305 |            |          |          | WT6X85       |            |             | HSS12X10X5/8        |                 |
| W12X279 |            |          |          | WT6X76       |            |             | HSS12X10X1/2        |                 |
| W12X252 |            |          |          | WT6X68       |            |             | HSS12X10X3/8        |                 |
| W12X230 |            |          |          | WT6X60       |            |             | HSS12X10X5/16       |                 |
| W12X210 |            |          |          | WT6X53       |            |             | HSS12X10X1/4        |                 |
| W12X190 |            |          |          | WT6X48       |            |             | HSS12X10X3/16       |                 |
| W12X170 |            |          |          | WT6X43.5     |            |             | HSS12X8X5/8         |                 |
| W12X152 |            |          |          | WT6X39.5     |            |             | HSS12X8X1/2         |                 |
| W12X136 |            |          |          | WT6X36       |            |             | HSS12X8X3/8         |                 |
| W12X120 |            |          |          | WT6X32.5     |            |             | HSS12X8X5/16        |                 |
| W12X106 |            |          |          | WT6X29       |            |             | HSS12X8X1/4         |                 |
| W12X96  |            |          |          | WT6X26.5     |            |             | HSS12X8X3/16        |                 |
| W12X87  |            |          |          | WT6X25       |            |             | HSS12X6X5/8         |                 |
| W12X79  |            |          |          | WT6X22.5     |            |             | HSS12X6X1/2         |                 |
| W12X72  |            |          |          | WT6X20       |            |             | HSS12X6X3/8         |                 |
| W12X65  |            |          |          | WT6X17.5     |            |             | HSS12X6X5/16        |                 |
| W12X58  |            |          |          | WT6X15       |            |             | HSS12X6X1/4         |                 |
| W12X53  |            |          |          | WT6X13       |            |             | HSS12X6X3/16        |                 |
| W12X50  |            |          |          | WT6X11       |            |             | HSS12X4X5/8         |                 |
| W12X45  |            |          |          | WT6X9.5      |            |             | HSS12X4X1/2         |                 |
| W12X40  |            |          |          | WT6X8        |            |             | HSS12X4X3/8         |                 |
| W12X35  |            |          |          | WT6X7        |            |             | HSS12X4X5/16        |                 |
| W12X30  |            |          |          | WT5X56       |            |             | HSS12X4X1/4         |                 |
| W12X26  |            |          |          | WT5X50       |            |             | HSS12X4X3/16        |                 |
| W12X22  |            |          |          | WT5X44       |            |             | HSS12X3X5/16        |                 |
| W12X19  |            |          |          | WT5X38.5     |            |             | HSS12X3X1/4         |                 |
| W12X16  |            |          |          | WT5X34       |            |             | HSS12X3X3/16        |                 |
| W12X14  |            |          |          | WT5X30       |            |             | HSS12X2X5/16        |                 |
| W10X112 |            |          |          | WT5X27       |            |             | HSS12X2X1/4         |                 |
| W10X100 |            |          |          | WT5X24.5     |            |             | HSS12X2X3/16        |                 |
| W10X88  |            |          |          | WT5X22.5     |            |             | HSS10X10X3/4        |                 |
| W10X77  |            |          |          | WT5X19.5     |            |             | HSS10X10X5/8        |                 |
| W10X68  |            |          |          | WT5X16.5     |            |             | HSS10X10X1/2        |                 |
| W10X60  |            |          |          | WT5X15       |            |             | HSS10X10X3/8        |                 |
| W10X54  |            |          |          | WT5X13       |            |             | HSS10X10X5/16       |                 |
| W10X49  |            |          |          | WT5X11       |            |             | HSS10X10X1/4        |                 |
| W10X45  |            |          |          | WT5X9.5      |            |             | HSS10X10X3/16       |                 |
| W10X39  |            |          |          | WT5X8.5      |            |             | HSS10X8X5/8         |                 |
| W10X33  |            |          |          | WT5X7.5      |            |             | HSS10X8X1/2         |                 |
| W10X30  |            |          |          | WT5X6        |            |             | HSS10X8X3/8         |                 |
| W10X26  |            |          |          | WT4X33.5     |            |             | HSS10X8X5/16        |                 |
| W10X22  |            |          |          | WT4X29       |            |             | HSS10X8X1/4         |                 |
| W10X19  |            |          |          | WT4X24       |            |             | HSS10X8X3/16        |                 |
| W10X17  |            |          |          | WT4X20       |            |             | HSS10X6X5/8         |                 |
| W10X15  |            |          |          | WT4X17.5     |            |             | HSS10X6X1/2         |                 |
| W10X12  |            |          |          | WT4X15.5     |            |             | HSS10X6X3/8         |                 |
| W8X67   |            |          |          | WT4X14       |            |             | HSS10X6X5/16        |                 |
| W8X58   |            |          |          | WT4X12       |            |             | HSS10X6X1/4         |                 |
| W8X48   |            |          |          | WT4X10.5     |            |             | HSS10X6X3/16        |                 |
| W8X40   |            |          |          | WT4X9        |            |             | HSS10X5X3/8         |                 |
| W8X35   |            |          |          | WT4X7.5      |            |             | HSS10X5X5/16        |                 |
| W8X31   |            |          |          | WT4X6.5      |            |             | HSS10X5X1/4         |                 |
| W8X28   |            |          |          | WT4X5        |            |             | HSS10X4X5/8         |                 |
| W8X24   |            |          |          | WT3X12.5     |            |             | HSS10X4X1/2         |                 |
| W8X21   |            |          |          | WT3X10       |            |             | HSS10X4X3/8         |                 |
| W8X18   |            |          |          | WT3X7.5      |            |             | HSS10X4X5/16        |                 |
| W8X15   |            |          |          | WT3X8        |            |             | HSS10X4X1/4         |                 |
| W8X13   |            |          |          | WT3X6        |            |             | HSS10X4X3/16        |                 |
| W8X10   |            |          |          | WT3X4.5      |            |             | HSS10X4X1/8         |                 |
| W6X25   |            |          |          | WT3X4.25     |            |             | HSS10X3-1/2X3/8     |                 |
| W6X20   |            |          |          | WT2.5X9.5    |            |             | HSS10X3-1/2X5/16    |                 |
| W6X15   |            |          |          | WT2.5X8      |            |             | HSS10X3-1/2X1/4     |                 |
| W6X16   |            |          |          | WT2X6.5      |            |             | HSS10X3-1/2X3/16    |                 |
| W6X12   |            |          |          |              |            |             | HSS10X3X3/8         |                 |
| W6X9    |            |          |          |              |            |             | HSS10X3X5/16        |                 |
| W6X8.5  |            |          |          |              |            |             | HSS10X3X1/4         |                 |
| W5X19   |            |          |          |              |            |             | HSS10X3X3/16        |                 |
| W5X16   |            |          |          |              |            |             | HSS10X3X1/8         |                 |
| W4X13   |            |          |          |              |            |             | HSS10X2X3/8         |                 |
|         |            |          |          |              |            |             | HSS10X2X5/16        |                 |
|         |            |          |          |              |            |             | HSS10X2X1/4         |                 |
|         |            |          |          |              |            |             | HSS10X2X3/16        |                 |
|         |            |          |          |              |            |             | HSS10X2X1/8         |                 |
|         |            |          |          |              |            |             | HSS9X9X5/8          |                 |
|         |            |          |          |              |            |             | HSS9X9X1/2          |                 |
|         |            |          |          |              |            |             | HSS9X9X3/8          |                 |
|         |            |          |          |              |            |             | HSS9X9X5/16         |                 |
|         |            |          |          |              |            |             | HSS9X9X1/4          |                 |
|         |            |          |          |              |            |             | HSS9X9X3/16         |                 |
|         |            |          |          |              |            |             | HSS9X9X1/8          |                 |
|         |            |          |          |              |            |             | HSS9X7X5/8          |                 |
|         |            |          |          |              |            |             | HSS9X7X1/2          |                 |
|         |            |          |          |              |            |             | HSS9X7X3/8          |                 |
|         |            |          |          |              |            |             | HSS9X7X5/16         |                 |
|         |            |          |          |              |            |             | HSS9X7X1/4          |                 |
|         |            |          |          |              |            |             | HSS9X7X3/16         |                 |
|         |            |          |          |              |            |             | HSS9X5X5/8          |                 |
|         |            |          |          |              |            |             | HSS9X5X1/2          |                 |
|         |            |          |          |              |            |             | HSS9X5X3/8          |                 |
|         |            |          |          |              |            |             | HSS9X5X5/16         |                 |
|         |            |          |          |              |            |             | HSS9X5X1/4          |                 |
|         |            |          |          |              |            |             | HSS9X5X3/16         |                 |
|         |            |          |          |              |            |             | HSS9X3X1/2          |                 |
|         |            |          |          |              |            |             | HSS9X3X3/8          |                 |
|         |            |          |          |              |            |             | HSS9X3X5/16         |                 |
|         |            |          |          |              |            |             | HSS9X3X1/4          |                 |
|         |            |          |          |              |            |             | HSS9X3X3/16         |                 |
|         |            |          |          |              |            |             | HSS8X8X5/8          |                 |
|         |            |          |          |              |            |             | HSS8X8X1/2          |                 |
|         |            |          |          |              |            |             | HSS8X8X3/8          |                 |
|         |            |          |          |              |            |             | HSS8X8X5/16         |                 |
|         |            |          |          |              |            |             | HSS8X8X1/4          |                 |
|         |            |          |          |              |            |             | HSS8X8X3/16         |                 |
|         |            |          |          |              |            |             | HSS8X8X1/8          |                 |
|         |            |          |          |              |            |             | HSS8X6X5/8          |                 |
|         |            |          |          |              |            |             | HSS8X6X1/2          |                 |
|         |            |          |          |              |            |             | HSS8X6X3/8          |                 |
|         |            |          |          |              |            |             | HSS8X6X5/16         |                 |
|         |            |          |          |              |            |             | HSS8X6X1/4          |                 |
|         |            |          |          |              |            |             | HSS8X6X3/16         |                 |
|         |            |          |          |              |            |             | HSS8X4X5/8          |                 |
|         |            |          |          |              |            |             | HSS8X4X1/2          |                 |
|         |            |          |          |              |            |             | HSS8X4X3/8          |                 |
|         |            |          |          |              |            |             | HSS8X4X5/16         |                 |
|         |            |          |          |              |            |             | HSS8X4X1/4          |                 |
|         |            |          |          |              |            |             | HSS8X4X3/16         |                 |
|         |            |          |          |              |            |             | HSS8X4X1/8          |                 |
|         |            |          |          |              |            |             | HSS8X3X1/2          |                 |
|         |            |          |          |              |            |             | HSS8X3X3/8          |                 |
|         |            |          |          |              |            |             | HSS8X3X5/16         |                 |
|         |            |          |          |              |            |             | HSS8X3X1/4          |                 |
|         |            |          |          |              |            |             | HSS8X3X3/16         |                 |
|         |            |          |          |              |            |             | HSS8X3X1/8          |                 |
|         |            |          |          |              |            |             | HSS8X2X1/2          |                 |
|         |            |          |          |              |            |             | HSS8X2X3/8          |                 |
|         |            |          |          |              |            |             | HSS8X2X5/16         |                 |
|         |            |          |          |              |            |             | HSS8X2X1/4          |                 |
|         |            |          |          |              |            |             | HSS8X2X3/16         |                 |
|         |            |          |          |              |            |             | HSS8X2X1/8          |                 |
|         |            |          |          |              |            |             | HSS7X7X5/8          |                 |
|         |            |          |          |              |            |             | HSS7X7X1/2          |                 |
|         |            |          |          |              |            |             | HSS7X7X3/8          |                 |
|         |            |          |          |              |            |             | HSS7X7X5/16         |                 |
|         |            |          |          |              |            |             | HSS7X7X1/4          |                 |
|         |            |          |          |              |            |             | HSS7X7X3/16         |                 |
|         |            |          |          |              |            |             | HSS7X7X1/8          |                 |
|         |            |          |          |              |            |             | HSS7X5X1/2          |                 |
|         |            |          |          |              |            |             | HSS7X5X3/8          |                 |
|         |            |          |          |              |            |             | HSS7X5X5/16         |                 |
|         |            |          |          |              |            |             | HSS7X5X1/4          |                 |
|         |            |          |          |              |            |             | HSS7X5X3/16         |                 |
|         |            |          |          |              |            |             | HSS7X5X1/8          |                 |
|         |            |          |          |              |            |             | HSS7X4X1/2          |                 |
|         |            |          |          |              |            |             | HSS7X4X3/8          |                 |
|         |            |          |          |              |            |             | HSS7X4X5/16         |                 |
|         |            |          |          |              |            |             | HSS7X4X1/4          |                 |
|         |            |          |          |              |            |             | HSS7X4X3/16         |                 |
|         |            |          |          |              |            |             | HSS7X4X1/8          |                 |
|         |            |          |          |              |            |             | HSS7X3X1/2          |                 |
|         |            |          |          |              |            |             | HSS7X3X3/8          |                 |
|         |            |          |          |              |            |             | HSS7X3X5/16         |                 |
|         |            |          |          |              |            |             | HSS7X3X1/4          |                 |
|         |            |          |          |              |            |             | HSS7X3X3/16         |                 |
|         |            |          |          |              |            |             | HSS7X3X1/8          |                 |
|         |            |          |          |              |            |             | HSS7X2X1/4          |                 |
|         |            |          |          |              |            |             | HSS7X2X3/16         |                 |
|         |            |          |          |              |            |             | HSS7X2X1/8          |                 |
|         |            |          |          |              |            |             | HSS6X6X5/8          |                 |
|         |            |          |          |              |            |             | HSS6X6X1/2          |                 |
|         |            |          |          |              |            |             | HSS6X6X3/8          |                 |
|         |            |          |          |              |            |             | HSS6X6X5/16         |                 |
|         |            |          |          |              |            |             | HSS6X6X1/4          |                 |
|         |            |          |          |              |            |             | HSS6X6X3/16         |                 |
|         |            |          |          |              |            |             | HSS6X6X1/8          |                 |
|         |            |          |          |              |            |             | HSS6X5X1/2          |                 |
|         |            |          |          |              |            |             | HSS6X5X3/8          |                 |
|         |            |          |          |              |            |             | HSS6X5X5/16         |                 |
|         |            |          |          |              |            |             | HSS6X5X1/4          |                 |
|         |            |          |          |              |            |             | HSS6X5X3/16         |                 |
|         |            |          |          |              |            |             | HSS6X5X1/8          |                 |
|         |            |          |          |              |            |             | HSS6X4X1/2          |                 |
|         |            |          |          |              |            |             | HSS6X4X3/8          |                 |
|         |            |          |          |              |            |             | HSS6X4X5/16         |                 |
|         |            |          |          |              |            |             | HSS6X4X1/4          |                 |
|         |            |          |          |              |            |             | HSS6X4X3/16         |                 |
|         |            |          |          |              |            |             | HSS6X4X1/8          |                 |
|         |            |          |          |              |            |             | HSS6X3X1/2          |                 |
|         |            |          |          |              |            |             | HSS6X3X3/8          |                 |
|         |            |          |          |              |            |             | HSS6X3X5/16         |                 |
|         |            |          |          |              |            |             | HSS6X3X1/4          |                 |
|         |            |          |          |              |            |             | HSS6X3X3/16         |                 |
|         |            |          |          |              |            |             | HSS6X3X1/8          |                 |
|         |            |          |          |              |            |             | HSS6X2X3/8          |                 |
|         |            |          |          |              |            |             | HSS6X2X5/16         |                 |
|         |            |          |          |              |            |             | HSS6X2X1/4          |                 |
|         |            |          |          |              |            |             | HSS6X2X3/16         |                 |
|         |            |          |          |              |            |             | HSS6X2X1/8          |                 |
|         |            |          |          |              |            |             | HSS5-1/2X5-1/2X3/8  |                 |
|         |            |          |          |              |            |             | HSS5-1/2X5-1/2X5/16 |                 |
|         |            |          |          |              |            |             | HSS5-1/2X5-1/2X1/4  |                 |
|         |            |          |          |              |            |             | HSS5-1/2X5-1/2X3/16 |                 |
|         |            |          |          |              |            |             | HSS5-1/2X5-1/2X1/8  |                 |
|         |            |          |          |              |            |             | HSS5X5X1/2          |                 |
|         |            |          |          |              |            |             | HSS5X5X3/8          |                 |
|         |            |          |          |              |            |             | HSS5X5X5/16         |                 |
|         |            |          |          |              |            |             | HSS5X5X1/4          |                 |
|         |            |          |          |              |            |             | HSS5X5X3/16         |                 |
|         |            |          |          |              |            |             | HSS5X5X1/8          |                 |
|         |            |          |          |              |            |             | HSS5X4X1/2          |                 |
|         |            |          |          |              |            |             | HSS5X4X3/8          |                 |
|         |            |          |          |              |            |             | HSS5X4X5/16         |                 |
|         |            |          |          |              |            |             | HSS5X4X1/4          |                 |
|         |            |          |          |              |            |             | HSS5X4X3/16         |                 |
|         |            |          |          |              |            |             | HSS5X4X1/8          |                 |
|         |            |          |          |              |            |             | HSS5X3X1/2          |                 |
|         |            |          |          |              |            |             | HSS5X3X3/8          |                 |
|         |            |          |          |              |            |             | HSS5X3X5/16         |                 |
|         |            |          |          |              |            |             | HSS5X3X1/4          |                 |
|         |            |          |          |              |            |             | HSS5X3X3/16         |                 |
|         |            |          |          |              |            |             | HSS5X3X1/8          |                 |
|         |            |          |          |              |            |             | HSS5X2-1/2X1/4      |                 |
|         |            |          |          |              |            |             | HSS5X2-1/2X3/16     |                 |
|         |            |          |          |              |            |             | HSS5X2-1/2X1/8      |                 |
|         |            |          |          |              |            |             | HSS5X2X3/8          |                 |
|         |            |          |          |              |            |             | HSS5X2X5/16         |                 |
|         |            |          |          |              |            |             | HSS5X2X1/4          |                 |
|         |            |          |          |              |            |             | HSS5X2X3/16         |                 |
|         |            |          |          |              |            |             | HSS5X2X1/8          |                 |
|         |            |          |          |              |            |             | HSS4-1/2X4-1/2X1/2  |                 |
|         |            |          |          |              |            |             | HSS4-1/2X4-1/2X3/8  |                 |
|         |            |          |          |              |            |             | HSS4-1/2X4-1/2X5/16 |                 |
|         |            |          |          |              |            |             | HSS4-1/2X4-1/2X1/4  |                 |
|         |            |          |          |              |            |             | HSS4-1/2X4-1/2X3/16 |                 |
|         |            |          |          |              |            |             | HSS4-1/2X4-1/2X1/8  |                 |
|         |            |          |          |              |            |             | HSS4X4X1/2          |                 |
|         |            |          |          |              |            |             | HSS4X4X3/8          |                 |
|         |            |          |          |              |            |             | HSS4X4X5/16         |                 |
|         |            |          |          |              |            |             | HSS4X4X1/4          |                 |
|         |            |          |          |              |            |             | HSS4X4X3/16         |                 |
|         |            |          |          |              |            |             | HSS4X4X1/8          |                 |
|         |            |          |          |              |            |             | HSS4X3X3/8          |                 |
|         |            |          |          |              |            |             | HSS4X3X5/16         |                 |
|         |            |          |          |              |            |             | HSS4X3X1/4          |                 |
|         |            |          |          |              |            |             | HSS4X3X3/16         |                 |
|         |            |          |          |              |            |             | HSS4X3X1/8          |                 |
|         |            |          |          |              |            |             | HSS4X2-1/2X1/4      |                 |
|         |            |          |          |              |            |             | HSS4X2-1/2X3/16     |                 |
|         |            |          |          |              |            |             | HSS4X2-1/2X1/8      |                 |
|         |            |          |          |              |            |             | HSS4X2X3/8          |                 |
|         |            |          |          |              |            |             | HSS4X2X5/16         |                 |
|         |            |          |          |              |            |             | HSS4X2X1/4          |                 |
|         |            |          |          |              |            |             | HSS4X2X3/16         |                 |
|         |            |          |          |              |            |             | HSS4X2X1/8          |                 |
|         |            |          |          |              |            |             | HSS4X1-1/2X1/4      |                 |
|         |            |          |          |              |            |             | HSS4X1-1/2X3/16     |                 |
|         |            |          |          |              |            |             | HSS4X1-1/2X1/8      |                 |
|         |            |          |          |              |            |             | HSS3-1/2X3-1/2X3/8  |                 |
|         |            |          |          |              |            |             | HSS3-1/2X3-1/2X5/16 |                 |
|         |            |          |          |              |            |             | HSS3-1/2X3-1/2X1/4  |                 |
|         |            |          |          |              |            |             | HSS3-1/2X3-1/2X3/16 |                 |
|         |            |          |          |              |            |             | HSS3-1/2X3-1/2X1/8  |                 |
|         |            |          |          |              |            |             | HSS3-1/2X2-1/2X3/8  |                 |
|         |            |          |          |              |            |             | HSS3-1/2X2-1/2X5/16 |                 |
|         |            |          |          |              |            |             | HSS3-1/2X2-1/2X1/4  |                 |
|         |            |          |          |              |            |             | HSS3-1/2X2-1/2X3/16 |                 |
|         |            |          |          |              |            |             | HSS3-1/2X2-1/2X1/8  |                 |
|         |            |          |          |              |            |             | HSS3-1/2X2X1/4      |                 |
|         |            |          |          |              |            |             | HSS3-1/2X2X3/16     |                 |
|         |            |          |          |              |            |             | HSS3-1/2X2X1/8      |                 |
|         |            |          |          |              |            |             | HSS3-1/2X1-1/2X1/4  |                 |
|         |            |          |          |              |            |             | HSS3-1/2X1-1/2X3/16 |                 |
|         |            |          |          |              |            |             | HSS3-1/2X1-1/2X1/8  |                 |
|         |            |          |          |              |            |             | HSS3X3X3/8          |                 |
|         |            |          |          |              |            |             | HSS3X3X5/16         |                 |
|         |            |          |          |              |            |             | HSS3X3X1/4          |                 |
|         |            |          |          |              |            |             | HSS3X3X3/16         |                 |
|         |            |          |          |              |            |             | HSS3X3X1/8          |                 |
|         |            |          |          |              |            |             | HSS3X2-1/2X5/16     |                 |
|         |            |          |          |              |            |             | HSS3X2-1/2X1/4      |                 |
|         |            |          |          |              |            |             | HSS3X2-1/2X3/16     |                 |
|         |            |          |          |              |            |             | HSS3X2-1/2X1/8      |                 |
|         |            |          |          |              |            |             | HSS3X2X5/16         |                 |
|         |            |          |          |              |            |             | HSS3X2X1/4          |                 |
|         |            |          |          |              |            |             | HSS3X2X3/16         |                 |
|         |            |          |          |              |            |             | HSS3X2X1/8          |                 |
|         |            |          |          |              |            |             | HSS3X1-1/2X1/4      |                 |
|         |            |          |          |              |            |             | HSS3X1-1/2X3/16     |                 |
|         |            |          |          |              |            |             | HSS3X1-1/2X1/8      |                 |
|         |            |          |          |              |            |             | HSS3X1X3/16         |                 |
|         |            |          |          |              |            |             | HSS3X1X1/8          |                 |
|         |            |          |          |              |            |             | HSS2-1/2X2-1/2X5/16 |                 |
|         |            |          |          |              |            |             | HSS2-1/2X2-1/2X1/4  |                 |
|         |            |          |          |              |            |             | HSS2-1/2X2-1/2X3/16 |                 |
|         |            |          |          |              |            |             | HSS2-1/2X2-1/2X1/8  |                 |
|         |            |          |          |              |            |             | HSS2-1/2X2X1/4      |                 |
|         |            |          |          |              |            |             | HSS2-1/2X2X3/16     |                 |
|         |            |          |          |              |            |             | HSS2-1/2X2X1/8      |                 |
|         |            |          |          |              |            |             | HSS2-1/2X1-1/2X1/4  |                 |
|         |            |          |          |              |            |             | HSS2-1/2X1-1/2X3/16 |                 |
|         |            |          |          |              |            |             | HSS2-1/2X1-1/2X1/8  |                 |
|         |            |          |          |              |            |             | HSS2-1/2X1X3/16     |                 |
|         |            |          |          |              |            |             | HSS2-1/2X1X1/8      |                 |
|         |            |          |          |              |            |             | HSS2-1/4X2-1/4X1/4  |                 |
|         |            |          |          |              |            |             | HSS2-1/4X2-1/4X3/16 |                 |
|         |            |          |          |              |            |             | HSS2-1/4X2-1/4X1/8  |                 |
|         |            |          |          |              |            |             | HSS2X2X1/4          |                 |
|         |            |          |          |              |            |             | HSS2X2X3/16         |                 |
|         |            |          |          |              |            |             | HSS2X2X1/8          |                 |
|         |            |          |          |              |            |             | HSS2X1-1/2X3/16     |                 |
|         |            |          |          |              |            |             | HSS2X1-1/2X1/8      |                 |
|         |            |          |          |              |            |             | HSS2X1X3/16         |                 |
|         |            |          |          |              |            |             | HSS2X1X1/8          |                 |
|         |            |          |          |              |            |             | HSS1-1/2X1-1/2X1/4  |                 |
|         |            |          |          |              |            |             | HSS1-1/2X1-1/2X3/16 |                 |
|         |            |          |          |              |            |             | HSS1-1/2X1-1/2X1/8  |                 |
