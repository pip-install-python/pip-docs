---
name: Dynamic Grid Layout
description: A Dash component library for creating dynamic grid layouts.
endpoint: /pip/dash_dynamic_grid_layout
package: dash_dynamic_grid_layout
icon: uim:grid
---

.. toc::

[Visit GitHub Repo](https://github.com/pip-install-python/dash-dynamic-grid-layout)

Dash Dynamic Grid Layout is a Dash component library that provides a flexible grid layout system for arranging and moving components within a Dash application.

.. exec::docs.dash_dynamic_grid_layout.example
    :code: false
## Features

- Drag-and-drop functionality for rearranging components
- Resizable grid items
- Customizable layout with responsive breakpoints
- Option to add or remove items dynamically
- Customizable drag handles for each item

```bash
pip install dash-dynamic-grid-layout
```

### Usage
Here's a basic example of how to use the DashGridLayout component:

### Example

.. exec::docs.dash_dynamic_grid_layout.intro

## Prop Reference
### DashGridLayout

| Property         | Type   | Default | Description                                                   |
|------------------|--------|---------|---------------------------------------------------------------|
| id               | string | -       | The ID used to identify this component in Dash callbacks      |
| children         | list   | -       | A list of dash components to be rendered in the grid          |
| currentLayout    | list   | []      | The current layout of the grid items                          |
| rowHeight        | number | 100     | The height of a single row in pixels                          |
| cols             | dict   | { lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 } | An object containing breakpoints and column numbers |
| compactType      | string | 'vertical' | Compaction type. Can be 'vertical', 'horizontal', or null |
| showRemoveButton | bool   | True    | Whether to show remove buttons for grid items                 |
| showResizeHandles| bool   | True    | Whether to show resize handles for grid items                 |

### DraggableWrapper

| Property         | Type   | Default       | Description                                      |
|------------------|--------|---------------|--------------------------------------------------|
| children         | node   | -             | The content to be wrapped and made draggable     |
| handleBackground | string | "rgb(85,85,85)"| Background color of the drag handle              |
| handleColor      | string | "white"       | Text color of the drag handle                    |
| handleText       | string | "Drag here"   | Text to display in the drag handle               |
### Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Special thanks to [BSd3v](https://github.com/BSd3v) for contributing the improvements and bug fixes making this a much more polished project.

### License
This project is licensed under the MIT License.
