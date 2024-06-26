# id: PropTypes.string,
# items: PropTypes.arrayOf(PropTypes.shape({
#     original: PropTypes.string,
#     thumbnail: PropTypes.string,
#     fullscreen: PropTypes.string,
#     originalHeight: PropTypes.number,
#     originalWidth: PropTypes.number,
#     loading: PropTypes.string,
#     thumbnailHeight: PropTypes.number,
#     thumbnailWidth: PropTypes.number,
#     thumbnailLoading: PropTypes.string,
#     originalClass: PropTypes.string,
#     thumbnailClass: PropTypes.string,
#     renderItem: PropTypes.func,
#     renderThumbInner: PropTypes.func,
#     originalAlt: PropTypes.string,
#     thumbnailAlt: PropTypes.string,
#     originalTitle: PropTypes.string,
#     thumbnailTitle: PropTypes.string,
#     thumbnailLabel: PropTypes.string,
#     description: PropTypes.string,
#     srcSet: PropTypes.string,
#     sizes: PropTypes.string,
#     bulletClass: PropTypes.string
# })).isRequired,
# infinite: PropTypes.bool,
# lazyLoad: PropTypes.bool,
# showNav: PropTypes.bool,
# showThumbnails: PropTypes.bool,
# thumbnailPosition: PropTypes.string,
# showFullscreenButton: PropTypes.bool,
# useBrowserFullscreen: PropTypes.bool,
# useTranslate3D: PropTypes.bool,
# showPlayButton: PropTypes.bool,
# isRTL: PropTypes.bool,
# showBullets: PropTypes.bool,
# showIndex: PropTypes.bool,
# autoPlay: PropTypes.bool,
# disableThumbnailScroll: PropTypes.bool,
# disableKeyDown: PropTypes.bool,
# disableSwipe: PropTypes.bool,
# disableThumbnailSwipe: PropTypes.bool,
# onErrorImageURL: PropTypes.string,
# indexSeparator: PropTypes.string,
# slideDuration: PropTypes.number,
# swipingTransitionDuration: PropTypes.number,
# slideInterval: PropTypes.number,
# slideOnThumbnailOver: PropTypes.bool,
# flickThreshold: PropTypes.number,
# swipeThreshold: PropTypes.number,
# stopPropagation: PropTypes.bool,
# startIndex: PropTypes.number,
# onImageError: PropTypes.func,
# onThumbnailError: PropTypes.func,
# onThumbnailClick: PropTypes.func,
# onBulletClick: PropTypes.func,
# onImageLoad: PropTypes.func,
# onSlide: PropTypes.func,
# onBeforeSlide: PropTypes.func,
# onScreenChange: PropTypes.func,
# onPause: PropTypes.func,
# onPlay: PropTypes.func,
# onClick: PropTypes.func,
# onTouchMove: PropTypes.func,
# onTouchEnd: PropTypes.func,
# onTouchStart: PropTypes.func,
# onMouseOver: PropTypes.func,
# onMouseLeave: PropTypes.func,
# additionalClass: PropTypes.string,
# renderCustomControls: PropTypes.func,
# renderItem: PropTypes.func,
# renderThumbInner: PropTypes.func,
# renderLeftNav: PropTypes.func,
# renderRightNav: PropTypes.func,
# renderPlayPauseButton: PropTypes.func,
# renderFullscreenButton: PropTypes.func,
# useWindowKeyDown: PropTypes.bool,

from dash import *
import dash_image_gallery
import dash_mantine_components as dmc

component = dmc.SimpleGrid(
    cols={"base": 1, "sm": 1, "lg": 4},
    children=[
        dmc.Paper(
            html.Div(id="view-dig"),
            id="intro-wrapper-dig",
            style={"gridColumn": "1 / 4"},
        ),
        dmc.Stack(
            [
                dmc.Checkbox(id="dig-checkbox-infinite", label="infinite", mb=10, checked=True),
                dmc.Checkbox(id="dig-checkbox-lazyLoad", label="lazyLoad", mb=10, checked=False),
                dmc.Checkbox(id="dig-checkbox-showNav", label="showNav", mb=10, checked=True),
                dmc.Checkbox(id="dig-checkbox-showThumbnails", label="showThumbnails", mb=10, checked=True),
                dmc.Select(
                            label="Select thumbnailPosition",
                            placeholder="Select one",
                            id="dig-text-thumbnailPosition",
                            value="right",
                            data=[
                                {"value": "top", "label": "top"},
                                {"value": "right", "label": "right"},
                                {"value": "left", "label": "left"},
                                {"value": "bottom", "label": "bottom"},

                            ],
                        ),
                # dmc.TextInput(id="dig-text-thumbnailPosition", label="thumbnailPosition", mb=10, value="bottom"),
                dmc.Checkbox(id="dig-checkbox-showFullscreenButton", label="showFullscreenButton", mb=10, checked=True),
                dmc.Checkbox(id="dig-checkbox-useBrowserFullscreen", label="useBrowserFullscreen", mb=10, checked=True),
                dmc.Checkbox(id="dig-checkbox-useTranslate3D", label="useTranslate3D", mb=10, checked=True),
                dmc.Checkbox(id="dig-checkbox-showPlayButton", label="showPlayButton", mb=10, checked=True),
                dmc.Checkbox(id="dig-checkbox-isRTL", label="isRTL", mb=10, checked=False),
                dmc.Checkbox(id="dig-checkbox-showBullets", label="showBullets", mb=10, checked=False),
                dmc.Checkbox(id="dig-checkbox-showIndex", label="showIndex", mb=10, checked=True),
                dmc.Checkbox(id="dig-checkbox-autoPlay", label="autoPlay", mb=10, checked=True),
                dmc.Checkbox(id="dig-checkbox-disableThumbnailScroll", label="disableThumbnailScroll", mb=10, checked=False),
                dmc.Checkbox(id="dig-checkbox-disableKeyDown", label="disableKeyDown", mb=10, checked=False),
                dmc.Checkbox(id="dig-checkbox-disableSwipe", label="disableSwipe", mb=10, checked=False),
                dmc.Checkbox(id="dig-checkbox-disableThumbnailSwipe", label="disableThumbnailSwipe", mb=10, checked=False),
                dmc.TextInput(id="dig-text-onErrorImageURL", label="onErrorImageURL", mb=10, value=""),
                dmc.TextInput(id="dig-text-indexSeparator", label="indexSeparator", mb=10, value=" / "),
                dmc.NumberInput(id="dig-number-slideDuration", label="slideDuration", mb=10, value=450),
                dmc.NumberInput(id="dig-number-swipingTransitionDuration", label="swipingTransitionDuration", mb=10, value=0),
                dmc.NumberInput(id="dig-number-slideInterval", label="slideInterval", mb=10, value=3000),
                dmc.Checkbox(id="dig-checkbox-slideOnThumbnailOver", label="slideOnThumbnailOver", mb=10, checked=True),
                dmc.NumberInput(id="dig-number-flickThreshold", label="flickThreshold", mb=10, value=0.4),
                dmc.NumberInput(id="dig-number-swipeThreshold", label="swipeThreshold", mb=10, value=30),
                dmc.Checkbox(id="dig-checkbox-stopPropagation", label="stopPropagation", mb=10, checked=False),
                dmc.NumberInput(id="dig-number-startIndex", label="startIndex", mb=10, value=0),
                dmc.Checkbox(id="dig-checkbox-useWindowKeyDown", label="useWindowKeyDown", mb=10, checked=True),


            ],
            style={'overflow-y': 'auto', 'max-height': '500px'},
        ),
    ],
    spacing="2rem",
)


