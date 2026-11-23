# orientation

The `orientation` command defines the local reference frame of a 3D beam element.
The resulting object is referenced by its tag to transform between global and local coordinates.

## Syntax

```text title="orientation"
orientation (1) (2) (3) (4) (5)
# (1) string, orientation type
# (2) int, unique orientation tag
# (3) double, x component of the reference vector
# (4) double, y component of the reference vector
# (5) double, z component of the reference vector
```

## Remarks

1. The available types are `B3DL`, `B3DC`, `B3DOSL`, and `B3DOSC`.
2. `B3DL` and `B3DOSL` use a linear transformation, while `B3DC` and `B3DOSC` use a corotational formulation.
3. Beams such as `B31`/`F31` require `B3DL` or `B3DC`, while the open-section beam `EB31OS` requires `B3DOSL` or `B3DOSC`.
4. See [Orientation](../../Library/Element/Beam/Orientation.md) for the definition of the local axes and worked examples.
