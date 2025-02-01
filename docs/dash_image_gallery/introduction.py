from dash import *
from dash_image_gallery import DashImageGallery
import dash_mantine_components as dmc
from dash_iconify import DashIconify

demo_py = """
import dash
from dash import *
import dash_mantine_components as dmc

app = dash.Dash(__name__, external_stylesheets=dmc.styles.ALL)

# Define your stories
stories = [
    {
        "url": "/assets/images/dash_insta_stories_0.png",
        "type": "image",
        "duration": 5000,
        "header": {
            "heading": "",
            "subheading": "Cute isn't he?",
            "profileImage": "https://avatars.githubusercontent.com/u/120129682?v=4"
        },
        # "seeMore": lambda: {"url": "https://example.com"},
        "styles": {"background": "#f5f5f5"},
        "preloadResource": True
    },
    {
        "url": "/assets/images/dash_insta_stories_1.png",
        "header": {
            "heading": "Mobile view of a Django app I've built check out the blog posts",
            "subheading": "👀",
            "profileImage": "https://avatars.githubusercontent.com/u/120129682?v=4"
        }
    },
    {
        "url": "/assets/images/dash_insta_stories_2.png",
        "header": {
            "heading": "Buy something from me? 🤑",
            "subheading": "Mobile view of an e-commerce site I've built.",
            "profileImage": "https://avatars.githubusercontent.com/u/120129682?v=4"
        }
    }
    # Add more stories as needed
]


 app.layout = dmc.MantineProvider([html.Div([
    DashImageGallery(
        id='input',
        items=[
            {
                "original": "https://cdn.britannica.com/78/43678-050-F4DC8D93/Starry-Night-canvas-Vincent-van-Gogh-New-1889.jpg",
                "thumbnail": "https://cdn.britannica.com/78/43678-050-F4DC8D93/Starry-Night-canvas-Vincent-van-Gogh-New-1889.jpg",
                "originalHeight": 300,
                "originalWidth": 300,
            },
            {
                "original": "https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/5eeea355389655.59822ff824b72.gif",
                "thumbnail": "https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/5eeea355389655.59822ff824b72.gif",
                "originalHeight": 300,
                "originalWidth": 300,
            },
            {
                "original": "https://www.theartstory.org/images20/hero/profile/van_gogh_vincent_525.jpg",
                "thumbnail": "https://www.theartstory.org/images20/hero/profile/van_gogh_vincent_525.jpg",
                "originalHeight": 300,
                "originalWidth": 300,
            },
            {
                "original": "/assets/images/03.jpg",
                "thumbnail": "/assets/images/03.jpg",
                "originalHeight": 300,
                "originalWidth": 300,
            },
        ],
        infinite=True,
        lazyLoad=False,
        showNav=True,
        showThumbnails=True,
        thumbnailPosition='bottom',
        showFullscreenButton=True,
        useBrowserFullscreen=True,
        useTranslate3D=True,
        showPlayButton=True,
        isRTL=False,
        showBullets=False,
        showIndex=True,
        autoPlay=True,
        disableThumbnailScroll=False,
        disableKeyDown=False,
        disableSwipe=False,
        disableThumbnailSwipe=False,
        onErrorImageURL=None,
        indexSeparator=' / ',
        slideDuration=450,
        swipingTransitionDuration=0,
        slideInterval=3000,
        slideOnThumbnailOver=True,
        flickThreshold=0.4,
        swipeThreshold=30,
        stopPropagation=False,
        startIndex=0,
        useWindowKeyDown=True,
    )
], style={'width': '100%', 'overflow':'auto'})
])


if __name__ == '__main__':
    app.run_server(debug=True, port='8050')
"""

code = [
    {
        "fileName": "insta_stories.py",
        "code": demo_py,
        "language": "python",
        "icon": DashIconify(icon="skill-icons:python-dark", width=20),
    },
]

component = dmc.Stack([DashImageGallery(
        id='input',
        items=[
            {
                "original": "https://cdn.britannica.com/78/43678-050-F4DC8D93/Starry-Night-canvas-Vincent-van-Gogh-New-1889.jpg",
                "thumbnail": "https://cdn.britannica.com/78/43678-050-F4DC8D93/Starry-Night-canvas-Vincent-van-Gogh-New-1889.jpg",
                "originalHeight": 300,
                "originalWidth": 300,
            },
            {
                "original": "https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/5eeea355389655.59822ff824b72.gif",
                "thumbnail": "https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/5eeea355389655.59822ff824b72.gif",
                "originalHeight": 300,
                "originalWidth": 300,
            },
            {
                "original": "https://www.theartstory.org/images20/hero/profile/van_gogh_vincent_525.jpg",
                "thumbnail": "https://www.theartstory.org/images20/hero/profile/van_gogh_vincent_525.jpg",
                "originalHeight": 300,
                "originalWidth": 300,
            },
            {
                "original": "/assets/images/03.jpg",
                "thumbnail": "/assets/images/03.jpg",
                "originalHeight": 300,
                "originalWidth": 300,
            },
        ],
        infinite=True,
        lazyLoad=False,
        showNav=True,
        showThumbnails=True,
        thumbnailPosition='bottom',
        showFullscreenButton=True,
        useBrowserFullscreen=True,
        useTranslate3D=True,
        showPlayButton=True,
        isRTL=False,
        showBullets=False,
        showIndex=True,
        autoPlay=True,
        disableThumbnailScroll=False,
        disableKeyDown=False,
        disableSwipe=False,
        disableThumbnailSwipe=False,
        onErrorImageURL=None,
        indexSeparator=' / ',
        slideDuration=450,
        swipingTransitionDuration=0,
        slideInterval=3000,
        slideOnThumbnailOver=True,
        flickThreshold=0.4,
        swipeThreshold=30,
        stopPropagation=False,
        startIndex=0,
        useWindowKeyDown=True,
    ), dmc.CodeHighlightTabs(
            code=code,
            withExpandButton=True,
            expandCodeLabel="Show full code",
            collapseCodeLabel="Show less",
            defaultExpanded=False,
            maxCollapsedHeight=200  # Height in collapsed state (in pixels)
        )])