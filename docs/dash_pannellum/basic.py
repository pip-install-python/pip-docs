from dash import html
import dash_pannellum

component = html.Div([
    dash_pannellum.DashPannellum(
        id='panorama',
        tour={
            "default": {
                "firstScene": "scene1",
                "sceneFadeDuration": 1000
            },
            "scenes": {
                "scene1": {
                    "title": "Example Panorama",
                    "hfov": 110,
                    "pitch": -3,
                    "yaw": 117,
                    "type": "equirectangular",
                    "panorama": "/assets/images/landscape.jpg"
                }
            }
        },
        autoLoad=True,
        width='100%',
        height='400px',
    )
])
