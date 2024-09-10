from dash import *
import dash_mantine_components as dmc
from dash_pannellum import DashPannellum


component = dmc.SimpleGrid(
    cols={"base": 1, "sm": 1, "lg": 4},
    children=[
        dmc.Paper(dmc.Stack([
            html.Div(id="view-pannellum"),
            html.Label(id="pannellum-output"),
            ]),
            id="intro-wrapper-dem",
            style={"gridColumn": "1 / 4"},
        ),
        dmc.Stack(
            [
                dmc.TextInput(
                    id='pannellum-panorama-url',
                    value='https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Panoramica_di_piazza_Garibaldi_-_Palagonia.jpg/1600px-Panoramica_di_piazza_Garibaldi_-_Palagonia.jpg',
                    label='Panorama URL',
                    placeholder='Enter URL',
                ),
                dmc.Select(
                        label="Select Panorama Type",
                        placeholder="Select one",
                        id="panorama-type",
                        value="equirectangular",
                        data=[
                            {"value": "equirectangular", "label": "Equirectangular"},
                            {"value": "tour", "label": "Tour"},
                            {"value": "multires", "label": "MultiRes"},
                            {"value": "video", "label": "Video"},
                        ],
                    ),
                dmc.NumberInput(
                            id='pannellum-haov', label="haov prop", hideControls=True, mb=10, value=360, min=0, max=360,
                        ),
                dmc.NumberInput(
                            id='pannellum-vaov', label="vaov prop", hideControls=True, mb=10, value=180, min=0, max=180,
                        ),
                dmc.NumberInput(
                            id='pannellum-vOffset', label="vOffset prop", hideControls=True, mb=10, value=1, min=-90, max=90,
                        ),
                    # dynamicWidth
                # dmc.Checkbox(
                #     id="pannellum-custom-controls", label="customControls", checked=False, mb=10
                # ),
                dmc.Checkbox(
                    id="pannellum-show-center-dot", label="showCenterDot", checked=True, mb=10
                ),
                dmc.Checkbox(
                    id="pannellum-autoload", label="autoLoad", checked=False, mb=10
                ),

            ],
            style={'overflow-y': 'auto', 'max-height': '500px'},
        ),
        dcc.Interval(id='interval-component', interval=100, n_intervals=0)
    ],
    spacing="2rem",
)

@callback(
    Output("view-pannellum", "children"),
    Input("pannellum-panorama-url", "value"),
    Input("panorama-type", "value"),
    Input("pannellum-haov", "value"),
    Input("pannellum-vaov", "value"),
    Input("pannellum-vOffset", "value"),
    # Input("pannellum-custom-controls", "checked"),
    Input("pannellum-show-center-dot", "checked"),
    Input("pannellum-autoload", "checked"),
)
def update_pannellum_output(url, panorama_type, haov, vaov, vOffset, showCenterDot, autoload):
    print('selected props')
    print(url, panorama_type, haov, vaov, vOffset, showCenterDot, autoload)
    if not url:
        return html.Div("No URL provided")
    elif panorama_type == "equirectangular":
        config = {
            "type": "equirectangular",
            "panorama": f"{url}",
            "haov": float(haov),
            "vaov": float(vaov),
            "vOffset": float(vOffset),
        }

        return DashPannellum(
            id=f"pannellum-example",
            tour={"default": {"firstScene": "scene1"}, "scenes": {"scene1": config}},
            showCenterDot=showCenterDot,
            autoLoad=autoload,
        )
    elif panorama_type == 'tour':
        tour_config = {
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
                    "panorama": f"{url}",
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
        }

        return DashPannellum(
            id='pannellum-example',
            tour=tour_config,
            showCenterDot=showCenterDot,
            width='100%',
            height='400px',
            autoLoad=autoload
        )
    elif panorama_type == 'multires':
        multiRes_config = {
            "basePath": "https://pannellum.org/images/multires/library",
            "path": "/%l/%s%y_%x",
            "fallbackPath": "/fallback/%s",
            "extension": "jpg",
            "tileResolution": 512,
            "maxLevel": 6,
            "cubeResolution": 8432,
        }

        return DashPannellum(
            id='pannellum-example',
            multiRes=multiRes_config,
            showCenterDot=showCenterDot,
            width='100%',
            height='400px',
            autoLoad=autoload
        )
    elif panorama_type == 'video':
        video_config = {
            "sources": [
                {"src": "https://bitmovin-a.akamaihd.net/content/playhouse-vr/progressive.mp4", "type": "video/mp4"},
            ],
            "poster": "https://bitmovin-a.akamaihd.net/content/playhouse-vr/poster.jpg"
        }

        return DashPannellum(
            id='pannellum-example',
            video=video_config,
            showCenterDot=showCenterDot,
            width='100%',
            height='400px',
            autoLoad=autoload
        )
    return html.Div("Something went wrong")


@callback(
    Output('pannellum-output', 'children'),
    Input('pannellum-example', 'pitch'),
    Input('pannellum-example', 'yaw'),
    Input('interval-component', 'n_intervals')
)
def update_video_output(pitch, yaw, n):
    if pitch is not None and yaw is not None:
        return f'Camera Position - Pitch: {pitch:.2f}, Yaw: {yaw:.2f}'
    return 'Camera Position - Pitch: 0.00, Yaw: 0.00'