@callback(
    Output('view-dig', 'children'),
    [
        Input("dig-checkbox-infinite", "checked"),
        Input("dig-checkbox-lazyLoad", "checked"),
        Input("dig-checkbox-showNav", "checked"),
        Input("dig-checkbox-showThumbnails","checked"),
        Input("dig-text-thumbnailPosition", "value"),
        Input("dig-checkbox-showFullscreenButton", "checked"),
        Input("dig-checkbox-useBrowserFullscreen", "checked"),
        Input("dig-checkbox-useTranslate3D", "checked"),
        Input("dig-checkbox-showPlayButton", "checked"),
        Input("dig-checkbox-isRTL", "checked"),
        Input("dig-checkbox-showBullets", "checked"),
        Input("dig-checkbox-showIndex", "checked"),
        Input("dig-checkbox-autoPlay", "checked"),
        Input("dig-checkbox-disableThumbnailScroll", "checked"),
        Input("dig-checkbox-disableKeyDown", "checked"),
        Input("dig-checkbox-disableSwipe", "checked"),
        Input("dig-checkbox-disableThumbnailSwipe", "checked"),
        Input("dig-text-onErrorImageURL", "value"),
        Input("dig-text-indexSeparator", "value"),
        Input("dig-number-slideDuration", "value"),
        Input("dig-number-swipingTransitionDuration", "value"),
        Input("dig-number-slideInterval", "value"),
        Input("dig-checkbox-slideOnThumbnailOver", "checked"),
        Input("dig-number-flickThreshold", "value"),
        Input("dig-number-swipeThreshold", "value"),
        Input("dig-checkbox-stopPropagation", "checked"),
        Input("dig-number-startIndex", "value"),
        Input("dig-checkbox-useWindowKeyDown", "checked"),
    ]
)
def update_image_gallery(infinite, lazyLoad, showNav, showThumbnails, thumbnailPosition, showFullscreenButton, useBrowserFullscreen, useTranslate3D, showPlayButton, isRTL, showBullets, showIndex, autoPlay, disableThumbnailScroll, disableKeyDown, disableSwipe, disableThumbnailSwipe, onErrorImageURL, indexSeparator, slideDuration, swipingTransitionDuration, slideInterval, slideOnThumbnailOver, flickThreshold, swipeThreshold, stopPropagation, startIndex, useWindowKeyDown):
    return dash_image_gallery.DashImageGallery(
        id='dig-input',
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
        infinite=infinite,
        lazyLoad=lazyLoad,
        showNav=showNav,
        showThumbnails=showThumbnails,
        thumbnailPosition=thumbnailPosition,
        showFullscreenButton=showFullscreenButton,
        useBrowserFullscreen=useBrowserFullscreen,
        useTranslate3D=useTranslate3D,
        showPlayButton=showPlayButton,
        isRTL=isRTL,
        showBullets=showBullets,
        showIndex=showIndex,
        autoPlay=autoPlay,
        disableThumbnailScroll=disableThumbnailScroll,
        disableKeyDown=disableKeyDown,
        disableSwipe=disableSwipe,
        disableThumbnailSwipe=disableThumbnailSwipe,
        onErrorImageURL=onErrorImageURL,
        indexSeparator=indexSeparator,
        slideDuration=slideDuration,
        swipingTransitionDuration=swipingTransitionDuration,
        slideInterval=slideInterval,
        slideOnThumbnailOver=slideOnThumbnailOver,
        flickThreshold=flickThreshold,
        swipeThreshold=swipeThreshold,
        stopPropagation=stopPropagation,
        startIndex=startIndex,
        useWindowKeyDown=useWindowKeyDown
    )