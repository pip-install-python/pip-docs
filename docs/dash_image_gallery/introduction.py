from dash import *
import dash_image_gallery

component = html.Div([
    dash_image_gallery.DashImageGallery(
        id='input',
        items=[
            {
                "original": "https://cdn.britannica.com/78/43678-050-F4DC8D93/Starry-Night-canvas-Vincent-van-Gogh-New-1889.jpg",
                "thumbnail": "https://cdn.britannica.com/78/43678-050-F4DC8D93/Starry-Night-canvas-Vincent-van-Gogh-New-1889.jpg",
            },
            {
                "original": "https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/5eeea355389655.59822ff824b72.gif",
                "thumbnail": "https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/5eeea355389655.59822ff824b72.gif",
            },
            {
                "original": "https://www.theartstory.org/images20/hero/profile/van_gogh_vincent_525.jpg",
                "thumbnail": "https://www.theartstory.org/images20/hero/profile/van_gogh_vincent_525.jpg",
            },
            {
                "original": "/assets/image4.png",
                "thumbnail": "/assets/image4.png",
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
    ),
])