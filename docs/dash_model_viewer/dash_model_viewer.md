---
name: Model Viewer
description: Embed interactive 3D models with AR support into Dash applications using Google's model-viewer.
endpoint: /pip/dash_model_viewer
package: dash_model_viewer
icon: mdi:cube-scan
---

.. toc::

[Visit GitHub Repo](https://github.com/pip-install-python/dash-model-viewer) 

`dash-model-viewer` is a Dash component library that wraps Google's `model-viewer` web component, allowing you to easily display and interact with 3D models (.glb, .gltf) within your Python Dash dashboards. It features interactive controls, Augmented Reality (AR) support via WebXR, annotations, dynamic updates, and extensive customization options.

### Installation

```bash
pip install dash-model-viewer
```

---

### Quick Start

Embed a 3D model with basic controls and AR capability.

.. exec::docs.dash_model_viewer.quick_start_example
    :code: false

.. sourcetabs::docs/dash_model_viewer/quick_start_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Camera Views via Hotspots

Configure hotspots to act as camera position presets. Clicking a hotspot with `orbit` and `target` defined will automatically animate the camera to that view. The component handles this interaction internally.

.. exec::docs.dash_model_viewer.camera_views_example
    :code: false

.. sourcetabs::docs/dash_model_viewer/camera_views_example.py
    :defaultExpanded: false
    :withExpandedButton: true

**Note:** The example uses pre-scaled values for orbit/target suitable for the specific model. You might need to adjust these values or use scaling functions (like in the original `usage_camera_views.py`) for your own models.

---

### Dynamic Model Switching

Update the `src` property of the `DashModelViewer` component using a standard Dash callback to load different 3D models interactively.

.. exec::docs.dash_model_viewer.dynamic_switching_example
    :code: false

.. sourcetabs::docs/dash_model_viewer/dynamic_switching_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Advanced: Dynamic Dimensions

This example demonstrates controlling hotspot *presence* via Dash callbacks and relies on **client-side JavaScript** (not included in this basic demo) to:
1. Calculate model dimensions using the `model-viewer` API.
2. Position the hotspots correctly based on the bounding box.
3. Draw SVG lines between hotspots to visualize dimensions.
4. Handle unit conversions.

The Python code sets up the necessary controls and toggles the hotspot list passed to the component.

**Requires:** Corresponding JavaScript in `assets/model_viewer_clientside.js` and CSS in `assets/dimensions_styles.css` for full functionality.

.. exec::docs.dash_model_viewer.dynamic_dimensions_example
    :code: false

.. sourcetabs::docs/dash_model_viewer/dynamic_dimensions_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Advanced: Interactive Hotspot Placement

This example demonstrates a setup for allowing users to dynamically add hotspots to a model. It uses Dash callbacks and `dcc.Store` to manage the application state (viewing vs. adding mode) and relies on **client-side JavaScript** to:
1. Capture the user's click intention when in "Place Hotspot" mode.
2. Use the `model-viewer` API (`positionAndNormalFromPoint`) to get the 3D position and surface normal at the center of the viewer (where the reticle is).
3. Send this data back to the server via a `dcc.Store`.
4. The server-side callback then updates the list of hotspots displayed by the component.

**Requires:** Corresponding JavaScript in `assets/model_viewer_clientside.js` and CSS for the reticle/hotspots in `assets/dynamic_hotspots.css` for full functionality.

.. exec::docs.dash_model_viewer.dynamic_hotspots_example
    :code: false

.. sourcetabs::docs/dash_model_viewer/dynamic_hotspots_example.py
    :defaultExpanded: false
    :withExpandedButton: true

---

### Component Properties (API Reference)

| Property           | Type                                | Default                                    | Description                                                                                                     |
| :----------------- | :---------------------------------- | :----------------------------------------- |:----------------------------------------------------------------------------------------------------------------|
| **`id`**           | `string`                            | **Required**                               | Unique identifier for the component.                                                                            |
| **`src`**          | `string`                            | **Required**                               | URL to the 3D model file (.glb, .gltf). Can be absolute or relative to assets folder.                           |
| **`alt`**          | `string`                            | **Required**                               | Alternative text description for accessibility.                                                                 |
| `style`            | `object`                            | `{}`                                       | Standard CSS styles for the outer container.                                                                    |
| `cameraControls`   | `bool`                              | `True`                                     | Enable user interaction to control the camera (orbit, zoom, pan).                                               |
| `touchAction`      | `'pan-y'`, `'pan-x'`, `'none'`      | `'pan-y'`                                  | How touch gestures interact with the model (vertical pan, horizontal pan, or none).                             |
| `cameraOrbit`      | `string`                            | `undefined`                                | Sets the initial/current camera position (`theta phi radius`, e.g., `0deg 75deg 1.5m`).                         |
| `cameraTarget`     | `string`                            | `undefined`                                | Sets the point the camera looks at (`X Y Z`, e.g., `0m 1m 0m`).                                                 |
| `fieldOfView`      | `string`                            | `'auto'`                                   | Camera's vertical field of view (e.g., `'45deg'`).                                                              |
| `minFieldOfView`   | `string`                            | `'25deg'`                                  | Minimum vertical field of view allowed.                                                                         |
| `maxFieldOfView`   | `string`                            | `'auto'`                                   | Maximum vertical field of view allowed.                                                                         |
| `interpolationDecay`| `number` or `string`                | `50`                                       | Controls the speed of camera transitions (higher is faster decay, slower transition). 0 is instant.             |
| `minCameraOrbit`   | `string`                            | `'auto auto auto'`                         | Sets minimum bounds for camera orbit (`theta phi radius`, use 'auto' for no limit).                             |
| `maxCameraOrbit`   | `string`                            | `'auto auto auto'`                         | Sets maximum bounds for camera orbit.                                                                           |
| `poster`           | `string`                            | `undefined`                                | URL of an image to show before the model loads. Can be absolute or relative to assets.                          |
| `ar`               | `bool`                              | `True`                                     | Enables AR features and displays the AR button if supported.                                                    |
| `arModes`          | `string`                            | `"webxr scene-viewer quick-look"`          | Space-separated list of preferred AR modes.                                                                     |
| `arScale`          | `'auto'`, `'fixed'`                 | `'auto'`                                   | Controls model scaling in AR ('auto' tries world scale, 'fixed' uses model's scene units).                      |
| `arButtonText`     | `string`                            | `'View in your space'`                     | Text displayed on the default AR button.                                                                        |
| `customArPrompt`   | `node` (string or Dash component)   | `null`                                     | Custom content to show while initializing AR (replaces default hand icon). Pass Dash components directly.       |
| `customArFailure`  | `node` (string or Dash component)   | `null`                                     | Custom content to show if AR fails to start or track (replaces default message). Pass Dash components directly. |
| `toneMapping`      | `'neutral'`, `'aces'`, ...         | `'neutral'`                                | Adjusts the color grading/tone mapping (see `model-viewer` docs for options like 'agx').                        |
| `shadowIntensity`  | `number` or `string`                | `0`                                        | Controls the opacity of the model's shadow (0 to 1).                                                            |
| `hotspots`         | `array`                             | `[]`                                       | List of hotspot configuration objects (see structure below).                                                    |
| `variantName`      | `string`                            | `null`                                     | Selects a specific model variant if the GLTF file defines variants. Use `null` or `'default'` for default.      |
| `setProps`         | `func`                              | (Dash Internal)                            | Callback function to update component properties.                                                               |
| `loading_state`    | `object`                            | (Dash Internal)                            | Object describing the loading state of the component or its props.                                              |

**Hotspot Object Structure:**

Each object in the `hotspots` array represents a `div` placed inside the `model-viewer` and can have the following keys:

*   `slot`: (String, Required) A unique name for the hotspot's `slot` attribute (e.g., `"hotspot-1"`, `"hotspot-visor"`). Used for targeting with CSS (`.hotspot[slot='...']`).
*   `position`: (String, Required) The 3D coordinates `"X Y Z"` where the hotspot should be placed in model space (e.g., `"0 1.75 0.35"`).
*   `normal`: (String, Optional) The surface normal vector `"X Y Z"` at the position (e.g., `"0 0 1"`). Influences the hotspot's orientation relative to the surface.
*   `text`: (String, Optional) Text content to display *inside* the hotspot's `div` element.
*   `children_classname`: (String, Optional) A CSS class name to add *in addition* to `.hotspot` on the hotspot's `div` element for custom styling (e.g., `"view-button"`).
*   `orbit`: (String, Optional) If provided, clicking this hotspot will internally update the model viewer's camera orbit to this value (e.g., `"45deg 60deg 2m"`). Used for [Camera Views via Hotspots](#camera-views-via-hotspots).
*   `target`: (String, Optional) If provided along with `orbit`, clicking this hotspot updates the camera target (e.g., `"0m 1m 0m"`).
*   `fov`: (String, Optional) If provided along with `orbit`/`target`, clicking updates the field of view (e.g., `"30deg"`). Defaults to `45deg` for camera view hotspots if not specified.

---

### Client-Side Scripting

For interactions beyond the built-in capabilities (like dynamic dimension drawing or complex hotspot logic), leverage Dash's `clientside_callback` mechanism.

1.  Create a JavaScript file in your `assets` folder (e.g., `assets/model_viewer_clientside.js`).
2.  Define functions within a namespace (e.g., `window.dash_clientside.clientside.modelViewer`).
3.  Use `dash.clientside_callback` and `dash.ClientsideFunction` in Python to trigger these JS functions based on Dash Inputs/States.
4.  Your JavaScript function can access the `model-viewer` DOM element using its `id` and interact with its powerful [JavaScript API](https://modelviewer.dev/docs/index.html#javascript-api).

Refer to the "Advanced" examples (`dynamic_dimensions_example.py`, `dynamic_hotspots_example.py`) and their corresponding `usage_*.py` files in the GitHub repository for implementation patterns.

---

### Styling

Style the component and its hotspots using CSS in your `assets` folder.

*   Target the viewer container: `#your-viewer-id { border: 1px solid blue; }`
*   Target all hotspots: `.hotspot { background-color: rgba(0, 0, 0, 0.5); color: white; padding: 4px 8px; border-radius: 4px; }`
*   Target specific hotspots: `.hotspot[slot='hotspot-visor'] { background-color: red; }`
*   Target custom hotspot classes: `.view-button { cursor: pointer; border: 1px solid white; }`
*   Style the AR button: `button[slot='ar-button'] { background-color: purple; color: white; }`

See the CSS files associated with the usage examples in the GitHub repo for more detailed styling examples.

---

### Acknowledgements

*   This component is built upon Google's [`model-viewer` web component](https://modelviewer.dev/).
*   Developed using the [Plotly Dash](https://dash.plotly.com/) framework.