from dash_swiper import DashSwiper
from dash import *
import dash_mantine_components as dmc
from dash_iconify import DashIconify

demo_py = """
import dash
from dash import *
import dash_mantine_components as dmc

app = dash.Dash(__name__, external_stylesheets=dmc.styles.ALL)


 app.layout = dmc.MantineProvider([dmc.Stack(
    [
        DashSwiper(
            id="my-swiper",
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
            shader="random",  # Add the shader effect here

        ),
    ],
    style={"width": "100%", "height": "50vh"},
)])
 
if __name__ == '__main__':
    app.run_server(debug=True, port='8050')
"""


code = [
    {
        "fileName": "swiper_example.py",
        "code": demo_py,
        "language": "python",
        "icon": DashIconify(icon="skill-icons:python-dark", width=20),
    },
]

component = dmc.Stack(
    [
        html.Div(DashSwiper(
            id="my-swiper",
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
            shader="random",  # Add the shader effect here
        ), style={"width": "100%", "height": "50vh"}),
        dmc.CodeHighlightTabs(
            code=code,
            withExpandButton=True,
            expandCodeLabel="Show full code",
            collapseCodeLabel="Show less",
            defaultExpanded=False,
            maxCollapsedHeight=200  # Height in collapsed state (in pixels)
        )
    ],
)