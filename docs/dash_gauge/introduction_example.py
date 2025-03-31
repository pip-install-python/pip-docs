import dash
from dash import html, callback, Input, Output
import dash_gauge as dg
import dash_mantine_components as dmc

# app = dash.Dash(__name__) # Define app in your main docs entry point

component = dmc.Container([
    dmc.Title("Dash Gauge Component Suite Showcase", order=2, ta="center", mb="lg"),

    dmc.SimpleGrid(
        cols={"base": 1, "sm": 2, "lg": 3},
        spacing="lg",
        verticalSpacing="lg",
        children=[
            # 1. DashGauge Example
            dmc.Paper(
                p="md", shadow="sm", withBorder=True, children=[
                    dmc.Stack([
                        dmc.Text("DashGauge (Semicircle)", fw=500, ta="center"),
                        dmc.Center(
                            dg.DashGauge(
                                id="intro-gauge",
                                type="semicircle",
                                value=65,
                                minValue=0,
                                maxValue=100,
                                style={'width': '90%'} # Adjust width as needed
                            )
                        )
                    ])
                ]
            ),

            # 2. DashRotaryKnob Example
            dmc.Paper(
                p="md", shadow="sm", withBorder=True, children=[
                    dmc.Stack([
                        dmc.Text("DashRotaryKnob", fw=500, ta="center"),
                        dmc.Center(
                            dg.DashRotaryKnob(
                                id="intro-knob",
                                skinName="s12", # Choose a visually interesting skin
                                value=30,
                                min=0,
                                max=100,
                                style={"width": "100px", "height": "100px"} # Explicit size
                            )
                        ),
                        dmc.Text("Value: --", id="intro-knob-output", ta="center", size="sm", c="dimmed")
                    ])
                ]
            ),

            # 3. DashThermostat Example
            dmc.Paper(
                p="md", shadow="sm", withBorder=True, children=[
                    dmc.Stack([
                        dmc.Text("DashThermostat", fw=500, ta="center"),
                        dmc.Space(h=20),
                        dmc.Center(
                            dg.DashThermostat(
                                id="intro-thermostat",
                                value=21,
                                min=5,
                                max=35,
                                valueSuffix="°C",
                                style={'width': '200px', 'height': '300px'} # Control size
                            )
                        )
                    ])
                ]
            ),

            # 4. DashRCJoystick Example
            dmc.Paper(
                p="md", shadow="sm", withBorder=True, children=[
                    dmc.Stack([
                        dmc.Text("DashRCJoystick", fw=500, ta="center"),
                        dmc.Center(
                            dg.DashRCJoystick(
                                id='intro-joystick',
                                directionCountMode='Nine',
                                baseRadius=60, # Slightly smaller for grid
                                controllerRadius=30,
                            )
                        ),
                        dmc.Text("Direction: Center", id="intro-joystick-direction", ta="center", size="sm", c="dimmed"),
                        dmc.Text("Angle: N/A", id="intro-joystick-angle", ta="center", size="sm", c="dimmed"),
                        dmc.Text("Distance: 0.00", id="intro-joystick-distance", ta="center", size="sm", c="dimmed"),
                    ])
                ]
            ),

            # 5. Dash7SegmentDisplay Example
            dmc.Paper(
                p="md", shadow="sm", withBorder=True, children=[
                    dmc.Stack([
                        dmc.Text("Dash7SegmentDisplay", fw=500, ta="center"),
                        dmc.Center(
                            dg.Dash7SegmentDisplay(
                                id='intro-display',
                                value="1337",
                                count=4,
                                height=50,
                                color='cyan',
                                backgroundColor='#222222',
                                skew=True
                            )
                        )
                    ])
                ]
            ),


        ]
    )
], fluid=True, pt="xl", pb="xl")


# --- Callbacks ---

@callback(
    Output("intro-knob-output", "children"),
    Input("intro-knob", "value")
)
def update_intro_knob_output(value):
    if value is None:
        return "Value: --"
    return f"Value: {value:.1f}"

@callback(
    Output('intro-joystick-direction', 'children'),
    Output('intro-joystick-angle', 'children'),
    Output('intro-joystick-distance', 'children'),
    Input('intro-joystick', 'direction'),
    Input('intro-joystick', 'angle'),
    Input('intro-joystick', 'distance')
)
def update_intro_joystick_output(direction, angle, distance):
    angle_str = f"Angle: {angle:.1f}°" if angle is not None else "Angle: N/A"
    distance_str = f"Distance: {distance:.2f}"
    direction_str = f"Direction: {direction}"
    return direction_str, angle_str, distance_str

# Add this section if running this file standalone for testing
# if __name__ == "__main__":
#     app = dash.Dash(__name__)
#     app.layout = component
#     app.run_server(debug=True)