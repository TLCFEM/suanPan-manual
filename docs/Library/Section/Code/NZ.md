# NZ

NZ Code Sections

Sections in accordance with AS/NZ standards are available in both 2D and 3D applications.

**See [Eccentricity](../Eccentricity.md) for more details.**

## Syntax

To define a section, analysts can use the following commands.

```
section NZ2D (1) (2) (3) [4] [5] [6]
# (1) string, designation
# (2) int, unique tag
# (3) int, material model tag
# [4] double, scale, default: 1.0
# [5] int, number of integration points, default: 6
# [6] double, eccentricity, default: 0.0

section NZ3D (1) (2) (3) [4] [5] [6] [7]
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
2. For 2D sections, the number of integration points is set to 2 using Gauss quadrature for flanges in I-sections.
3. For 3D sections, along web/flange thickness, one integration point is used. along flange width and web height, the
   same amount of integration points are used as defined by user.

## Supported Designations

Currently, the following designations are available.

### I-Sections

`AS/NZ 3679.1:2016` and `AS/NZ 3679.2:2016`

| Welded Beams | Welded Columns | Universal Beams | Universal Columns |
|:-------------|:---------------|:----------------|:------------------|
| 1200WB455    | 500WC440       | 610UB125        | 320UC158          |
| 1200WB423    | 500WC414       | 610UB113        | 310UC137          |
| 1200WB392    | 500WC383       | 610UB101        | 310UC118          |
| 1200WB342    | 500WC340       | 530UB92.4       | 310UC96.8         |
| 1200WB317    | 500WC290       | 530UB82.0       | 250UC89.5         |
| 1200WB278    | 500WC267       | 460UB82.1       | 250UC72.9         |
| 1200WB249    | 500WC228       | 460UB74.6       | 200UC59.5         |
| 1000WB322    | 400WC361       | 460UB67.1       | 200UC52.2         |
| 1000WB296    | 400WC328       | 410UB59.7       | 200UC46.2         |
| 1000WB258    | 400WC303       | 410UB53.7       | 150UC37.2         |
| 1000WB215    | 400WC270       | 360UB56.7       | 150UC30.0         |
| 900WB282     | 400WC212       | 360UB50.7       | 150UC23.4         |
| 900WB257     | 400WC181       | 360UB44.7       | 100UC14.8         |
| 900WB218     | 400WC144       | 310UB46.2       |                   |
| 900WB175     | 350WC280       | 310UB40.4       |                   |
| 800WB192     | 350WC258       | 310UB32.0       |                   |
| 800WB168     | 350WC230       | 250UB37.3       |                   |
| 800WB146     | 350WC197       | 250UB31.4       |                   |
| 800WB122     |                | 250UB25.7       |                   |
| 700WB173     |                | 200UB29.8       |                   |
| 700WB150     |                | 200UB25.4       |                   |
| 700WB130     |                | 200UB22.3       |                   |
| 700WB115     |                | 200UB18.2       |                   |
|              |                | 180UB22.2       |                   |
|              |                | 180UB18.1       |                   |
|              |                | 180UB16.1       |                   |
|              |                | 150UB18.0       |                   |
|              |                | 150UB14.0       |                   |

### Rectangular/Square Hollow Sections

Note for hollow sections, due to FE idealization, the moment of inertia is larger than the one(s) shown in the standard.
The difference can be as large as $$10\%$$.

`AS/NZS 1163:2016`

| RHS            | RHS          | SHS        | SHS       |
|:---------------|:-------------|:-----------|:----------|
| 250X150X9.0RHS | 75X50X4.0RHS | 250X9.0SHS | 65X3.0SHS |
| 250X150X6.0RHS | 75X50X3.0RHS | 250X6.0SHS | 65X2.5SHS |
| 250X150X5.0RHS | 75X50X2.5RHS | 200X9.0SHS | 65X2.0SHS |
| 200X100X9.0RHS | 75X50X2.0RHS | 200X6.0SHS | 50X4.0SHS |
| 200X100X6.0RHS | 75X25X2.5RHS | 200X5.0SHS | 50X3.0SHS |
| 200X100X5.0RHS | 75X25X2.0RHS | 150X9.0SHS | 50X2.5SHS |
| 200X100X4.0RHS | 75X25X1.6RHS | 150X6.0SHS | 50X2.0SHS |
| 150X100X6.0RHS | 65X35X3.0RHS | 150X5.0SHS | 50X1.6SHS |
| 150X100X5.0RHS | 65X35X2.5RHS | 125X9.0SHS | 40X4.0SHS |
| 150X100X4.0RHS | 65X35X2.0RHS | 125X6.0SHS | 40X2.5SHS |
| 150X50X5.0RHS  | 50X25X3.0RHS | 125X5.0SHS | 40X2.0SHS |
| 150X50X4.0RHS  | 50X25X2.5RHS | 125X4.0SHS | 40X1.6SHS |
| 150X50X3.0RHS  | 50X25X2.0RHS | 100X9.0SHS | 35X3.0SHS |
| 125X75X5.0RHS  | 50X25X1.6RHS | 100X6.0SHS | 35X2.5SHS |
| 125X75X4.0RHS  | 50X20X3.0RHS | 100X5.0SHS | 35X2.0SHS |
| 125X75X3.0RHS  | 50X20X2.5RHS | 100X4.0SHS | 35X1.6SHS |
| 100X50X6.0RHS  | 50X20X2.0RHS | 100X3.0SHS | 30X2.0SHS |
| 100X50X5.0RHS  | 50X20X1.6RHS | 89X6.0SHS  | 30X1.6SHS |
| 100X50X4.0RHS  |              | 89X5.0SHS  | 25X3.0SHS |
| 100X50X3.5RHS  |              | 89X3.5SHS  | 25X2.5SHS |
| 100X50X3.0RHS  |              | 75X6.0SHS  | 25X2.0SHS |
| 100X50X2.5RHS  |              | 75X5.0SHS  | 25X1.6SHS |
| 100X50X2.0RHS  |              | 75X4.0SHS  | 20X1.6SHS |
|                |              | 75X3.5SHS  |           |
|                |              | 75X3.0SHS  |           |
|                |              | 75X2.5SHS  |           |

### Circular Hollow Sections

`AS/NZS 1163:2016`

| CHS           | CHS           | CHS           | CHS          |
|:--------------|:--------------|:--------------|:-------------|
| 610.0X12.7CHS | 76.1X5.9CHS   | 355.6X12.7CHS | 139.7X3.5CHS |
| 610.0X9.5CHS  | 76.1X4.5CHS   | 355.6X9.5CHS  | 139.7X3.0CHS |
| 610.0X6.4CHS  | 76.1X3.6CHS   | 355.6X6.4CHS  | 114.3X6.0CHS |
| 508.0X12.7CHS | 60.3X5.4CHS   | 323.9X12.7CHS | 114.3X4.8CHS |
| 508.0X9.5CHS  | 60.3X4.5CHS   | 323.9X9.5CHS  | 114.3X3.6CHS |
| 508.0X6.4CHS  | 60.3X3.6CHS   | 323.9X6.4CHS  | 114.3X3.2CHS |
| 165.1X5.4CHS  | 48.3X5.4CHS   | 273.1X9.3CHS  | 101.6X3.2CHS |
| 165.1X5.0CHS  | 48.3X4.0CHS   | 273.1X6.4CHS  | 101.6X2.6CHS |
| 139.7X5.4CHS  | 48.3X3.2CHS   | 273.1X4.8CHS  | 88.9X5.5CHS  |
| 139.7X5.0CHS  | 42.4X4.9CHS   | 219.1X8.2CHS  | 88.9X4.8CHS  |
| 114.3X5.4CHS  | 42.4X4.0CHS   | 219.1X6.4CHS  | 88.9X3.2CHS  |
| 114.3X4.5CHS  | 42.4X3.2CHS   | 219.1X4.8CHS  | 88.9X2.6CHS  |
| 101.6X5.0CHS  | 457.0X12.7CHS | 168.3X7.1CHS  | 76.1X3.2CHS  |
| 101.6X4.0CHS  | 457.0X9.5CHS  | 168.3X6.4CHS  | 76.1X2.3CHS  |
| 88.9X5.9CHS   | 457.0X6.4CHS  | 168.3X4.8CHS  |              |
| 88.9X5.0CHS   | 406.4X12.7CHS | 165.1X3.5CHS  |              |
| 88.9X4.0CHS   | 406.4X9.5CHS  | 165.1X3.0CHS  |              |
|               | 406.4X6.4CHS  |               |              |
