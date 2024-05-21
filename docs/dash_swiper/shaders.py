import dash_swiper
from dash import *
import dash_mantine_components as dmc

component = dmc.SimpleGrid(
    [
        dmc.Paper(
            html.Div(id="view-swiper-shader-output"),
            id="intro-wrapper-swiper-shader",
            style={"gridColumn": "1 / 4"},
        ),
        dmc.Stack(
            [
                dmc.Select(
                    label="Shaders",
                    placeholder="Select one",
                    id="swiper-select-shader",
                    value="random",
                    data=[
                        {"value": "random", "label": "random"},
                        {"value": "dots", "label": "dots"},
                        {"value": "flyeye", "label": "flyeye"},
                        {"value": "morph-x", "label": "morph-x"},
                        {"value": "morph-y", "label": "morph-y"},
                        {"value": "page-curl", "label": "page-curl"},
                        {"value": "peel-x", "label": "peel-x"},
                        {"value": "peel-y", "label": "peel-y"},
                        {"value": "polygons-fall", "label": "polygons-fall"},
                        {"value": "polygons-morph", "label": "polygons-morph"},
                        {"value": "polygons-wind", "label": "polygons-wind"},
                        {"value": "pixelize", "label": "pixelize"},
                        {"value": "ripple", "label": "ripple"},
                        {"value": "shutters", "label": "shutters"},
                        {"value": "slices", "label": "slices"},
                        {"value": "squares", "label": "squares"},
                        {"value": "stretch", "label": "stretch"},
                        {"value": "wave-x", "label": "wave-x"},
                        {"value": "wind", "label": "wind"},
                    ],
                ),
            ],
        ),
    ],
    cols={"base": 1, "sm": 1, "lg": 4},
    spacing="2rem",
)

@callback(
    Output("view-swiper-shader-output", "children"),
    Input("swiper-select-shader", "value"),
)
def update_swiper_shader(value):
    shader = dash_swiper.DashSwiper(
            id=f"my-swiper-shaded-{value}",
            className="swiper-slide",
            swiperOptions={
                "direction": "horizontal",
                "loop": True,
                "pauseOnMouseEnter": True,
                "autoplay": False,  # Add this line to turn off autoplay
                "waitForTransition": True,
                # Add more Swiper options here
            },
            # speed=0,
            # loop=True,
            slides=[
                {
                    "src": get_asset_url("images/01.jpg"),
                    "alt": "Image 1",
                    "title": "Spider-Man: No Way Home",
                    "link": "https://www.example1.com",
                },
                {
                    "src": get_asset_url("images/02.jpg"),
                    "alt": "Image 2",
                    "title": "Free Guy",
                    "link": "https://www.example2.com",
                },
                {
                    "src": get_asset_url("images/03.jpg"),
                    "alt": "Image 3",
                    "title": "The Nice Guys",
                    "link": "https://www.example3.com",
                },
                {
                    "src": get_asset_url("images/04.jpg"),
                    "alt": "Image 4",
                    "title": "Cage",
                    "link": "https://www.example4.com",
                },
                {
                    "src": get_asset_url("images/05.jpg"),
                    "alt": "Image 5",
                    "title": "avatar",
                    "link": "https://www.example5.com",
                },
            ],
            shader=f'{value}',  # Add the shader effect here
        )

    return html.Div(shader, style={"width": "100%", "height": "50vh"})