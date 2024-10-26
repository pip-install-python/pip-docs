import dash_swiper
from dash import *
import dash_mantine_components as dmc

component = dmc.SimpleGrid(
    [
        dmc.Paper(
            html.Div(id="view-carousel-basic-output"),
            id="intro-wrapper-carousel-basic",
            style={"gridColumn": "1 / 4"},
        ),
        dmc.Stack(
            [
                dmc.NumberInput(
                    id="slides-per-view",
                    label="Slides Per View",
                    value=2,
                    min=1,
                    max=5,
                    step=1,
                ),
                dmc.NumberInput(
                    id="side-slides",
                    label="Side Slides",
                    value=2,
                    min=1,
                    max=4,
                    step=1,
                ),
                dmc.Checkbox(
                    id="carousel-navigation",
                    label="Show Navigation",
                    checked=True,
                ),
                dmc.Checkbox(
                    id="carousel-pagination",
                    label="Show Pagination",
                    checked=True,
                ),
                dmc.Checkbox(
                    id="carousel-autoplay",
                    label="Enable Autoplay",
                    checked=False,
                ),
            ],
        ),
    ],
    cols={"base": 1, "sm": 1, "lg": 4},
    spacing="2rem",
)


@callback(
    Output("view-carousel-basic-output", "children"),
    Input("slides-per-view", "value"),
    Input("side-slides", "value"),
    Input("carousel-navigation", "checked"),
    Input("carousel-pagination", "checked"),
    Input("carousel-autoplay", "checked"),
)
def update_carousel_basic(slides_per_view, side_slides, show_nav, show_pagination, enable_autoplay):
    carousel = dash_swiper.DashCarousel(
        id="basic-carousel-demo",
        className="custom-carousel",
        slides=[
            {
                "src": get_asset_url("images/01.jpg"),
                "alt": "Nature 1",
                "title": "Mountain Lake",
                "description": "Serene mountain lake at sunset.",
            },
            {
                "src": get_asset_url("images/02.jpg"),
                "alt": "Nature 2",
                "title": "Forest Path",
                "description": "A winding path through ancient trees.",
            },
            {
                "src": get_asset_url("images/03.jpg"),
                "alt": "Nature 3",
                "title": "Desert Dunes",
                "description": "Rolling sand dunes at dawn.",
            },
            {
                "src": get_asset_url("images/04.jpg"),
                "alt": "Nature 4",
                "title": "Ocean Waves",
                "description": "Powerful waves crash on rocky shores.",
            },
            {
                "src": get_asset_url("images/05.jpg"),
                "alt": "Nature 5",
                "title": "Alpine Meadow",
                "description": "Wildflowers bloom in mountain meadows.",
            },
        ],
        carouselEffect={
            "opacityStep": 0.33,
            "scaleStep": 0.2,
            "sideSlides": side_slides,
        },
        autoplayEnabled=enable_autoplay,
        autoplay={
            "delay": 3000,
            "disableOnInteraction": True,
        },
        loop=True,
        grabCursor=True,
        navigation=show_nav,
        pagination=show_pagination,
        slidesPerView=slides_per_view,
        style={"width": "100%", "height": "300px"},
    )

    return carousel