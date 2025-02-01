---
name: Image Gallery
description: Image Gallery for dash.
endpoint: /pip/dash_image_gallery
package: dash_image_gallery
icon: ph:images-light
---

.. toc::

[Visit GitHub Repo](https://github.com/pip-install-python/dash_image_gallery)
### Installation

```bash
pip install dash-image-gallery
```

### Introduction

This is an example of a image gallery component. 

.. exec::docs.dash_image_gallery.introduction
    :code: false

### Props

.. exec::docs.dash_image_gallery.props
    :code: false

## Image Gallery Props
| Prop                        | Type    | Default     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-----------------------------|---------|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `items`                     | Array   | Required    | Array of objects containing image data. Each object can have the following properties: `original`, `thumbnail`, `fullscreen`, `originalHeight`, `originalWidth`, `loading`, `thumbnailHeight`, `thumbnailWidth`, `thumbnailLoading`, `originalClass`, `thumbnailClass`, `renderItem`, `renderThumbInner`, `originalAlt`, `thumbnailAlt`, `originalTitle`, `thumbnailTitle`, `thumbnailLabel`, `description`, `srcSet`, `sizes`, `bulletClass` |
| `infinite`                  | Boolean | `true`      | Enable infinite sliding                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `lazyLoad`                  | Boolean | `false`     | Enable lazy loading of images                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `showNav`                   | Boolean | `true`      | Show navigation arrows                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `showThumbnails`            | Boolean | `true`      | Show thumbnail strip                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `thumbnailPosition`         | String  | `'bottom'`  | Position of thumbnails. Options: `'top'`, `'right'`, `'bottom'`, `'left'`                                                                                                                                                                                                                                                                                                                                                                     |
| `showFullscreenButton`      | Boolean | `true`      | Show fullscreen toggle button                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `useBrowserFullscreen`      | Boolean | `true`      | Use browser's fullscreen API. If false, fullscreen will be done via CSS                                                                                                                                                                                                                                                                                                                                                                       |
| `useTranslate3D`            | Boolean | `true`      | Use `translate3d` instead of `translate` for transitions                                                                                                                                                                                                                                                                                                                                                                                      |
| `showPlayButton`            | Boolean | `true`      | Show play/pause button                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `isRTL`                     | Boolean | `false`     | Enable right-to-left direction                                                                                                                                                                                                                                                                                                                                                                                                                |
| `showBullets`               | Boolean | `false`     | Show navigation bullets                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `showIndex`                 | Boolean | `false`     | Show current image index                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `autoPlay`                  | Boolean | `false`     | Enable automatic slideshow                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `disableThumbnailScroll`    | Boolean | `false`     | Disable thumbnail container adjustment                                                                                                                                                                                                                                                                                                                                                                                                        |
| `disableKeyDown`            | Boolean | `false`     | Disable keyboard navigation (left/right/esc)                                                                                                                                                                                                                                                                                                                                                                                                  |
| `disableSwipe`              | Boolean | `false`     | Disable touch swipe                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `disableThumbnailSwipe`     | Boolean | `false`     | Disable thumbnail touch swipe                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `onErrorImageURL`           | String  | `undefined` | Default image URL to show if image fails to load                                                                                                                                                                                                                                                                                                                                                                                              |
| `indexSeparator`            | String  | `' / '`     | Separator for image index display                                                                                                                                                                                                                                                                                                                                                                                                             |
| `slideDuration`             | Number  | `450`       | Transition duration in milliseconds                                                                                                                                                                                                                                                                                                                                                                                                           |
| `swipingTransitionDuration` | Number  | `0`         | Swipe transition duration in milliseconds                                                                                                                                                                                                                                                                                                                                                                                                     |
| `slideInterval`             | Number  | `3000`      | Interval between slides in autoplay mode                                                                                                                                                                                                                                                                                                                                                                                                      |
| `slideOnThumbnailOver`      | Boolean | `false`     | Change slides on thumbnail hover                                                                                                                                                                                                                                                                                                                                                                                                              |
| `flickThreshold`            | Number  | `0.4`       | Swipe velocity threshold for flick detection                                                                                                                                                                                                                                                                                                                                                                                                  |
| `swipeThreshold`            | Number  | `30`        | Percentage of slide width that must be swiped to trigger slide change                                                                                                                                                                                                                                                                                                                                                                         |
| `stopPropagation`           | Boolean | `false`     | Stop event propagation on swipe events                                                                                                                                                                                                                                                                                                                                                                                                        |
| `startIndex`                | Number  | `0`         | Initial slide index                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `useWindowKeyDown`          | Boolean | `true`      | Listen for keydown events on window instead of gallery element                                                                                                                                                                                                                                                                                                                                                                                |

#### Callback Props

| Prop               | Type     | Parameters       | Description                              |
|--------------------|----------|------------------|------------------------------------------|
| `onImageError`     | Function | `(event)`        | Called when main image fails to load     |
| `onThumbnailError` | Function | `(event)`        | Called when thumbnail fails to load      |
| `onThumbnailClick` | Function | `(event, index)` | Called when thumbnail is clicked         |
| `onBulletClick`    | Function | `(event, index)` | Called when navigation bullet is clicked |
| `onImageLoad`      | Function | `(event)`        | Called when image loads successfully     |
| `onSlide`          | Function | `(currentIndex)` | Called after slide transition            |
| `onBeforeSlide`    | Function | `(nextIndex)`    | Called before slide transition           |
| `onScreenChange`   | Function | `(boolean)`      | Called when fullscreen mode changes      |
| `onPause`          | Function | `(currentIndex)` | Called when slideshow is paused          |
| `onPlay`           | Function | `(currentIndex)` | Called when slideshow starts playing     |
| `onClick`          | Function | `(event)`        | Called when gallery is clicked           |
| `onTouchMove`      | Function | `(event)`        | Called during touch move on gallery      |
| `onTouchEnd`       | Function | `(event)`        | Called when touch ends on gallery        |
| `onTouchStart`     | Function | `(event)`        | Called when touch starts on gallery      |
| `onMouseOver`      | Function | `(event)`        | Called on mouse over gallery             |
| `onMouseLeave`     | Function | `(event)`        | Called on mouse leave gallery            |

#### Rendering Props

| Prop               | Type     | Description                                                               |
|--------------------|----------|---------------------------------------------------------------------------|
| `additionalClass`  | String   | Additional CSS class for root element                                     |
| `renderItem`       | Function | Custom item renderer function. Can be specified globally or per-item      |
| `renderThumbInner` | Function | Custom thumbnail renderer function. Can be specified globally or per-item |
