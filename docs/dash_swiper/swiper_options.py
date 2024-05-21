import dash_swiper
from dash import *
import dash_mantine_components as dmc

# id: PropTypes.string,
# loop: PropTypes.bool,
# shader: PropTypes.arrayOf(PropTypes.string),
# speed: PropTypes.number,
# autoplay: PropTypes.shape({
#         delay: PropTypes.number,
#         disableOnInteraction: PropTypes.bool,
#     }),
# slides: PropTypes.arrayOf(
#     PropTypes.shape({
#         src: PropTypes.string.isRequired,
#         alt: PropTypes.string,
#         title: PropTypes.string,
#         link: PropTypes.string
#     })
# ),
# className: PropTypes.string,
# navigation: PropTypes.shape({
#     prevEl: PropTypes.string,
#     nextEl: PropTypes.string,
# }),
# pagination: PropTypes.shape({
#     el: PropTypes.string,
#     clickable: PropTypes.bool,
# }),
# nextButton: PropTypes.bool,
# prevButton: PropTypes.bool,
# swiperOptions: PropTypes.object,

component = dmc.SimpleGrid(
    [
        dmc.Paper(
            html.Div(id="view-swiper-options-output"),
            id="intro-wrapper-swiper-shader",
            style={"gridColumn": "1 / 4"},
        ),
        dmc.Stack(
            [
                html.Label('swiperOptions'),
                dmc.Select(
                    label="direction",
                    placeholder="Select one",
                    id="swiper-select-direction",
                    value="horizontal",
                    data=[
                        {"value": "horizontal", "label": "horizontal"},
                        {"value": "vertical", "label": "vertical"},
                    ],
                ),
                dmc.Checkbox(id='swiper-check-loop', label='loop', checked=True),
                dmc.Checkbox(id='swiper-pause-on-mouse-enter', label='pauseOnMouseEnter', checked=True),
                dmc.Checkbox(id='swiper-autoplay', label='autoplay', checked=False),
                dmc.Checkbox(id='swiper-wait-for-transition', label='waitForTransition', checked=True),
                dmc.NumberInput(id='speed', label='Speed', value=300),

            ],
        ),
    ],
    cols={"base": 1, "sm": 1, "lg": 4},
    spacing="2rem",
)

@callback(
    Output("view-swiper-options-output", "children"),
    Input("swiper-select-direction", "value"),
    Input("swiper-check-loop", "checked"),
    Input("swiper-pause-on-mouse-enter", "checked"),
    Input("swiper-autoplay", "checked"),
    Input("swiper-wait-for-transition", "checked"),
    Input("speed", "value"),
)
def update_swiper_options(direction, loop, pause_on_mouse_enter, autoplay, wait_for_transition, speed):
    shader = dash_swiper.DashSwiper(
            id=f"my-swiper-shaded-{direction}-{loop}-{pause_on_mouse_enter}-{autoplay}-{wait_for_transition}-{speed}",
            className="swiper-slide",
            swiperOptions={
                "direction": direction,
                "pauseOnMouseEnter": pause_on_mouse_enter,
                "autoplay": autoplay,  # Add this line to turn off autoplay
                "waitForTransition": wait_for_transition,
                # Add more Swiper options here
            },
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
            speed=speed,
            loop=loop,
            shader='random',  # Add the shader effect here
        )

    return html.Div(shader, style={"width": "100%", "height": "50vh"})