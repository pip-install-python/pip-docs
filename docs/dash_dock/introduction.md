---
name: Dock
description: Dynamic Dock window management / layout system for dash.
endpoint: /pip/dash_dock
package: dash_dock
icon: tabler:layout-sidebar-right-collapse
---

.. toc::

[Visit the Github Repo](https://github.com/pip-install-python/dash-dock)


### Features

- Create dock-able, resizable, and floatable windows in your Dash apps
- Drag and drop tabs between dock containers
- Maximize, close, and pop-out tabs
- Compatible with both Dash 2 and Dash 3
- Free version with up to 3 tabs
- Premium version with unlimited tabs (requires API key)

### Installation

```bash
pip install dash-dock
```

### Simple Example

.. exec::docs.dash_dock.simple_usage
    :code: false

.. sourcetabs::docs/dash_dock/simple_usage.py
    :defaultExpanded: false
    :withExpandedButton: true

## Premium Version

DashDock is available in two versions:

- **Free Version**: Limited to 3 tabs
- **Premium Version**: Unlimited tabs (requires API key)

To use the premium version, obtain an API key and include it in your DashDock component:

```python
dash_dock.DashDock(
    id='dock-layout',
    model=dock_config,
    children=tab_components,
    apiKey="your-api-key-here"
)
```

.. exec::docs.dash_dock.api_example
    :code: false

.. sourcetabs::docs/dash_dock/api_example.py
    :defaultExpanded: false
    :withExpandedButton: true

### Getting an API Key

Visit [My Shop](https://shop.geomapindex.com/catalogue/dash-dock_1/) to obtain an API key for the premium version.

* After purchase, I will send api keys to the email used on purchase within 24h 

### Component Properties

#### DashDock

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | The ID used to identify this component |
| `model` | object | FlexLayout model configuration |
| `children` | list | React components to render in the tabs |
| `headers` | object | Custom headers for tabs |
| `useStateForModel` | boolean | Use internal state for the model (default: false) |
| `font` | object | Override font styles for tabs |
| `supportsPopout` | boolean | Whether pop-out windows are supported |
| `popoutURL` | string | URL for pop-out windows |
| `realtimeResize` | boolean | Resize tabs during dragging (default: false) |
| `apiKey` | string | API key for premium features |
| `freeTabLimit` | number | Maximum number of tabs in free version (default: 3) |
| `debugMode` | boolean | Enable debug mode (default: false) |

#### Tab

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | The ID used to identify this tab |
| `children` | list | React components to render in the tab |


### License

This was created under the [Pip Install Python LLC](https://pip-install-python.com) and licensed under the MIT License.


    