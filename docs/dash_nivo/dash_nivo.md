---
name: Nivo
description: Dash Nivo is a Dash component library for Nivo visualizations.
endpoint: /pip/dash_nivo
package: dash_nivo
icon: la:chart-line
---

.. toc::

### Introduction

This package provides Dash components for Nivo charts. Currently, it includes two components: ResponsiveCircle and AreaBump.

[Visit GitHub Repo](https://github.com/pip-install-python/dash_nivo)

### Installation

```bash
pip install dash-nivo
```

### Example of Both Components
.. exec::docs.dash_nivo.initial_example
    :code: false

.. sourcetabs::docs/dash_nivo/initial_example.py
    :defaultExpanded: false
    :withExpandedButton: true

### Area Bump 
.. exec::docs.dash_nivo.areabump
    :code: false

.. sourcetabs::docs/dash_nivo/areabump.py
    :defaultExpanded: false
    :withExpandedButton: true

#### Properties

| Property       | Type             | Default                                      | Description                                      |
|----------------|------------------|----------------------------------------------|--------------------------------------------------|
| `id`           | string           | -                                            | The ID of this component, used to identify dash components |
| `data`         | array            | -                                            | The data to display                              |
| `margin`       | object           | { top: 40, right: 100, bottom: 40, left: 100 } | Chart margin                                     |
| `spacing`      | number           | 8                                            | Spacing between each area                        |
| `colors`       | object or func   | { scheme: 'nivo' }                           | Colors used for the areas                        |
| `blendMode`    | string           | 'multiply'                                   | Blend mode for areas                             |
| `defs`         | array            | See default props                            | Defines patterns and gradients                   |
| `fill`         | array            | See default props                            | Defines how to fill areas                        |
| `startLabel`   | string or func   | 'id'                                         | Defines how to get the label of an area at the start |
| `endLabel`     | string or func   | 'id'                                         | Defines how to get the label of an area at the end |
| `axisTop`      | object           | See default props                            | Top axis configuration                           |
| `axisBottom`   | object           | See default props                            | Bottom axis configuration                        |
| `clickedPoint` | object           | null                                         | Contains data about the clicked point            |

### Responsive Circle
.. exec::docs.dash_nivo.responsivecircle
    :code: false

.. sourcetabs::docs/dash_nivo/responsivecircle.py
    :defaultExpanded: false
    :withExpandedButton: true

#### Properties

  
| Property         | Type    | Default                                      | Description                                      |
|------------------|---------|----------------------------------------------|--------------------------------------------------|
| `id`             | string  | -                                            | The ID of this component, used to identify dash components |
| `data`           | object  | -                                            | The hierarchical data to display                 |
| `margin`         | object  | { top: 20, right: 20, bottom: 20, left: 20 } | Chart margin                                     |
| `colors`         | object  | { scheme: 'nivo' }                           | Colors used for the circles                      |
| `childColor`     | object  | See default props                            | How to compute child circle color                |
| `padding`        | number  | 4                                            | Padding between each circle                      |
| `enableLabels`   | bool    | true                                         | Enable/disable labels                            |
| `labelsFilter`   | func    | label => label.node.height === 0             | Define which labels should be displayed          |
| `labelsSkipRadius` | number | 16                                           | Skip label rendering if node radius is lower than given value |
| `labelTextColor` | object  | See default props                            | How to compute label text color                  |
| `borderWidth`    | number  | 1                                            | Width of circle border                           |
| `borderColor`    | object  | See default props                            | How to compute circle border color               |
| `defs`           | array   | See default props                            | Defines patterns and gradients                   |
| `fill`           | array   | See default props                            | Defines how to fill circles                      |
| `motionConfig`   | string  | 'slow'                                       | Motion config for transitions                    |
| `zoomedId`       | string  | null                                         | ID of the zoomed circle                          |

