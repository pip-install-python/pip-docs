import dash_mantine_components as dmc
from dash import html
from model_viewer import ModelViewer

# Use local assets assuming they are served by the main docs app
CHAIR_SRC = "assets/model_viewer/Froggy_rocking_chair.glb"
CHAIR_POSTER = "assets/model_viewer/frog_rocking_chair.png"
HAND_ICON = "assets/model_viewer/hand.png" # Default hand icon, assuming it's available

component = dmc.Paper(
    p="md", shadow="sm", withBorder=True,
    children=[
         dmc.Text("AR features require a supported mobile device.", size="sm", ta="center", mb="xs"),
        ModelViewer(
            id="ar-custom-viewer",
            src=CHAIR_SRC,
            poster=CHAIR_POSTER,
            alt="A 3D model of a rocking chair",
            ar=True,
            arModes="webxr scene-viewer quick-look",
            cameraControls=True,
            shadowIntensity=1.0,
            style={"height": "450px", "width": "100%"},
            # Customizations
            arButtonText="Place Chair in Room",
            customArPrompt=dmc.Stack( # Example using Dash Mantine components
                [
                    dmc.Loader(size="sm"),
                    dmc.Text("Scanning your space...", size="sm", c="dimmed")
                ],
                align="center"
            ),
            customArFailure=dmc.Alert(
                "AR failed to start. Ensure your browser supports WebXR and has camera permissions.",
                title="AR Error!", color="red", withCloseButton=True
            ),
        )
    ]
)