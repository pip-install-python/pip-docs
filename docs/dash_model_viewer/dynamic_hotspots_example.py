# --- START OF FILE dynamic_hotspots_example.py ---

import dash
# ****** Add ClientsideFunction to imports ******
from dash import html, dcc, callback, Input, Output, State, no_update, clientside_callback, ClientsideFunction
import dash_mantine_components as dmc
from model_viewer import ModelViewer
import time

# ****** Ensure this path is correct for your docs setup ******
# If your assets are in assets/model_viewer/, use get_asset_url
# from dash import get_asset_url
# ASTRONAUT_SRC = get_asset_url("model_viewer/Astronaut.glb")
# Otherwise, use the direct URL if served externally
ASTRONAUT_SRC = "https://modelviewer.dev/shared-assets/models/Astronaut.glb"


component = dmc.Paper(
    p="md", shadow="sm", withBorder=True,
    children=[
        # Stores to manage state and data between client and server
        dcc.Store(id='dyn-hotspot-store', data=[]),
        dcc.Store(id='dyn-mode-store', data='viewing'), # 'viewing' or 'adding'
        dcc.Store(id='dyn-new-hotspot-data-store', data=None), # Used by JS to send data

        # Controls
        dmc.Group(
            [
                dmc.Button("Set Hotspot", id="dyn-set-place-button"),
                dmc.Button("Cancel", id="dyn-cancel-button", variant="outline", style={'display': 'none'}),
                dmc.TextInput(
                    id="dyn-label-input",
                    placeholder="Enter hotspot label...",
                    style={'display': 'none', 'flexGrow': 1},
                    value="", # Set initial value
                ),
            ],
            mb="md"
        ),

        # Viewer Container
        html.Div(
            id="dyn-viewer-container",
            style={'position': 'relative', 'height': '450px', 'width': '100%', 'border': '1px dashed #ccc'},
            children=[
                ModelViewer(
                    id="dynamic-hotspots-viewer",
                    src=ASTRONAUT_SRC,
                    alt="Astronaut for adding hotspots",
                    cameraControls=True,
                    ar=True, # Ensure model-viewer includes necessary JS for positionAndNormalFromPoint
                    style={"height": "100%", "width": "100%", "position": 'absolute', 'top': 0, 'left': 0},
                    hotspots=[] # Start empty, updated by callback
                ),
                # Visual reticle - centered overlay, shown only in 'adding' mode
                html.Div(
                    id="dyn-reticle",
                    style={
                        'position': 'absolute', 'top': '50%', 'left': '50%',
                        'transform': 'translate(-50%, -50%)',
                        'width': '30px', 'height': '30px',
                        'border': '2px solid red', 'borderRadius': '50%',
                        'pointerEvents': 'none', 'display': 'none' # Controlled by callback
                    }
                )
            ]
        ),
        dmc.Text(
            "Click 'Set Hotspot', type label, aim reticle, click 'Place Hotspot'. Requires client-side JS.",
            size="xs", c="dimmed", ta="center", mt="sm"
        ),
        # ****** Add note about CSS ******
        dmc.Text(
            "Requires CSS for '.hotspot-dynamic' styling in assets folder.",
            size="xs", c="dimmed", ta="center", mt="xs"
        )
    ]
)


# --- Callbacks ---

# Callback 1: Toggle Add/Viewing Mode State (Handles UI Changes)
@callback(
    Output('dyn-mode-store', 'data'),
    Output('dyn-label-input', 'style'),
    Output('dyn-set-place-button', 'children'),
    Output('dyn-cancel-button', 'style'),
    Output('dyn-reticle', 'style'),
    Input('dyn-set-place-button', 'n_clicks'),
    Input('dyn-cancel-button', 'n_clicks'),
    State('dyn-mode-store', 'data'),
    prevent_initial_call=True
)
def toggle_add_mode(set_clicks, cancel_clicks, current_mode):
    button_id = dash.callback_context.triggered_id
    reticle_style = { # Base style, display controlled below
        'position': 'absolute', 'top': '50%', 'left': '50%',
        'transform': 'translate(-50%, -50%)', 'width': '30px', 'height': '30px',
        'border': '2px solid red', 'borderRadius': '50%', 'pointerEvents': 'none'
    }

    # --- Entering Add Mode ---
    if button_id == 'dyn-set-place-button' and current_mode == 'viewing':
        print("Entering Add Mode") # Debug
        reticle_style['display'] = 'block'
        return 'adding', {'display': 'inline-block', 'flexGrow': 1}, "Place Hotspot", {'display': 'inline-block'}, reticle_style

    # --- Exiting Add Mode (via Cancel or JS completion) ---
    # If 'Place Hotspot' is clicked while in 'adding' mode, this callback does nothing.
    # The clientside callback handles the action. Callback 2 handles resetting the UI AFTER data is received.
    elif button_id == 'dyn-cancel-button':
         print("Exiting Add Mode via Cancel") # Debug
         reticle_style['display'] = 'none'
         return 'viewing', {'display': 'none', 'flexGrow': 1}, "Set Hotspot", {'display': 'none'}, reticle_style
    elif button_id == 'dyn-set-place-button' and current_mode == 'adding':
         # This case is handled by the clientside callback below.
         # The server-side callback should do nothing here.
         print("Place Hotspot clicked - Clientside callback should handle this.") # Debug
         return no_update # Explicitly do nothing

    # Default case (shouldn't normally be reached for these inputs)
    return no_update


