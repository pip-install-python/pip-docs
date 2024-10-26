import dash_insta_stories
from dash import *

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

component = html.Div([
    dash_insta_stories.DashInstaStories(
        id='input',
        stories=stories,  # Pass the stories to DashInstaStories
        renderers=[],  # Pass the renderers to DashInstaStories
        defaultInterval=2200,  # Pass the defaultInterval to DashInstaStories
        loader=None,  # Pass the loader to DashInstaStories
        header=None,  # Pass the header to DashInstaStories
        storyContainerStyles={},  # Pass the storyContainerStyles to DashInstaStories
        width=360,  # Pass the width to DashInstaStories
        height=640,  # Pass the height to DashInstaStories
        storyStyles={},  # Pass the storyStyles to DashInstaStories
        progressContainerStyles={},  # Pass the progressContainerStyles to DashInstaStories
        progressWrapperStyles={},  # Pass the progressWrapperStyles to DashInstaStories
        progressStyles={},  # Pass the progressStyles to DashInstaStories
        loop=True,  # Pass the loop to DashInstaStories
        isPaused=False,  # Pass the isPaused to DashInstaStories
        currentIndex=None,  # Pass the currentIndex to DashInstaStories
        # onStoryStart=None,  # Pass the onStoryStart to DashInstaStories
        # onStoryEnd=None,  # Pass the onStoryEnd to DashInstaStories
        # onAllStoriesEnd=None,  # Pass the onAllStoriesEnd to DashInstaStories
        # onNext=None,  # Pass the onNext to DashInstaStories
        # onPrevious=None,  # Pass the onPrevious to DashInstaStories
        keyboardNavigation=True,  # Pass the keyboardNavigation to DashInstaStories
        preventDefault=False,  # Pass the preventDefault to DashInstaStories
        preloadCount=1,  # Pass the preloadCount to DashInstaStories
    ),
], style={'width': '100%', 'overflow':'auto'})