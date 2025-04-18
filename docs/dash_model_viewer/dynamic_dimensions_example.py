# --- START OF FILE dynamic_dimensions_example.py ---

import dash
from dash import html, dcc, callback, Input, Output, State, get_asset_url, clientside_callback, ClientsideFunction
import dash_mantine_components as dmc
from model_viewer import ModelViewer

# Basic structure for hotspots - positions/text usually set by client-side JS
# Keep children_classname for CSS targeting if needed (.dot, .dim)
dimension_hotspots_structure = [
    # Dots for line endpoints
    {"slot": "hotspot-dot+X-Y+Z", "normal": "1 0 0", "text": "", "children_classname": "dot"},
    {"slot": "hotspot-dot+X-Y-Z", "normal": "1 0 0", "text": "", "children_classname": "dot"},
    {"slot": "hotspot-dot+X+Y-Z", "normal": "0 1 0", "text": "", "children_classname": "dot"},
    {"slot": "hotspot-dot-X+Y-Z", "normal": "0 1 0", "text": "", "children_classname": "dot"},
    {"slot": "hotspot-dot-X-Y-Z", "normal": "-1 0 0", "text": "", "children_classname": "dot"},
    {"slot": "hotspot-dot-X-Y+Z", "normal": "-1 0 0", "text": "", "children_classname": "dot"},
    # Hotspots to display dimension text
    {"slot": "hotspot-dim+X-Y", "normal": "1 0 0", "text": "", "children_classname": "dim"}, # e.g., Length Z
    {"slot": "hotspot-dim+X-Z", "normal": "1 0 0", "text": "", "children_classname": "dim"}, # e.g., Height Y
    {"slot": "hotspot-dim+Y-Z", "normal": "0 1 0", "text": "", "children_classname": "dim"}, # e.g., Width X (Top) - Might be unused by JS line drawing
    {"slot": "hotspot-dim-X-Z", "normal": "-1 0 0", "text": "", "children_classname": "dim"}, # e.g., Height Y
    {"slot": "hotspot-dim-X-Y", "normal": "-1 0 0", "text": "", "children_classname": "dim"}, # e.g., Length Z
]

# Ensure this path is correct relative to where assets are served in your docs app
CHAIR_SRC = get_asset_url("model_viewer/Froggy_rocking_chair.glb")

# Define unit options consistent with JS
unit_options = [
    {"label": "cm", "value": "cm"},
    {"label": "mm", "value": "mm"},
    {"label": "m", "value": "m"},
    {"label": "in", "value": "in"},
    {"label": "ft", "value": "ft"},
]

component = dmc.Paper(
    p="md", shadow="sm", withBorder=True,
    children=[
        dmc.Group( # Group controls for better layout
            [
                dmc.Checkbox(
                    id="dims-show-checkbox",
                    label="Show Dimensions",
                    checked=True, # Start checked
                ),
                dmc.RadioGroup(
                    id='dims-unit-select',
                    label="Units",
                    children=dmc.Group([dmc.Radio(label=opt['label'], value=opt['value']) for opt in unit_options]),
                    value='cm', # Default value
                    size="sm",
                    mt="xs" # Add some margin top if Checkbox is above
                ),
            ],
            mb="md", # Margin bottom for the group
            align="flex-end" # Align items nicely
        ),

        html.Div( # Container for relative positioning (needed for SVG overlay)
            id="dims-model-container",
            style={'position': 'relative', 'height': '450px', 'width': '100%', 'border': '1px dashed #ccc'},
            children=[
                ModelViewer(
                    id="dimension-demo-dynamic",
                    src=CHAIR_SRC, alt="Chair for dimensions",
                    cameraControls=True, cameraOrbit="-30deg auto auto",
                    ar=True, shadowIntensity=1,
                    # Hotspots are controlled by the callback below
                    hotspots=dimension_hotspots_structure, # Initial state based on checkbox
                    style={"height": "100%", "width": "100%", "position": 'absolute', 'top': 0, 'left': 0}
                ),
                # SVG overlay for lines will be added here by client-side JS
            ]
        ),
        dmc.Text(
            "Dimension calculation, positioning, text update, and line drawing require client-side JS.",
            size="xs", c="dimmed", ta="center", mt="sm"
        ),
        dmc.Text(
            "Hotspot *presence* is controlled server-side. Styling requires CSS.",
            size="xs", c="dimmed", ta="center", mt="xs"
        )
    ]
)

# Callback controls ONLY the presence of the hotspots passed to the component.
# The actual positioning, text update, and line drawing require client-side JS.
@callback(
    Output("dimension-demo-dynamic", "hotspots"),
    Input("dims-show-checkbox", "checked"),
)
def control_hotspot_visibility(is_checked):
    if is_checked:
        # print("Server: Sending hotspot structure") # Debug
        return dimension_hotspots_structure # Send structure to component/JS
    else:
        # print("Server: Sending empty hotspot list") # Debug
        return [] # Send empty list to hide


# UPDATED Client-side Callback
# Triggers the JS function to perform calculations, updates, and SVG drawing.
clientside_callback(
    ClientsideFunction(
        namespace='modelViewer',       # Namespace defined in model_viewer_clientside.js
        function_name='updateDimensions' # Function name defined in model_viewer_clientside.js
    ),
    Output("dimension-demo-dynamic", "alt"), # Dummy output, needed for any clientside callback
    # --- Inputs that trigger the JS ---
    Input("dimension-demo-dynamic", "src"),   # Trigger on model change
    Input("dims-show-checkbox", "checked"),   # Trigger on checkbox change (passes boolean)
    Input("dims-unit-select", "value"),       # Trigger on unit change (passes string like 'cm')
    Input("dimension-demo-dynamic", "hotspots"), # *** CRUCIAL: Trigger AFTER Python updates hotspots ***
    # --- States needed by the JS function ---
    State("dimension-demo-dynamic", "id"),    # Pass the ID of the ModelViewer component
    State("dims-model-container", "id"),      # Pass the ID of the container DIV
    prevent_initial_call=False # Allow to run on page load
)

# --- END OF FILE dynamic_dimensions_example.py ---


