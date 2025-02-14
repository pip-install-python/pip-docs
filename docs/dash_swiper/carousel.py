from dash_swiper import DashCarousel
from dash import *
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
from dash_iconify import DashIconify

demo_py = """
import dash
from dash import *
import dash_mantine_components as dmc

app = dash.Dash(__name__, external_stylesheets=dmc.styles.ALL)


 app.layout = dmc.MantineProvider([dmc.Stack(
    [
html.Div([  # Wrapper div for the carousel
        DashCarousel(
            id="my-carousel",
            className="custom-carousel",
            slides=[
            {
                "src": get_asset_url("images/01.jpg"),
                "alt": "Spider Man",
                "title": "Spider-Man: No Way Home",
                "description": "A thrilling superhero adventure.",
            },
            {
                "src": get_asset_url("images/02.jpg"),
                "alt": "Free Guy",
                "title": "Free Guy",
                "description": "A comedy about a video game NPC.",
            },
            {
                "src": get_asset_url("images/03.jpg"),
                "alt": "Nice Guys Finish Last",
                "title": "The Nice Guys",
                "description": "A neo-noir comedy thriller.",
            },
            {
                "src": get_asset_url("images/04.jpg"),
                "alt": "Cage",
                "title": "Cage",
                "description": "An intense action-packed movie.",
            },
            {
                "src": get_asset_url("images/05.jpg"),
                "alt": "Avatar",
                "title": "Avatar",
                "description": "An epic science fiction adventure.",
            },
        ],
            carouselEffect={
                "opacityStep": 0.33,
                "scaleStep": 0.2,
                "sideSlides": 1,
            },
            autoplayEnabled=False,
            autoplay={
                "delay": 3000,
                "disableOnInteraction": True,
            },
            loop=True,
            grabCursor=True,
            navigation=False,
            pagination=False,
            slidesPerView=5,
            style={"width": "100%", "height": "100%"},  # Set to 100% to fill the wrapper
        )
    ], style={"width": "100%", "height": "100px", "margin": "0 auto"}),
        html.Div(id='current-slide-display', style={"color": "white", "marginTop": "20px"}),
        
])

@callback(
    Output("current-slide-display", "children"),
    Input("my-carousel", "activeSlideAlt")
)
def display_active_slide(active_slide_alt):
    if active_slide_alt is None:
        raise PreventUpdate
    return f"Current Slide: {active_slide_alt}"

if __name__ == '__main__':
    app.run_server(debug=True, port='8050')
"""

code = [
    {
        "fileName": "carousel_example.py",
        "code": demo_py,
        "language": "python",
        "icon": DashIconify(icon="skill-icons:python-dark", width=20),
    },
]


component = dmc.Stack(
    [
html.Div([  # Wrapper div for the carousel
        DashCarousel(
            id="my-carousel",
            className="custom-carousel",
            slides=[
            {
                "src": get_asset_url("images/01.jpg"),
                "alt": "Spider Man",
                "title": "Spider-Man: No Way Home",
                "description": "A thrilling superhero adventure.",
            },
            {
                "src": get_asset_url("images/02.jpg"),
                "alt": "Free Guy",
                "title": "Free Guy",
                "description": "A comedy about a video game NPC.",
            },
            {
                "src": get_asset_url("images/03.jpg"),
                "alt": "Nice Guys Finish Last",
                "title": "The Nice Guys",
                "description": "A neo-noir comedy thriller.",
            },
            {
                "src": get_asset_url("images/04.jpg"),
                "alt": "Cage",
                "title": "Cage",
                "description": "An intense action-packed movie.",
            },
            {
                "src": get_asset_url("images/05.jpg"),
                "alt": "Avatar",
                "title": "Avatar",
                "description": "An epic science fiction adventure.",
            },
        ],
            carouselEffect={
                "opacityStep": 0.33,
                "scaleStep": 0.2,
                "sideSlides": 1,
            },
            autoplayEnabled=False,
            autoplay={
                "delay": 3000,
                "disableOnInteraction": True,
            },
            loop=True,
            grabCursor=True,
            navigation=False,
            pagination=False,
            slidesPerView=5,
            style={"width": "100%", "height": "100%"},  # Set to 100% to fill the wrapper
        )
    ], style={"width": "100%", "height": "100px", "margin": "0 auto"}),
        html.Div(id='current-slide-display', style={"color": "white", "marginTop": "20px"}),
dmc.CodeHighlightTabs(
            code=code,
            withExpandButton=True,
            expandCodeLabel="Show full code",
            collapseCodeLabel="Show less",
            defaultExpanded=False,
            maxCollapsedHeight=200  # Height in collapsed state (in pixels)
        )
    ]
)

@callback(
    Output("current-slide-display", "children"),
    Input("my-carousel", "activeSlideAlt")
)
def display_active_slide(active_slide_alt):
    if active_slide_alt is None:
        raise PreventUpdate
    return f"Current Slide: {active_slide_alt}"