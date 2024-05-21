import dash_insta_stories
from dash import *

# Define your stories
stories = [
    {
        "url": "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
        "type": "image",
        "duration": 5000,
        "header": {
            "heading": "Colorize lizard",
            "subheading": "Cute isn't he?",
            "profileImage": "https://sea2.discourse-cdn.com/business7/user_avatar/community.plotly.com/pipinstallpython/288/27532_2.png"
        },
        # "seeMore": lambda: {"url": "https://example.com"},
        "styles": {"background": "#f5f5f5"},
        "preloadResource": True
    },
    {
        "url": "https://www.simplilearn.com/ice9/free_resources_article_thumb/what_is_image_Processing.jpg",
        "header": {
            "heading": "Eyeseast",
            "subheading": "👀",
            "profileImage": "https://sea2.discourse-cdn.com/business7/user_avatar/community.plotly.com/pipinstallpython/288/27532_2.png"
        }
    },
{
        "url": "https://www.adobe.com/products/media_14562ad96c12a2f3030725ae81bd3ede1c68cb783.jpeg?width=750&format=jpeg&optimize=medium",
        "header": {
            "heading": "backster",
            "subheading": "puppies with sweaters",
            "profileImage": "https://sea2.discourse-cdn.com/business7/user_avatar/community.plotly.com/pipinstallpython/288/27532_2.png"
        }
    }
    # Add more stories as needed
]

component = dmc.SimpleGrid(
    [
        dmc.Paper(
            html.Div(id="view-insta-stories-output"),
            id="intro-wrapper-insta-stories",
            style={"gridColumn": "1 / 4"},
        ),
        dmc.NumberInput(id='defaultInterval', label='defaultInterval', value=2200),
        dmc.NumberInput(id='width', label='width', value=360),
        dmc.NumberInput(id='height', label='height', value=640),
    ]
)


