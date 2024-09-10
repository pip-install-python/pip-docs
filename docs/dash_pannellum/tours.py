from dash import html
import dash_pannellum

component = html.Div([
    dash_pannellum.DashPannellum(
        id='panorama',
        tour={
                "default": {
                    "firstScene": "circle",
                    "author": "Pip Install Python",
                    "sceneFadeDuration": 1000,
                },
                "scenes": {
                    "circle": {
                        "title": "Dash Pannellum",
                        "hfov": 110,
                        "pitch": -3,
                        "yaw": 117,
                        "type": "equirectangular",
                        "panorama": "https://pannellum.org/images/alma.jpg",
                        "hotSpots": [
                            {
                                "pitch": -2.1,
                                "yaw": 132.9,
                                "type": "scene",
                                "text": "Spring House or Dairy",
                                "sceneId": "house"
                            }
                        ]
                    },
                    "house": {
                        "title": "Spring House or Dairy",
                        "hfov": 110,
                        "yaw": 5,
                        "type": "equirectangular",
                        "panorama": "https://pannellum.org/images/bma-0.jpg",
                        "hotSpots": [
                            {
                                "pitch": -0.6,
                                "yaw": 37.1,
                                "type": "scene",
                                "text": "Mason Circle",
                                "sceneId": "circle",
                                "targetYaw": -23,
                                "targetPitch": 2
                            }
                        ]
                    }
                }
            },
        autoLoad=True,
        width='100%',
        height='400px',
    )
])
