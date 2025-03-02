
---
name: Leaflet
description: Some custom components I've built to complement dash leaflet.
endpoint: /pip/dash_leaflet
package: dash_leaflet
icon: gis:poi-map-o
---

.. toc::

[Visit the Github Repo Fork](https://github.com/pip-install-python/dash-leaflet)


### Installation

This isn't a full feature pip component only a .tar.gz file that can be installed in your project. First you'll need to download the file via:
.. exec::docs.dash_leaflet.download_code
    :code: false

then you'll need to place it in the root of your project and install it via:
```bash
pip install dash-leaflet-1.0.18.tar.gz
```

## Introduction
This is a fork of the dash-leaflet package that I've added some custom components to. This project contains all the components from the original dash-leaflet package, but with some additional components like the `RotatedMarker` and `AntPath` components and improvements to the edit controls.

### RotatedMarker Component
The first example was designed to showcase how with a RotatedMarker you can use math and callbacks to rotate a marker as it follows a polyline. Like in this uber-like map following the marker example.
.. exec::docs.dash_leaflet.track_player
    :code: false
This second example was designed to showcase the props and how they affect the roted marker. Like in this example where you can change the rotation angle of the marker.
.. exec::docs.dash_leaflet.marker_rotation
    :code: false
The RotatedMarker component extends the basic Leaflet marker functionality to support rotation. It's built on top of the react-leaflet Marker component and uses the leaflet-marker-rotation plugin.

#### Example Usage
```python
import dash_leaflet as dl
from dash import *
import dash

app = dash.Dash(__name__)

app.layout = html.Div([
    dl.Map([
        dl.TileLayer(),
        dl.RotatedMarker(
            position=[51.515, -0.09],
            rotation_angle=45,
            rotationOrigin='center',
            id='rotated_marker_id',
            icon={
    "iconUrl": "https://e7.pngegg.com/pngimages/612/120/png-clipart-finger-icon-finger-touch-person-s-hand-pointing-up-hand-people-thumbnail.png",
    "iconSize": [15, 25],
    "iconAnchor": [10, 10],
    "popupAnchor": [0, 0],
})
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
```
#### RotatedMarker Props

| Prop           | Type                                 | Default         | Description                                                                                                                                                                                             |
|----------------|--------------------------------------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| position       | L.LatLngExpression                   | Required        | The geographical position of the marker on the map (latitude and longitude).                                                                                                                            |
| icon           | L.IconOptions \| null                | null            | Options for customizing the marker's icon appearance. When null, uses Leaflet's default marker icon. See [Leaflet Icon documentation](https://leafletjs.com/reference.html#icon) for available options. |
| rotationAngle  | number                               | 0               | The angle (in degrees) to rotate the marker clockwise.                                                                                                                                                  |
| rotationOrigin | string                               | 'center center' | Defines the origin point for the rotation transformation, specified as a CSS transform-origin value (e.g., 'bottom center', 'center center').                                                           |
| onClick        | (event: L.LeafletMouseEvent) => void | -               | Handler function called when the marker is clicked.                                                                                                                                                     |
| onDblClick     | (event: L.LeafletMouseEvent) => void | -               | Handler function called when the marker is double-clicked.                                                                                                                                              |
| onMouseDown    | (event: L.LeafletMouseEvent) => void | -               | Handler function called when a mouse button is pressed on the marker.                                                                                                                                   |
| onMouseUp      | (event: L.LeafletMouseEvent) => void | -               | Handler function called when a mouse button is released on the marker.                                                                                                                                  |
| onMouseOver    | (event: L.LeafletMouseEvent) => void | -               | Handler function called when the mouse enters the marker.                                                                                                                                               |
| onMouseOut     | (event: L.LeafletMouseEvent) => void | -               | Handler function called when the mouse leaves the marker.                                                                                                                                               |
| onContextMenu  | (event: L.LeafletMouseEvent) => void | -               | Handler function called when the marker is right-clicked.                                                                                                                                               |

#### Notes

- The component automatically handles rotation updates when the rotationAngle or rotationOrigin props change.

- Custom icons can be specified using the icon prop, following Leaflet's IconOptions interface.

- All mouse event handlers receive a Leaflet MouseEvent object as their argument.

- The component integrates with react-leaflet and must be used within a MapContainer component.


### AntPath Component
The AntPath component creates animated polylines with a marching-ants effect using the leaflet-ant-path plugin. It's perfect for visualizing routes or paths with a dynamic flow animation.

.. exec::docs.dash_leaflet.ant_path
    :code: false
#### AntPath Props


| Prop | Type | Default | Description |
|------|------|---------|-------------|
| id | `string` | `undefined` | The unique identifier for the component. |
| positions | `L.LatLngExpression[] \| L.LatLngExpression[][]` | Required | Array of latitude/longitude points defining the path. Can be a single array for lines or an array of arrays for complex shapes. |
| delay | `number` | `400` | Animation delay in milliseconds. Controls the speed of the marching ants effect. |
| dashArray | `[number, number] \| string` | `[10, 20]` | Size of the animated dashes. Can be provided as [dash_size, gap_size] array or a string. |
| pulseColor | `string` | `"#FFFFFF"` | Color of the animated dash flow (the "marching ants"). |
| color | `string` | `"#0000FF"` | Base color of the path. |
| weight | `number` | `5` | Width of the path in pixels. |
| paused | `boolean` | `false` | Whether the animation starts in a paused state. |
| reverse | `boolean` | `false` | Whether to reverse the animation direction. |
| hardwareAccelerated | `boolean` | `true` | Whether to use hardware acceleration for the animation. |
| interactive | `boolean` | `true` | Whether the path should respond to mouse/touch events. |
| children | `React.ReactNode` | `undefined` | Optional child components like popups or tooltips. |
| n_clicks | `number` | `undefined` | Number of times the path has been clicked. |
| clickData | `object` | `undefined` | Data from the latest click event. |
| setProps | `(props: Record<string, any>) => void` | `undefined` | Callback to update props (used in Dash). |

#### Example Usage

```python
from dash_leaflet import AntPath

# Simple polyline
antpath = AntPath(
    id='my-antpath',
    positions=[[51.508, -0.11], [51.503, -0.06], [51.51, -0.047]],
    color="#0000FF",
    pulseColor="#FFFFFF",
    delay=800,
    weight=5,
    dashArray=[10, 20],
    paused=False,
    reverse=False
)

# Closed polygon
polygon_path = AntPath(
    id='polygon-path',
    positions=[
        [51.515, -0.12],
        [51.52, -0.10],
        [51.525, -0.13],
        [51.515, -0.12]  # Close the polygon
    ],
    color="#FF0000",
    pulseColor="#FFFF00",
    delay=400,
    weight=8
)
```

#### Notes

- The component supports various path types: polylines, polygons, rectangles, and circles (approximated with points)
- Animation can be controlled through the `paused` and `reverse` props
- The `dashArray` property controls the appearance of the marching ants effect
- Supports all standard Leaflet mouse events through the interactive property
- Must be used within a Leaflet map container
- The animation performance can be optimized using the `hardwareAccelerated` prop

### EditControl Component
This is an improved Edit Control component that works in partnership with [dash-emoji-mart](https://pip-install-python.com/pip/dash_emoji_mart) and [dash mantine component colorInput](https://www.dash-mantine-components.com/components/colorinput) so allow real time changes in markers or color changes in drawings on a map.
.. exec::docs.dash_leaflet.edit_controls
    :code: false


