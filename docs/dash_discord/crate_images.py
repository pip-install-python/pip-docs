from dash_image_gallery import DashImageGallery
from dash import *

component = DashImageGallery(
        id='input',
        items=[
            {
                "original": "/assets/images/discord_crate_example.gif",
                "thumbnail": "/assets/images/discord_crate_example.gif",
                "originalHeight": 300,
                "originalWidth": 300,
            },
            {
                "original": "/assets/images/discord_crate.png",
                "thumbnail": "/assets/images/discord_crate.png",
                "originalHeight": 300,
                "originalWidth": 300,
            },
            {
                "original": "/assets/images/discord_store.png",
                "thumbnail": "/assets/images/discord_store.png",
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
        autoPlay=False,
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
        useWindowKeyDown=True
    )