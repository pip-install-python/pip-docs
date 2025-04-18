import dash
from dash import html, callback, Input, Output, get_asset_url
import dash_mantine_components as dmc
from model_viewer import ModelViewer

MODELS = {
    "Shoe": get_asset_url("model_viewer/MaterialsVariantsShoe.glb"),
    "Woman": get_asset_url("model_viewer/kara_-_detroit_become_human.glb"),
    "Horse": "https://modelviewer.dev/shared-assets/models/Horse.glb" # Added another option
}

component = dmc.Paper(
    p="md", shadow="sm", withBorder=True,
    children=[
        dmc.SegmentedControl(
            id="dyn-switch-model-select",
            data=list(MODELS.keys()),
            value="Astronaut",
            fullWidth=True,
            mb="md",
        ),
        ModelViewer(
            id="dynamic-switch-viewer",
            src=MODELS["Shoe"], # Initial model
            alt="A 3D model",
            cameraControls=True,
            ar=True,
            style={"height": "450px", "width": "100%"},
        )
    ]
)

@callback(
    Output('dynamic-switch-viewer', 'src'),
    Input('dyn-switch-model-select', 'value')
)
def update_dynamic_model(selected_model_name):
    return MODELS.get(selected_model_name, MODELS["Shoe"])