# ****** START: ADDED CLIENTSIDE CALLBACK ******
# Callback 1.5: Trigger JS to get hotspot data when "Place Hotspot" is clicked
clientside_callback(
    ClientsideFunction(
        namespace='modelViewer', # Namespace in your JS file
        function_name='handleAddHotspotClick' # Function name in your JS file
    ),
    Output('dyn-new-hotspot-data-store', 'data'), # JS function returns data here
    Input('dyn-set-place-button', 'n_clicks'), # Triggered by this button
    State('dynamic-hotspots-viewer', 'id'), # Pass viewer ID to JS
    State('dyn-mode-store', 'data'), # Pass current mode to JS
    State('dyn-label-input', 'value'), # Pass label text to JS
    prevent_initial_call=True
)
# ****** END: ADDED CLIENTSIDE CALLBACK ******


# Callback 2: Process New Hotspot Data (received from Client-Side via Store)
@callback(
    # Outputs to update the main hotspot list and reset the UI
    Output('dyn-hotspot-store', 'data', allow_duplicate=True),
    Output('dyn-mode-store', 'data', allow_duplicate=True),    # Reset mode back to viewing
    Output('dyn-label-input', 'value', allow_duplicate=True), # Clear input
    Output('dyn-label-input', 'style', allow_duplicate=True), # Hide input
    Output('dyn-set-place-button', 'children', allow_duplicate=True), # Reset button text
    Output('dyn-cancel-button', 'style', allow_duplicate=True),    # Hide Cancel button
    Output('dyn-reticle', 'style', allow_duplicate=True),            # Hide reticle
    # Triggered ONLY when the clientside callback updates this store
    Input('dyn-new-hotspot-data-store', 'data'),
    # State needed to update the list
    State('dyn-hotspot-store', 'data'),                      # Get current list
    prevent_initial_call=True
)
def add_new_hotspot(new_hotspot_data, current_hotspots):
    # Check if the trigger was just the initial None value or invalid data
    if new_hotspot_data is None or not isinstance(new_hotspot_data, dict):
        print(f"Dynamic Hotspots: Invalid or no new hotspot data received: {new_hotspot_data}")
        # Don't reset the UI if data is invalid, just don't add the hotspot
        # UI reset should only happen on SUCCESSFUL addition or explicit CANCEL.
        # However, if this callback IS triggered by bad data from JS somehow,
        # maybe we *should* reset? Let's keep the reset for now.
        reticle_style = { # Base style, display controlled below
            'position': 'absolute', 'top': '50%', 'left': '50%',
            'transform': 'translate(-50%, -50%)', 'width': '30px', 'height': '30px',
            'border': '2px solid red', 'borderRadius': '50%', 'pointerEvents': 'none', 'display':'none'
        }
        # Return no_update for hotspot list, but still reset UI
        return no_update, 'viewing', "", {'display': 'none', 'flexGrow': 1}, "Set Hotspot", {'display': 'none'}, reticle_style

    print(f"Dynamic Hotspots (Server): Received new hotspot data: {new_hotspot_data}")

    # Add the new hotspot to the list
    if not isinstance(current_hotspots, list):
         current_hotspots = [] # Initialize if store is empty/invalid

    # Add a default class if needed for styling new hotspots
    # Ensure the keys from JS match what ModelViewer expects
    validated_hotspot = {
        "slot": new_hotspot_data.get("slot", f"hs-err-{time.time()}"),
        "position": new_hotspot_data.get("position", "0 0 0"),
        "normal": new_hotspot_data.get("normal"), # Optional
        "text": new_hotspot_data.get("text", ""),
        "children_classname": new_hotspot_data.get('children_classname', 'hotspot-dynamic')
    }
    current_hotspots.append(validated_hotspot)
    print(f"Dynamic Hotspots (Server): Updated list: {current_hotspots}")


    # Reset UI elements back to viewing state AFTER successful add
    reticle_style = { # Base style, display controlled below
        'position': 'absolute', 'top': '50%', 'left': '50%',
        'transform': 'translate(-50%, -50%)', 'width': '30px', 'height': '30px',
        'border': '2px solid red', 'borderRadius': '50%', 'pointerEvents': 'none', 'display':'none'
    }
    return current_hotspots, 'viewing', "", {'display': 'none', 'flexGrow': 1}, "Set Hotspot", {'display': 'none'}, reticle_style


# Callback 3: Update ModelViewer's 'hotspots' prop when the store changes
@callback(
    Output('dynamic-hotspots-viewer', 'hotspots'),
    Input('dyn-hotspot-store', 'data') # Triggered by Callback 2 updating the store
)
def update_viewer_hotspots_list(hotspot_list):
    print(f"Dynamic Hotspots (Server): Updating viewer component with hotspots: {hotspot_list}")
    # Ensure it's always a list, even if store somehow becomes None
    return hotspot_list if isinstance(hotspot_list, list) else []


# --- END OF FILE dynamic_hotspots_example.py ---