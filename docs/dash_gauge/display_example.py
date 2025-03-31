import dash
from dash import html, dcc, callback, Input, Output
import dash_gauge as dg
import dash_mantine_components as dmc

# Based on usage_7_segment_display.py

# Common colors for dropdown
color_options = [
    {"label": "Red", "value": "red"}, {"label": "Blue", "value": "blue"},
    {"label": "Green", "value": "lime"}, {"label": "Yellow", "value": "yellow"},
    {"label": "Cyan", "value": "cyan"}, {"label": "Orange", "value": "orange"},
    {"label": "Black", "value": "black"}, {"label": "White", "value": "white"},
]

bg_color_options = [
    {'label': 'Dark Gray', 'value': '#222222'}, {'label': 'Black', 'value': '#111111'},
    {'label': 'None', 'value': ''}
] + color_options

component = dmc.Container([
    dmc.Title("Dash7SegmentDisplay Example", order=3, ta="center", mb="lg"),
    dmc.Grid(
        gutter="xl",
        children=[
            # Left side: Display Component
            dmc.GridCol(span={"md": 5, "sm": 12}, children=dmc.Stack(align="center", children=[
                dmc.Text("Display Output", fw=500),
                dg.Dash7SegmentDisplay(
                    id='my-display-docs',
                    value="1235",
                    count=5,
                    height=80,
                    color='cyan',
                    backgroundColor='#222222',
                    skew=True,
                    style={'marginTop': '20px', 'marginBottom': '20px'}
                ),
                # Optional second display
                dg.Dash7SegmentDisplay(
                    id='my-display-hex-docs',
                    value="A0B1", # Example Hex
                    count=4,
                    height=60,
                    color='orange',
                    backgroundColor='#111111',
                 ),
            ])),

            # Right side: Controls
            dmc.GridCol(span={"md": 7, "sm": 12}, children=dmc.Stack([
                dmc.Text("Controls", fw=500),
                dmc.TextInput(
                    id='display-value-input-docs',
                    label="Value (Number or Hex String)",
                    value='1235',
                    mb="sm"
                ),
                dmc.Text("Number of Digits (count):", size="sm", fw=500),
                dmc.Slider(
                    id='display-count-slider-docs', min=1, max=10, step=1, value=5,
                    marks=[{"value": i, "label": str(i)} for i in range(1, 11)],
                    mb="sm"
                ),
                 dmc.Text("Digit Height (pixels):", size="sm", fw=500),
                dmc.Slider(
                    id='display-height-slider-docs', min=20, max=200, step=10, value=80,
                    marks=[{"value": i, "label": str(i)} for i in range(20, 201, 40)],
                    mb="sm"
                 ),
                dmc.Select(
                    id='display-color-dropdown-docs',
                    label="Segment Color", data=color_options, value='cyan',
                    clearable=False, mb="sm"
                 ),
                dmc.Select(
                    id='display-bgcolor-dropdown-docs',
                    label="Background Color", data=bg_color_options, value='#222222',
                    clearable=False, mb="sm"
                 ),
                dmc.Checkbox(
                    id='display-skew-checklist-docs',
                    label='Skew Digits',
                    checked=True,
                    mb="sm"
                ),
            ]))
        ])
], fluid=True)

@callback(
    Output('my-display-docs', 'value'),
    Output('my-display-docs', 'count'),
    Output('my-display-docs', 'height'),
    Output('my-display-docs', 'color'),
    Output('my-display-docs', 'backgroundColor'),
    Output('my-display-docs', 'skew'),
    # Also update the hex display value for demo purposes
    Output('my-display-hex-docs', 'value'),
    Input('display-value-input-docs', 'value'),
    Input('display-count-slider-docs', 'value'),
    Input('display-height-slider-docs', 'value'),
    Input('display-color-dropdown-docs', 'value'),
    Input('display-bgcolor-dropdown-docs', 'value'),
    Input('display-skew-checklist-docs', 'checked')
)
def update_display_output_docs(val_input, count, height, color, bgcolor, skew_checked):
    final_bgcolor = bgcolor if bgcolor else None
    # For demo, show input value in both displays if possible, otherwise default hex
    hex_val = val_input if len(val_input) <= 4 else "DEMO"

    return val_input, count, height, color, final_bgcolor, skew_checked, hex_val