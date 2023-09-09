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

## Supported Designations

| WT           | WT        | W       | W       | MT & ST     | M & S      | HP       |
|:-------------|:----------|:--------|:--------|:------------|:-----------|:---------|
| WT22X167.5   | WT9X155.5 | W44X335 | W18X311 | MT6.25X6.2  | M12.5X12.4 | HP18X204 |
| WT22X145     | WT9X141.5 | W44X290 | W18X283 | MT6.25X5.8  | M12.5X11.6 | HP18X181 |
| WT22X131     | WT9X129   | W44X262 | W18X258 | MT6X5.9     | M12X11.8   | HP18X157 |
| WT22X115     | WT9X117   | W44X230 | W18X234 | MT6X5.4     | M12X10.8   | HP18X135 |
| WT20X327.5   | WT9X105.5 | W40X655 | W18X211 | MT6X5       | M12X10     | HP16X183 |
| WT20X296.5   | WT9X96    | W40X593 | W18X192 | MT5X4.5     | M10X9      | HP16X162 |
| WT20X251.5   | WT9X87.5  | W40X503 | W18X175 | MT5X4       | M10X8      | HP16X141 |
| WT20X215.5   | WT9X79    | W40X431 | W18X158 | MT5X3.75    | M10X7.5    | HP16X121 |
| WT20X198.5   | WT9X71.5  | W40X397 | W18X143 | MT4X3.25    | M8X6.5     | HP16X101 |
| WT20X186     | WT9X65    | W40X372 | W18X130 | MT4X3.1     | M8X6.2     | HP16X88  |
| WT20X181     | WT9X59.5  | W40X362 | W18X119 | MT3X2.2     | M6X4.4     | HP14X117 |
| WT20X162     | WT9X53    | W40X324 | W18X106 | MT3X1.85    | M6X3.7     | HP14X102 |
| WT20X148.5   | WT9X48.5  | W40X297 | W18X97  | MT2.5X9.45  | M5X18.9    | HP14X89  |
| WT20X138.5   | WT9X43    | W40X277 | W18X86  | MT2X3       | M4X6       | HP14X73  |
| WT20X124.5   | WT9X38    | W40X249 | W18X76  | ST12X60.5   | M4X4.08    | HP12X89  |
| WT20X107.5   | WT9X35.5  | W40X215 | W18X71  | ST12X53     | M4X3.45    | HP12X84  |
| WT20X99.5    | WT9X32.5  | W40X199 | W18X65  | ST12X50     | M4X3.2     | HP12X74  |
| WT20X196     | WT9X30    | W40X392 | W18X60  | ST12X45     | M3X2.9     | HP12X63  |
| WT20X165.5   | WT9X27.5  | W40X331 | W18X55  | ST12X40     | S24X121    | HP12X53  |
| WT20X163.5   | WT9X25    | W40X327 | W18X50  | ST10X48     | S24X106    | HP10X57  |
| WT20X147     | WT9X23    | W40X294 | W18X46  | ST10X43     | S24X100    | HP10X42  |
| WT20X139     | WT9X20    | W40X278 | W18X40  | ST10X37.5   | S24X90     | HP8X36   |
| WT20X132     | WT9X17.5  | W40X264 | W18X35  | ST10X33     | S24X80     |          |
| WT20X117.5   | WT8X50    | W40X235 | W16X100 | ST9X35      | S20X96     |          |
| WT20X105.5   | WT8X44.5  | W40X211 | W16X89  | ST9X27.35   | S20X86     |          |
| WT20X91.5    | WT8X38.5  | W40X183 | W16X77  | ST7.5X25    | S20X75     |          |
| WT20X83.5    | WT8X33.5  | W40X167 | W16X67  | ST7.5X21.45 | S20X66     |          |
| WT20X74.5    | WT8X28.5  | W40X149 | W16X57  | ST6X25      | S18X70     |          |
| WT18X462.5   | WT8X25    | W36X925 | W16X50  | ST6X20.4    | S18X54.7   |          |
| WT18X426.5   | WT8X22.5  | W36X853 | W16X45  | ST6X17.5    | S15X50     |          |
| WT18X401     | WT8X20    | W36X802 | W16X40  | ST6X15.9    | S15X42.9   |          |
| WT18X361.5   | WT8X18    | W36X723 | W16X36  | ST5X17.5    | S12X50     |          |
| WT18X326     | WT8X15.5  | W36X652 | W16X31  | ST5X12.7    | S12X40.8   |          |
| WT18X264.5   | WT8X13    | W36X529 | W16X26  | ST4X11.5    | S12X35     |          |
| WT18X243.5   | WT7X436.5 | W36X487 | W14X873 | ST4X9.2     | S12X31.8   |          |
| WT18X220.5   | WT7X404   | W36X441 | W14X808 | ST3X8.6     | S10X35     |          |
| WT18X197.5   | WT7X365   | W36X395 | W14X730 | ST3X6.25    | S10X25.4   |          |
| WT18X180.5   | WT7X332.5 | W36X361 | W14X665 | ST2.5X5     | S8X23      |          |
| WT18X165     | WT7X302.5 | W36X330 | W14X605 | ST2X4.75    | S8X18.4    |          |
| WT18X151     | WT7X275   | W36X302 | W14X550 | ST2X3.85    | S6X17.25   |          |
| WT18X141     | WT7X250   | W36X282 | W14X500 | ST1.5X3.75  | S6X12.5    |          |
| WT18X131     | WT7X227.5 | W36X262 | W14X455 | ST1.5X2.85  | S5X10      |          |
| WT18X123.5   | WT7X213   | W36X247 | W14X426 |             | S4X9.5     |          |
| WT18X115.5   | WT7X199   | W36X231 | W14X398 |             | S4X7.7     |          |
| WT18X128     | WT7X185   | W36X256 | W14X370 |             | S3X7.5     |          |
| WT18X116     | WT7X171   | W36X232 | W14X342 |             | S3X5.7     |          |
| WT18X105     | WT7X155.5 | W36X210 | W14X311 |             |            |          |
| WT18X97      | WT7X141.5 | W36X194 | W14X283 |             |            |          |
| WT18X91      | WT7X128.5 | W36X182 | W14X257 |             |            |          |
| WT18X85      | WT7X116.5 | W36X170 | W14X233 |             |            |          |
| WT18X80      | WT7X105.5 | W36X160 | W14X211 |             |            |          |
| WT18X75      | WT7X96.5  | W36X150 | W14X193 |             |            |          |
| WT18X67.5    | WT7X88    | W36X135 | W14X176 |             |            |          |
| WT16.5X193.5 | WT7X79.5  | W33X387 | W14X159 |             |            |          |
| WT16.5X177   | WT7X72.5  | W33X354 | W14X145 |             |            |          |
| WT16.5X159   | WT7X66    | W33X318 | W14X132 |             |            |          |
| WT16.5X145.5 | WT7X60    | W33X291 | W14X120 |             |            |          |
| WT16.5X131.5 | WT7X54.5  | W33X263 | W14X109 |             |            |          |
| WT16.5X120.5 | WT7X49.5  | W33X241 | W14X99  |             |            |          |
| WT16.5X110.5 | WT7X45    | W33X221 | W14X90  |             |            |          |
| WT16.5X100.5 | WT7X41    | W33X201 | W14X82  |             |            |          |
| WT16.5X84.5  | WT7X37    | W33X169 | W14X74  |             |            |          |
| WT16.5X76    | WT7X34    | W33X152 | W14X68  |             |            |          |
| WT16.5X70.5  | WT7X30.5  | W33X141 | W14X61  |             |            |          |
| WT16.5X65    | WT7X26.5  | W33X130 | W14X53  |             |            |          |
| WT16.5X59    | WT7X24    | W33X118 | W14X48  |             |            |          |
| WT15X195.5   | WT7X21.5  | W30X391 | W14X43  |             |            |          |
| WT15X178.5   | WT7X19    | W30X357 | W14X38  |             |            |          |
| WT15X163     | WT7X17    | W30X326 | W14X34  |             |            |          |
| WT15X146     | WT7X15    | W30X292 | W14X30  |             |            |          |
| WT15X130.5   | WT7X13    | W30X261 | W14X26  |             |            |          |
| WT15X117.5   | WT7X11    | W30X235 | W14X22  |             |            |          |
| WT15X105.5   | WT6X168   | W30X211 | W12X336 |             |            |          |
| WT15X95.5    | WT6X152.5 | W30X191 | W12X305 |             |            |          |
| WT15X86.5    | WT6X139.5 | W30X173 | W12X279 |             |            |          |
| WT15X74      | WT6X126   | W30X148 | W12X252 |             |            |          |
| WT15X66      | WT6X115   | W30X132 | W12X230 |             |            |          |
| WT15X62      | WT6X105   | W30X124 | W12X210 |             |            |          |
| WT15X58      | WT6X95    | W30X116 | W12X190 |             |            |          |
| WT15X54      | WT6X85    | W30X108 | W12X170 |             |            |          |
| WT15X49.5    | WT6X76    | W30X99  | W12X152 |             |            |          |
| WT15X45      | WT6X68    | W30X90  | W12X136 |             |            |          |
| WT13.5X269.5 | WT6X60    | W27X539 | W12X120 |             |            |          |
| WT13.5X184   | WT6X53    | W27X368 | W12X106 |             |            |          |
| WT13.5X168   | WT6X48    | W27X336 | W12X96  |             |            |          |
| WT13.5X153.5 | WT6X43.5  | W27X307 | W12X87  |             |            |          |
| WT13.5X140.5 | WT6X39.5  | W27X281 | W12X79  |             |            |          |
| WT13.5X129   | WT6X36    | W27X258 | W12X72  |             |            |          |
| WT13.5X117.5 | WT6X32.5  | W27X235 | W12X65  |             |            |          |
| WT13.5X108.5 | WT6X29    | W27X217 | W12X58  |             |            |          |
| WT13.5X97    | WT6X26.5  | W27X194 | W12X53  |             |            |          |
| WT13.5X89    | WT6X25    | W27X178 | W12X50  |             |            |          |
| WT13.5X80.5  | WT6X22.5  | W27X161 | W12X45  |             |            |          |
| WT13.5X73    | WT6X20    | W27X146 | W12X40  |             |            |          |
| WT13.5X64.5  | WT6X17.5  | W27X129 | W12X35  |             |            |          |
| WT13.5X57    | WT6X15    | W27X114 | W12X30  |             |            |          |
| WT13.5X51    | WT6X13    | W27X102 | W12X26  |             |            |          |
| WT13.5X47    | WT6X11    | W27X94  | W12X22  |             |            |          |
| WT13.5X42    | WT6X9.5   | W27X84  | W12X19  |             |            |          |
| WT12X185     | WT6X8     | W24X370 | W12X16  |             |            |          |
| WT12X167.5   | WT6X7     | W24X335 | W12X14  |             |            |          |
| WT12X153     | WT5X56    | W24X306 | W10X112 |             |            |          |
| WT12X139.5   | WT5X50    | W24X279 | W10X100 |             |            |          |
| WT12X125     | WT5X44    | W24X250 | W10X88  |             |            |          |
| WT12X114.5   | WT5X38.5  | W24X229 | W10X77  |             |            |          |
| WT12X103.5   | WT5X34    | W24X207 | W10X68  |             |            |          |
| WT12X96      | WT5X30    | W24X192 | W10X60  |             |            |          |
| WT12X88      | WT5X27    | W24X176 | W10X54  |             |            |          |
| WT12X81      | WT5X24.5  | W24X162 | W10X49  |             |            |          |
| WT12X73      | WT5X22.5  | W24X146 | W10X45  |             |            |          |
| WT12X65.5    | WT5X19.5  | W24X131 | W10X39  |             |            |          |
| WT12X58.5    | WT5X16.5  | W24X117 | W10X33  |             |            |          |
| WT12X52      | WT5X15    | W24X104 | W10X30  |             |            |          |
| WT12X51.5    | WT5X13    | W24X103 | W10X26  |             |            |          |
| WT12X47      | WT5X11    | W24X94  | W10X22  |             |            |          |
| WT12X42      | WT5X9.5   | W24X84  | W10X19  |             |            |          |
| WT12X38      | WT5X8.5   | W24X76  | W10X17  |             |            |          |
| WT12X34      | WT5X7.5   | W24X68  | W10X15  |             |            |          |
| WT12X31      | WT5X6     | W24X62  | W10X12  |             |            |          |
| WT12X27.5    | WT4X33.5  | W24X55  | W8X67   |             |            |          |
| WT10.5X137.5 | WT4X29    | W21X275 | W8X58   |             |            |          |
| WT10.5X124   | WT4X24    | W21X248 | W8X48   |             |            |          |
| WT10.5X111.5 | WT4X20    | W21X223 | W8X40   |             |            |          |
| WT10.5X100.5 | WT4X17.5  | W21X201 | W8X35   |             |            |          |
| WT10.5X91    | WT4X15.5  | W21X182 | W8X31   |             |            |          |
| WT10.5X83    | WT4X14    | W21X166 | W8X28   |             |            |          |
| WT10.5X73.5  | WT4X12    | W21X147 | W8X24   |             |            |          |
| WT10.5X66    | WT4X10.5  | W21X132 | W8X21   |             |            |          |
| WT10.5X61    | WT4X9     | W21X122 | W8X18   |             |            |          |
| WT10.5X55.5  | WT4X7.5   | W21X111 | W8X15   |             |            |          |
| WT10.5X50.5  | WT4X6.5   | W21X101 | W8X13   |             |            |          |
| WT10.5X46.5  | WT4X5     | W21X93  | W8X10   |             |            |          |
| WT10.5X41.5  | WT3X12.5  | W21X83  | W6X25   |             |            |          |
| WT10.5X36.5  | WT3X10    | W21X73  | W6X20   |             |            |          |
| WT10.5X34    | WT3X7.5   | W21X68  | W6X15   |             |            |          |
| WT10.5X31    | WT3X8     | W21X62  | W6X16   |             |            |          |
| WT10.5X27.5  | WT3X6     | W21X55  | W6X12   |             |            |          |
| WT10.5X24    | WT3X4.5   | W21X48  | W6X9    |             |            |          |
| WT10.5X28.5  | WT3X4.25  | W21X57  | W6X8.5  |             |            |          |
| WT10.5X25    | WT2.5X9.5 | W21X50  | W5X19   |             |            |          |
| WT10.5X22    | WT2.5X8   | W21X44  | W5X16   |             |            |          |
|              | WT2X6.5   |         | W4X13   |             |            |          |
