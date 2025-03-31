import dash
from dash import html, dcc, callback, Input, Output, State
import dash_gauge as dg
import dash_mantine_components as dmc

# Based on usage_rc_joystick.py

component = dmc.Container([
    dmc.Title("DashRCJoystick Example", order=3, ta="center", mb="lg"),
    dmc.Grid(
        gutter="xl",
        children=[
            # Left side: Joystick Component
            dmc.GridCol(span={"md": 5, "sm": 12}, children=dmc.Stack(align="center", children=[
                dmc.Text("Interactive Joystick", fw=500),
                dg.DashRCJoystick(
                    id='my-joystick-docs',
                    directionCountMode='Nine', # Default to Nine for demo
                    baseRadius=75,
                    controllerRadius=35,
                    style={'marginTop': '20px'} # Add some space
                ),
            ])),

            # Right side: Displaying Joystick State & Controls
            dmc.GridCol(span={"md": 7, "sm": 12}, children=dmc.Stack([
                dmc.Text("Joystick State", fw=500),
                dmc.Text(id='joystick-output-direction-docs', size="sm"),
                dmc.Text(id='joystick-output-angle-docs', size="sm"),
                dmc.Text(id='joystick-output-distance-docs', size="sm"),
                dmc.Divider(my="md"),
                dmc.RadioGroup(
                    [dmc.Radio(label, value=value) for label, value in
                     [('5 Directions', 'Five'), ('9 Directions', 'Nine')]],
                    id='direction-mode-selector-docs',
                    value='Nine', # Initial value matches component
                    label="Direction Mode",
                    size="sm",
                    mb="md",
                ),
                dmc.Text("Base Radius:", size="sm", fw=500),
                dmc.Slider(
                    id='base-radius-slider-docs', min=50, max=150, step=5, value=75,
                    marks=[{"value": i, "label": str(i)} for i in range(50, 151, 25)],
                    mb="md"
                ),
                dmc.Text("Controller Radius:", size="sm", fw=500),
                dmc.Slider(
                    id='controller-radius-slider-docs', min=20, max=70, step=5, value=35,
                    marks=[{"value": i, "label": str(i)} for i in range(20, 71, 10)],
                    mb="md"
                 ),
            ]))
        ])
], fluid=True)


# Callback to display joystick state changes
@callback(
    Output('joystick-output-direction-docs', 'children'),
    Output('joystick-output-angle-docs', 'children'),
    Output('joystick-output-distance-docs', 'children'),
    Input('my-joystick-docs', 'direction'),
    Input('my-joystick-docs', 'angle'),
    Input('my-joystick-docs', 'distance')
)
def update_joystick_output_docs(direction, angle, distance):
    angle_str = f"Angle: {angle:.1f}°" if angle is not None else "Angle: N/A (Center)"
    distance_str = f"Distance: {distance:.2f}"
    direction_str = f"Direction: {direction}"
    return direction_str, angle_str, distance_str

# Callback to update joystick configuration from controls
@callback(
    Output('my-joystick-docs', 'directionCountMode'),
    Output('my-joystick-docs', 'baseRadius'),
    Output('my-joystick-docs', 'controllerRadius'),
    Input('direction-mode-selector-docs', 'value'),
    Input('base-radius-slider-docs', 'value'),
    Input('controller-radius-slider-docs', 'value'),
)
def update_joystick_config_docs(direction_mode, base_radius, controller_radius):
    return direction_mode, base_radius, controller_radius