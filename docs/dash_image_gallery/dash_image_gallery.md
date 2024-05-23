---
name: Dash Image Gallery
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

### Props

.. exec::docs.dash_image_gallery.props
    :code: false

- `items`: (required) Array of objects, see example above,
  - Available Properties
    - `original` - image src url
    - `thumbnail` - image thumbnail src url
    - `fullscreen` - image for fullscreen (defaults to original)
    - `originalHeight` - image height (html5 attribute)
    - `originalWidth` - image width (html5 attribute)
    - `loading` - image loading. Either "lazy" or "eager" (html5 attribute)
    - `thumbnailHeight` - image height (html5 attribute)
    - `thumbnailWidth` - image width (html5 attribute)
    - `thumbnailLoading` - image loading. Either "lazy" or "eager" (html5 attribute)
    - `originalClass` - custom image class
    - `thumbnailClass` - custom thumbnail class
    - `renderItem` - Function for custom rendering a specific slide (see renderItem below)
    - `renderThumbInner` - Function for custom thumbnail renderer (see renderThumbInner below)
    - `originalAlt` - image alt
    - `thumbnailAlt` - thumbnail image alt
    - `originalTitle` - image title
    - `thumbnailTitle` - thumbnail image title
    - `thumbnailLabel` - label for thumbnail
    - `description` - description for image
    - `srcSet` - image srcset (html5 attribute)
    - `sizes` - image sizes (html5 attribute)
    - `bulletClass` - extra class for the bullet of the item
- `infinite`: Boolean, default `true`
  - infinite sliding
- `lazyLoad`: Boolean, default `false`
- `showNav`: Boolean, default `true`
- `showThumbnails`: Boolean, default `true`
- `thumbnailPosition`: String, default `bottom`
  - available positions: `top, right, bottom, left`
- `showFullscreenButton`: Boolean, default `true`
- `useBrowserFullscreen`: Boolean, default `true`
  - if false, fullscreen will be done via css within the browser
- `useTranslate3D`: Boolean, default `true`
  - if false, will use `translate` instead of `translate3d` css property to transition slides
- `showPlayButton`: Boolean, default `true`
- `isRTL`: Boolean, default `false`
  - if true, gallery's direction will be from right-to-left (to support right-to-left languages)
- `showBullets`: Boolean, default `false`
- `showIndex`: Boolean, default `false`
- `autoPlay`: Boolean, default `false`
- `disableThumbnailScroll`: Boolean, default `false`
  - disables the thumbnail container from adjusting
- `disableKeyDown`: Boolean, default `false`
  - disables keydown listener for keyboard shortcuts (left arrow, right arrow, esc key)
- `disableSwipe`: Boolean, default `false`
- `disableThumbnailSwipe`: Boolean, default `false`
- `onErrorImageURL`: String, default `undefined`
  - an image src pointing to your default image if an image fails to load
  - handles both slide image, and thumbnail image
- `indexSeparator`: String, default `' / '`, ignored if `showIndex` is false
- `slideDuration`: Number, default `450`
  - transition duration during image slide in milliseconds
- `swipingTransitionDuration`: Number, default `0`
  - transition duration while swiping in milliseconds
- `slideInterval`: Number, default `3000`
- `slideOnThumbnailOver`: Boolean, default `false`
- `flickThreshold`: Number (float), default `0.4`
  - Determines the max velocity of a swipe before it's considered a flick (lower = more sensitive)
- `swipeThreshold`: Number, default `30`
  - A percentage of how far the offset of the current slide is swiped to trigger a slide event.
    e.g. If the current slide is swiped less than 30% to the left or right, it will not trigger a slide event.
- `stopPropagation`: Boolean, default `false`
  - Automatically calls stopPropagation on all 'swipe' events.
- `startIndex`: Number, default `0`
- `onImageError`: Function, `callback(event)`
  - overrides onErrorImage
- `onThumbnailError`: Function, `callback(event)`
  - overrides onErrorImage
- `onThumbnailClick`: Function, `callback(event, index)`
- `onBulletClick`: Function, `callback(event, index)`
- `onImageLoad`: Function, `callback(event)`
- `onSlide`: Function, `callback(currentIndex)`
- `onBeforeSlide`: Function, `callback(nextIndex)`
- `onScreenChange`: Function, `callback(boolean)`
  - When fullscreen is toggled a boolean is passed to the callback
- `onPause`: Function, `callback(currentIndex)`
- `onPlay`: Function, `callback(currentIndex)`
- `onClick`: Function, `callback(event)`
- `onTouchMove`: Function, `callback(event) on gallery slide`
- `onTouchEnd`: Function, `callback(event) on gallery slide`
- `onTouchStart`: Function, `callback(event) on gallery slide`
- `onMouseOver`: Function, `callback(event) on gallery slide`
- `onMouseLeave`: Function, `callback(event) on gallery slide`
- `additionalClass`: String,
  - Additional class that will be added to the root node of the component.
- `renderItem`: Function, custom item rendering
  - NOTE: Highly suggest looking into a render cache such as React.memo if you plan to override renderItem
  - On a specific item `[{thumbnail: '...', renderItem: this.myRenderItem}]`
  - As a prop passed into `ImageGallery` to completely override `renderItem`, see source for renderItem implementation
- `renderThumbInner`: Function, custom thumbnail rendering
  - On a specific item `[{thumbnail: '...', renderThumbInner: this.myRenderThumbInner}]`
  - As a prop passed into `ImageGallery` to completely override `_renderThumbInner`, see source for reference
- `useWindowKeyDown`: Boolean, default `true`
  - If `true`, listens to keydown events on window (window.addEventListener)
  - If `false`, listens to keydown events on image gallery element (imageGalleryElement.addEventListener)



