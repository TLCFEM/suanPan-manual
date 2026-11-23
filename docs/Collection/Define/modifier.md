# modifier

`modifier` objects modify element response that is not considered in the element itself.
Typical examples include the element damping matrix and the lumped mass matrix.

If several modifiers are defined, they are applied to the system sequentially in tag order.
They are not executed in parallel because different orders may lead to different results.

Users should pay extra attention to the order in which modifiers are defined.

Please refer to [`Modifier`](../../Library/Element/Modifier/Modifier.md) for the available modifiers.
