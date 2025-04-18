import dash_mantine_components as dmc
from model_viewer import ModelViewer

ASTRONAUT_SRC = "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
ASTRONAUT_POSTER = "https://modelviewer.dev/assets/poster-astronaut.webp"

astronaut_hotspots = [
    {
        "slot": "anno-hotspot-visor",      # Unique slot name for this example
        "position": "0 1.75 0.35",
        "normal": "0 0 1",
        "text": "Visor"
    },
    {
        "slot": "anno-hotspot-hand",
        "position": "-0.54 0.93 0.1",
        "normal": "-0.73 0.05 0.69",
        "text": "Left Hand"
    },
    {
        "slot": "anno-hotspot-foot",
        "position": "0.16 0.1 0.17",
        "normal": "-0.07 0.97 0.23",
        "text": "Foot"
    },
]

component = dmc.Paper(
    p="md", shadow="sm", withBorder=True,
    children=[
        dmc.Text("Hover or click hotspots.", size="sm", ta="center", mb="xs"),
        ModelViewer(
            id="annotations-viewer",
            src=ASTRONAUT_SRC,
            poster=ASTRONAUT_POSTER,
            alt="Astronaut with annotations",
            cameraControls=True,
            ar=True,
            arModes="webxr scene-viewer quick-look",
            toneMapping="neutral", # Changed from aces for potentially wider compatibility
            shadowIntensity=1,
            hotspots=astronaut_hotspots, # Pass the list of hotspots
            style={"width": "100%", "height": "450px"}
        ),
        dmc.Text("Styling requires CSS in assets folder (e.g., assets/model_viewer/model-viewer-styles.css)", size="xs", c="dimmed", ta="center", mt="xs")
    ]
)
# Example CSS for assets/model_viewer_styles.css:
# .hotspot {
#   background-color: rgba(0, 128, 255, 0.7);
#   border-radius: 100%;
#   border: 1px solid white;
#   width: 20px;
#   height: 20px;
#   box-sizing: border-box;
#   cursor: pointer;
#   transition: opacity 0.3s;
#   opacity: 0.8;
# }
# .hotspot:not([data-visible]) { /* Hide hotspot text initially */
#     background-color: transparent;
#     border: 3px solid rgba(0, 128, 255, 0.7);
#     color: transparent;
#     pointer-events: none;
#     width: 30px;
#     height: 30px;
# }
# .hotspot > * { /* Hide text inside hotspot */
#     opacity: 0;
#     transform: translateY(-50%);
# }
# .hotspot[data-visible] > * { /* Show text on hover/focus */
#     opacity: 1;
#     transform: translateY(0);
# }
# .hotspot[data-visible] { /* Style annotation box when visible */
#     background-color: rgba(0, 128, 255, 0.8);
#     border-radius: 4px;
#     color: white;
#     display: block;
#     font-size: 14px;
#     padding: 8px 12px;
#     position: absolute;
#     left: calc(100% + 1em);
#     top: 50%;
#     width: max-content;
#     max-width: 200px;
#     pointer-events: none; /* Allow clicking through annotation */
#     height: auto;
#     transition: opacity 0.3s 0.1s;
#     transform: translateY(-50%);
#     border: none;
# }
# .hotspot[slot="anno-hotspot-visor"] { --hotspot-color: red; } /* Example slot specific color */
# .hotspot[slot="anno-hotspot-visor"]::before { border-color: red; }