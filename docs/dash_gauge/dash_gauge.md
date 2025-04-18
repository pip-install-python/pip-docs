---
name: Gauge
description: A collection of gauge, knob, thermostat, joystick, and display components for Dash.
endpoint: /pip/dash_gauge
package: dash_gauge
icon: mdi:gauge 
---

.. toc::

[Visit GitHub Repo](https://github.com/pip-install-python/dash-gauge)

### Installation

```bash
pip install dash-gauge
```


### Introduction

The `dash-gauge` package provides a suite of interactive and visually appealing components to enhance your Plotly Dash dashboards. Built as wrappers around popular React libraries, this collection includes:

*   **`DashGauge`**: Customizable gauge charts (Grafana, Semicircle, Radial styles).
*   **`DashRotaryKnob`**: Interactive rotary knob controls with various skins.
*   **`DashThermostat`**: A thermostat-like input component.
*   **`DashRCJoystick`**: A virtual joystick component for directional input.
*   **`Dash7SegmentDisplay`**: A classic 7-segment display for numbers and hex values.

This page documents each component included in the suite.

.. exec::docs.dash_gauge.introduction_example
    :code: false

.. sourcetabs::docs/dash_gauge/introduction_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### DashGauge

Displays a value on a customizable gauge. Supports different styles, color ranges, sub-arcs, custom labels, and pointers. Ideal for visualizing KPIs, sensor readings, or progress metrics.

.. exec::docs.dash_gauge.gauge_example
    :code: false

.. sourcetabs::docs/dash_gauge/gauge_example.py
    :defaultExpanded: false
    :withExpandedButton: true


#### DashGauge Props

| Prop              | Type                       | Default      | Description                                                                                                                                  |
|-------------------|----------------------------|--------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `id`              | string                     | -            | Component ID for Dash callbacks.                                                                                                             |
| `value`           | number                     | `33`         | The value the gauge should indicate.                                                                                                         |
| `type`            | string                     | `'grafana'`  | Style of the gauge. Choices: `'grafana'`, `'semicircle'`, `'radial'`.                                                                         |
| `minValue`        | number                     | `0`          | Minimum value of the gauge scale.                                                                                                            |
| `maxValue`        | number                     | `100`        | Maximum value of the gauge scale.                                                                                                            |
| `className`       | string                     | `dash-gauge` | CSS class name for the component.                                                                                                            |
| `style`           | object                     | `{}`         | Inline CSS styles for the component.                                                                                                         |
| `marginInPercent` | number or object           | `undefined`  | Sets the margin for the chart inside the SVG. Can be a single number or `{top, bottom, left, right}`.                                         |
| `arc`             | object                     | `{}`         | Configuration for the gauge arc (e.g., `width`, `padding`, `cornerRadius`, `colorArray`, `subArcs`, `gradient`). See `usage_gauge.py` for details. |
| `pointer`         | object                     | `{}`         | Configuration for the gauge pointer/needle (e.g., `type`, `color`, `length`, `width`, `animate`, `elastic`). See `usage_gauge.py` for details.   |
| `labels`          | object                     | `{}`         | Configuration for value and tick labels (e.g., `valueLabel`, `tickLabels`, `formatTextValue`, `hideMinMax`). See `usage_gauge.py` for details. |
| `setProps`        | func                       | -            | Dash-assigned callback function.                                                                                                             |

**Note:** For detailed examples of `arc`, `pointer`, and `labels` configurations, please refer to the `usage_gauge.py` file in the GitHub repository.

---

### DashRotaryKnob

An interactive knob component, useful for selecting values within a range (e.g., volume, tuning). Comes with multiple visual skins from the `react-rotary-knob-skin-pack`.

.. exec::docs.dash_gauge.knob_example
    :code: false

.. sourcetabs::docs/dash_gauge/knob_example.py
    :defaultExpanded: false
    :withExpandedButton: true

#### DashRotaryKnob Props

| Prop            | Type    | Default   | Description                                                                                                |
|-----------------|---------|-----------|------------------------------------------------------------------------------------------------------------|
| `id`            | string  | -         | Component ID for Dash callbacks.                                                                           |
| `value`         | number  | `0`       | The current value of the knob. Updated via interaction or callbacks.                                     |
| `min`           | number  | `0`       | Minimum value of the knob.                                                                                 |
| `max`           | number  | `100`     | Maximum value of the knob.                                                                                 |
| `step`          | number  | `1`       | Increment/decrement step size.                                                                             |
| `skinName`      | string  | `'s1'`    | Selects the visual appearance (e.g., `'s1'`, `'s5'`, `'s10'`, up to `'s18'`). See repository for examples. |
| `preciseMode`   | boolean | `true`    | If true, requires Shift key + drag for fine adjustments.                                                     |
| `unlockDistance`| number  | `0`       | Degrees the mouse must move vertically to "unlock" the knob for rotation.                                    |
| `className`     | string  | `''`      | CSS class name for the component.                                                                          |
| `style`         | object  | `{}`      | Inline CSS styles for the component.                                                                       |
| `setProps`      | func    | -         | Dash-assigned callback function.                                                                           |

**Note:** Explore all 18 skins by changing the `skinName` prop! See `usage_rotary_knob.py` for an interactive example. Only skins 1 & 10-15 look good 🤷‍ "no idea why the other skins don't alin correctly".

---

### DashThermostat

A component mimicking a thermostat interface for setting a target value, typically temperature.

.. exec::docs.dash_gauge.thermostat_example
    :code: false

.. sourcetabs::docs/dash_gauge/thermostat_example.py
    :defaultExpanded: false
    :withExpandedButton: true

#### DashThermostat Props

| Prop         | Type    | Default     | Description                                                                                             |
|--------------|---------|-------------|---------------------------------------------------------------------------------------------------------|
| `id`         | string  | -           | Component ID for Dash callbacks.                                                                        |
| `value`      | number  | Required    | The current set value (e.g., temperature). Updated via interaction or callbacks.                          |
| `min`        | number  | `0`         | Minimum value of the thermostat scale.                                                                    |
| `max`        | number  | `100`       | Maximum value of the thermostat scale.                                                                    |
| `valueSuffix`| string  | `'°'`       | Text to display after the value (e.g., `'°C'`, `'°F'`, `'%`).                                             |
| `disabled`   | boolean | `false`     | If true, disables user interaction with the thermostat.                                                   |
| `handle`     | object  | `undefined` | Configuration object for the draggable handle (e.g., `size`, `colors`). See `react-thermostat` docs.      |
| `track`      | object  | `undefined` | Configuration object for the background track (e.g., `colors`, `thickness`, `markers`). See `react-thermostat` docs. |
| `className`  | string  | `''`        | CSS class name for the component.                                                                       |
| `style`      | object  | `{}`        | Inline CSS styles for the component. Note: Component has min-width/height defaults.                     |
| `setProps`   | func    | -           | Dash-assigned callback function.                                                                        |

**Note:** The `usage_thermostat.py` example demonstrates complex interaction with custom styling and mode switching. It may require CSS files placed in an `assets` folder.

---

### DashRCJoystick

A virtual joystick component that reports direction, angle, and distance based on user interaction. Useful for controlling elements in simulations, games, or robotics dashboards.

.. exec::docs.dash_gauge.joystick_example
    :code: false

.. sourcetabs::docs/dash_gauge/joystick_example.py
    :defaultExpanded: false
    :withExpandedButton: true

#### DashRCJoystick Props

| Prop                 | Type    | Default      | Description                                                                                                                                 |
|----------------------|---------|--------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `id`                 | string  | -            | Component ID for Dash callbacks.                                                                                                            |
| `baseRadius`         | number  | `75`         | Radius of the joystick's static base circle.                                                                                                  |
| `controllerRadius`   | number  | `35`         | Radius of the movable controller knob.                                                                                                      |
| `directionCountMode` | string  | `'Five'`     | Determines the reported directions. Choices: `'Five'` (Center, Top, Bottom, Left, Right), `'Nine'` (includes diagonals).                      |
| `insideMode`         | boolean | `false`      | If true, the controller knob stays within the base radius.                                                                                  |
| `throttle`           | number  | `0`          | Throttle time in milliseconds for `onChange` events. `0` means no throttle.                                                                   |
| `className`          | string  | `''`         | CSS class name for the container.                                                                                                           |
| `style`              | object  | `{}`         | Inline CSS styles for the container.                                                                                                        |
| `controllerClassName`| string  | `undefined`  | Additional CSS class for the controller knob.                                                                                               |
| **Read-only Props**  |         |              | *(These props are updated by the component and read in callbacks)*                                                                          |
| `angle`              | number  | `undefined`  | [Readonly] Current angle of the joystick (degrees). `undefined` when centered.                                                              |
| `direction`          | string  | `'Center'`   | [Readonly] Current direction string (e.g., 'Top', 'BottomLeft', 'Center'). Possible values depend on `directionCountMode`.                   |
| `distance`           | number  | `0`          | [Readonly] Current distance of the controller from the center (normalized 0-1 based on `baseRadius`).                                       |
| `setProps`           | func    | -            | Dash-assigned callback function.                                                                                                            |

**Note:** See `usage_rc_joystick.py` for an example controlling the joystick's appearance and reading its state.

---
