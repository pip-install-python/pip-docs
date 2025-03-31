import dash
from dash import html, dcc, callback, Input, Output, State
import dash_gauge as dg
import dash_mantine_components as dmc

# Based on usage_thermostat.py, but simplified for docs

# Define some example colors
cool_colors = ['#dae8eb', '#2c8e98']
heat_colors = ['#cfac48', '#cd5401']

component = dmc.Container([
    dmc.Title("DashThermostat Example", order=3, ta="center", mb="lg"),
    dmc.Grid(
        gutter="xl",
        children=[
            dmc.GridCol(span={"md": 6, "sm": 12}, children=dmc.Stack(align="center", children=[
                 dmc.Text("Thermostat Control", fw=500),
                 dmc.Space(h=20),
                 dg.DashThermostat(
                    id='thermostat-docs',
                    value=21,
                    min=5,
                    max=35,
                    valueSuffix='°C',
                    track={'colors': cool_colors}, # Start with cool colors
                    style={'width': '250px', 'height': '350px', 'marginBottom': '20px'},
                 )
            ])),
             dmc.GridCol(span={"md": 6, "sm": 12}, children=dmc.Stack([
                 dmc.Text("Controls", fw=500),
                 dmc.Text("Set Temperature:", size="sm"),
                 dmc.Slider(
                     id="thermostat-slider-docs",
                     min=5, max=35, step=0.5, value=21,
                     marks=[{"value": v, "label": f"{v}°"} for v in range(5, 36, 5)],
                     style={"maxWidth": 300},
                     mb="lg"
                 ),
                 dmc.Text("Current Setting:", size="sm"),
                 dmc.Title(id="thermostat-value-display-docs", order=4, ta="center"),
                 dmc.Space(h="lg"),
                 dmc.Text("Toggle Disabled:", size="sm"),
                 dmc.Switch(id="thermostat-disable-switch-docs", label="Disable Thermostat", checked=False),
                 dmc.Space(h="lg"),
                 dmc.Text("Change Track Color:", size="sm"),
                  dmc.SegmentedControl(
                    id="thermostat-color-switch-docs",
                    value="cool",
                    data=[
                        {"label": "Cool Mode", "value": "cool"},
                        {"label": "Heat Mode", "value": "heat"},
                    ],
                    fullWidth=True,
                    mb="md",
                ),
             ]))
        ]
    )
], fluid=True)

@callback(
    Output('thermostat-docs', 'value'),
    Input('thermostat-slider-docs', 'value')
)
def update_thermostat_from_slider(value):
    return value

@callback(
    Output('thermostat-value-display-docs', 'children'),
    Input('thermostat-docs', 'value')
)
def display_thermostat_value(value):
    if value is None:
        return "-- °C"
    return f"{value:.1f} °C"

@callback(
    Output('thermostat-docs', 'disabled'),
    Input('thermostat-disable-switch-docs', 'checked')
)
def toggle_thermostat_disabled(checked):
    return checked

@callback(
    Output('thermostat-docs', 'track'),
    Input('thermostat-color-switch-docs', 'value'),
    State('thermostat-docs', 'track') # Get current track state if needed
)
def update_thermostat_track_color(mode, current_track):
    # Ensure track is a dictionary before modifying
    track_config = current_track if isinstance(current_track, dict) else {}
    if mode == 'cool':
        track_config['colors'] = cool_colors
    elif mode == 'heat':
        track_config['colors'] = heat_colors
    # Add other track properties if they exist, e.g., thickness
    # track_config['thickness'] = current_track.get('thickness', 0.2) # Example
    return track_config