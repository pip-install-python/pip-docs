from dash import *
import dash_leaflet as dl
import dash_mantine_components as dmc

# Default marker settings
DEFAULT_POSITION = [56, 10]
DEFAULT_ROTATION = 95
DEFAULT_ROTATION_ORIGIN = 'center center'
DEFAULT_ICON = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png"

# Available rotation origin options
ROTATION_ORIGINS = [
    {'value': 'center center', 'label': 'Center'},
    {'value': 'bottom center', 'label': 'Bottom'},
    {'value': 'top center', 'label': 'Top'},
    {'value': 'center left', 'label': 'Left'},
    {'value': 'center right', 'label': 'Right'},
]

component = html.Div([
    dmc.Container([
        dmc.Grid([
            dmc.GridCol(span=6, children=[
                dmc.Paper(
                    shadow="xs",
                    p="md",
                    children=[
                        dmc.TextInput(
                            id="icon-url",
                            label="Marker Icon URL",
                            value=DEFAULT_ICON,
                            style={"marginBottom": 10}
                        ),
                        dmc.Grid([
                            dmc.GridCol(span=6, children=[
                                dmc.NumberInput(
                                    id="lat-input",
                                    label="Latitude",
                                    value=DEFAULT_POSITION[0],
                                    step=0.1,
                                    style={"marginBottom": 10}
                                ),
                            ]),
                            dmc.GridCol(span=6, children=[
                                dmc.NumberInput(
                                    id="lon-input",
                                    label="Longitude",
                                    value=DEFAULT_POSITION[1],
                                    step=0.1,
                                    style={"marginBottom": 10}
                                ),
                            ]),
                        ]),
                        dmc.NumberInput(
                            id="rotation-input",
                            label="Rotation Angle (degrees)",
                            value=DEFAULT_ROTATION,
                            step=5,
                            style={"marginBottom": 10}
                        ),
                        dmc.Select(
                            id="rotation-origin-select",
                            label="Rotation Origin",
                            data=ROTATION_ORIGINS,
                            value=DEFAULT_ROTATION_ORIGIN,
                            style={"marginBottom": 10}
                        ),
                        dmc.Button(
                            "Update Marker",
                            id="update-button",
                            variant="filled",
                            color="green",
                            fullWidth=True
                        ),
                    ]
                )
            ]),
            dmc.GridCol(span=6, children=dl.Map(
                id='rotation_map',
                center=DEFAULT_POSITION,
                children=[dl.TileLayer()],
                zoom=13,
                style={'height': '50vh', 'width': '100%'}
            ))
        ])
    ])
])

@callback(
    Output("rotation_map", "children"),
    Output('update-button', 'children'),
    Output('update-button', 'color'),
    Input("update-button", "n_clicks"),
    State("lat-input", "value"),
    State("lon-input", "value"),
    State("rotation-input", "value"),
    State("rotation-origin-select", "value"),
    State("icon-url", "value"),
    prevent_initial_call=True
)
def update_marker(n_clicks, lat, lon, rotation, rotation_origin, icon_url):
    if n_clicks %2 != 0:
        print(f"Updating marker with rotation={rotation}, origin={rotation_origin}")

        # Ensure rotation is a number
        rotation = float(rotation) if rotation is not None else DEFAULT_ROTATION

        # Ensure rotation_origin is a string and has a valid value
        if rotation_origin not in [opt['value'] for opt in ROTATION_ORIGINS]:
            rotation_origin = DEFAULT_ROTATION_ORIGIN

        icon = {
            'iconUrl': icon_url,
            'iconSize': [25, 41],
            'iconAnchor': [12, 41],
        }

        pos = [float(lat) if lat is not None else DEFAULT_POSITION[0],
               float(lon) if lon is not None else DEFAULT_POSITION[1]]

        marker = dl.RotatedMarker(
            id="rotated-marker",
            position=pos,
            rotationAngle=rotation,
            rotationOrigin=rotation_origin,
            icon=icon
        )

        return [marker, dl.TileLayer()], 'Reset Map', 'gray'
    return [dl.TileLayer()], 'Update Marker', 'green'



