# SimpleHysteresis

The `SimpleHysteresis` model is a simplified framework for defining arbitrary backbones with linear unloading/reloading
behaviour. The residual strain can be customised according to the specific rules.

## History Variable Layout

| location             | value                             |
|----------------------|-----------------------------------|
| `initial_history(0)` | maximum compression strain        |
| `initial_history(1)` | maximum tension strain            |
| `initial_history(2)` | last compression unloading strain |
| `initial_history(3)` | last compression unloading stress |
| `initial_history(4)` | last tension unloading strain     |
| `initial_history(5)` | last tension unloading stress     |
| `initial_history(6)` | residual compression strain       |
| `initial_history(7)` | residual tension strain           |
