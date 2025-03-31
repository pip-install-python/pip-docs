import dash
from dash import html, dcc, callback, Input, Output, State
import dash_gauge as dg
import dash_mantine_components as dmc

# Based on usage_rotary_knob.py

component = dmc.Container([
    dmc.Title("DashRotaryKnob Example", order=3, ta="center", mb="lg"),
    dmc.Grid(
        gutter="xl",
        children=[
            dmc.GridCol(span={"md": 5, "sm": 12}, children=dmc.Stack(align="center", children=[
                dmc.Text("Interactive Knob", fw=500),
                dmc.Text(id="knob-value-display-docs", size="lg", mt="sm"),
                dg.DashRotaryKnob(
                    id="interactive-knob-docs",
                    skinName="s10",
                    value=50,
                    min=0,
                    max=100,
                    # format="{value}%", # Formatting might be better handled in display callback
                    style={"width": "150px", "height": "150px"} # Adjust size
                ),
            ])),
            dmc.GridCol(span={"md": 7, "sm": 12}, children=dmc.Stack([
                dmc.Text("Controls", fw=500),
                dmc.Slider(
                    id="knob-slider-docs",
                    label="Adjust with slider",
                    min=0, max=100, step=1, value=50,
                    marks=[{"value": i, "label": str(i)} for i in range(0, 101, 20)],
                    mb="lg"
                ),
                dmc.Select(
                    id="skin-selector-docs",
                    label="Change skin",
                    data=[{"label": f"Skin s{i}", "value": f"s{i}"} for i in range(1, 19)],
                    value="s10",
                    clearable=False,
                     mb="lg"
                ),

            ]))
        ]
    )
], fluid=True)

@callback(
    Output("knob-value-display-docs", "children"),
    Input("interactive-knob-docs", "value")
)
def update_knob_value_display_docs(value):
     if value is None:
        return "Current value: --"
     return f"Current value: {value:.1f}"

@callback(
    Output("interactive-knob-docs", "value"),
    Input("knob-slider-docs", "value"),
)
def update_knob_from_slider_docs(value):
    return value

@callback(
    Output("interactive-knob-docs", "skinName"),
    Input("skin-selector-docs", "value"),
)
def update_knob_skin_docs(skin_name):
    return skin_name

