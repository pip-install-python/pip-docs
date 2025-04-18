import dash_mantine_components as dmc
from model_viewer import ModelViewer

# Assume assets folder is configured by the main docs app
ASTRONAUT_SRC = "https://modelviewer.dev/shared-assets/models/Astronaut.glb"

component = dmc.Paper(
    p="md", shadow="sm", withBorder=True,
    children=[
        ModelViewer(
            id="3d-model",
            src="https://modelviewer.dev/shared-assets/models/Astronaut.glb",
            alt="A 3D model of an astronaut",
            cameraControls=True,
            touchAction="pan-y",
            ar=True,
            poster="https://modelviewer.dev/shared-assets/models/Astronaut.webp",
            style={"height": "1000px", "width": "100%"},
            arButtonText="View in AR"
        ),
    ]
)