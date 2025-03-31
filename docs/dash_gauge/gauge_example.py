import dash
from dash import html, dcc, callback, Input, Output
import dash_gauge as dg
import dash_mantine_components as dmc

# Based on usage_gauge.py

component = dmc.Container([
    dmc.Title("DashGauge Examples", order=3, ta="center", mb="lg"),
    dmc.SimpleGrid(
        cols={"base": 1, "sm": 1, "lg": 3},
        spacing="lg",
        children=[
            dmc.Paper(p="md", shadow="sm", withBorder=True, children=dmc.Stack([
                dmc.Text("Basic Gauge", fw=500, ta="center"),
                dmc.Center(
                    dg.DashGauge(
                        id="basic-gauge-docs",
                        value=50,
                        style={'width': '90%'}
                    )
                )
            ])),
            dmc.Paper(p="md", shadow="sm", withBorder=True, children=dmc.Stack([
                dmc.Text("Temperature Gauge (Semicircle)", fw=500, ta="center"),
                dmc.Center(
                    dg.DashGauge(
                        id="temperature-gauge-docs",
                        type="semicircle",
                        value=22.5,
                        minValue=10,
                        maxValue=35,
                        arc={
                            "width": 0.2, "padding": 0.005, "cornerRadius": 1,
                            "subArcs": [
                                {"limit": 15, "color": "#EA4228", "showTick": True, "tooltip": {"text": "Too low!"}},
                                {"limit": 17, "color": "#F5CD19", "showTick": True, "tooltip": {"text": "Low"}},
                                {"limit": 28, "color": "#5BE12C", "showTick": True, "tooltip": {"text": "OK"}},
                                {"limit": 30, "color": "#F5CD19", "showTick": True, "tooltip": {"text": "High"}},
                                {"color": "#EA4228", "tooltip": {"text": "Too high!"}}
                            ]
                        },
                        pointer={"color": "#345243", "length": 0.80, "width": 15},
                        labels={"valueLabel": {"style": {"fontSize": "30px"}}}, # Simplified labels
                        style={'width': '90%'}
                    )
                )
            ])),
            dmc.Paper(p="md", shadow="sm", withBorder=True, children=dmc.Stack([
                dmc.Text("Bandwidth Gauge (Radial)", fw=500, ta="center"),
                dmc.Center(
                    dg.DashGauge(
                        id="bandwidth-gauge-docs",
                        type="radial", # Changed type for variety
                        value=900,
                        maxValue=3000,
                        arc={
                            "nbSubArcs": 150,
                            "colorArray": ["#5BE12C", "#F5CD19", "#EA4228"],
                            "width": 0.3, # Adjusted width for radial
                            "padding": 0.003
                        },
                         style={'width': '90%'}
                    )
                )
            ])),
        ]
    ),
    dmc.Space(h="xl"),
    dmc.Paper(p="md", shadow="sm", withBorder=True, children=dmc.Stack([
        dmc.Text("Interactive Gauge", fw=500, ta="center"),
        dmc.Text("Use the slider to update the gauge value:", size="sm", ta="center"),
        dmc.Slider(
            id="gauge-slider-docs",
            min=0, max=100, step=1, value=40,
            labelTransitionProps={
                "transition": "skew-down",
                "duration": 150,
                "timingFunction": "linear",
            },
        ),
        dmc.Center(
            dg.DashGauge(
                id="interactive-gauge-docs",
                type="radial",
                value=50, # Initial value linked to slider
                arc={
                    "colorArray": ["#5BE12C", "#EA4228"],
                    "subArcs": [{"limit": 10}, {"limit": 30}, {}, {}, {}],
                    "padding": 0.02,
                    "width": 0.3
                },
                pointer={"elastic": True, "animationDelay": 0},
                labels={
                    "tickLabels": {"type": "inner", "ticks": [{"value": i} for i in range(20, 101, 20)]}
                },
                 style={'width': '300px', 'marginTop': '20px'} # Control size
            )
        )
    ]))
], fluid=True)

@callback(
    Output("interactive-gauge-docs", "value"),
    Input("gauge-slider-docs", "value")
)
def update_gauge_docs(value):
    return value