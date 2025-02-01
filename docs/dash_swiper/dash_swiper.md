---
name: Swiper
description: Fancy swipe transitions for images.
endpoint: /pip/dash_swiper
package: dash_swiper
icon: ph:hand-swipe-right-duotone
---

.. toc::

[Visit GitHub Repo](https://github.com/pip-install-python/dash_swiper)

### Installation

```bash
pip install dash-swiper
```

### Swiper Introduction

This is an example of a dash swiper component with swipe transitions for images. You can add images to your swiper with `slides` witch can be cycled with arrow keys, automatic transitioned or swiped on mobile which will shade to the next image.

.. exec::docs.dash_swiper.introduction
    :code: false

### Shader Options
shader is a prop in DashSwiper that allows you to add a shader to the image. You can add a `random`, `dots`, `flyeye`, `morph-x`, `morph-y`, `page-curl`, `peel-x`, `peel-y`, `polygons-fall`, `polygons-morph`, `polygons-wind`, `pixelize`, `ripple`, `shutters`, `slices`, `squares`, `stretch`, `wave-x`, `wind` shader to the image. Can either be a string with a single shader or a selection of shaders in a list.

.. exec::docs.dash_swiper.shaders
    :code: false

### swiperOptions

.. exec::docs.dash_swiper.swiper_options
    :code: false

### Swiper Options / Props Tables

| Option        | Default | Choices          | Description                                                                                                                    |
|---------------|---------|------------------|--------------------------------------------------------------------------------------------------------------------------------|
| id            | `none`  |                  | The ID used to identify this component in Dash callbacks                                                                       |
| autoplay      | `none`  |                  | Configuration object for autoplay behavior with properties: delay (in ms) and disableOnInteraction (boolean)                   |
| className     | `none`  |                  | Additional CSS class for the root element                                                                                      |
| loop          | `none`  |                  | If true, enables continuous loop mode                                                                                          |
| navigation    | `none`  |                  | Configuration object for navigation with properties: prevEl (CSS selector/HTML element) and nextEl (CSS selector/HTML element) |
| nextButton    | `none`  |                  | If true, displays the next navigation button                                                                                   |
| pagination    | `none`  |                  | Configuration object for pagination with properties: el (CSS selector/HTML element) and clickable (boolean)                    |
| prevButton    | `none`  |                  | If true, displays the previous navigation button                                                                               |
| shader        | `none`  | array of strings | An array of shader names to be used for the WebGL effect                                                                       |
| slides        | `none`  |                  | An array of objects representing the slides. Each object requires: src (required), alt, title, link                            |
| speed         | `none`  |                  | The transition speed between slides in milliseconds                                                                            |
| swiperOptions | `none`  |                  | Additional options to pass directly to Swiper instance                                                                         |

#### Slide Object Properties
| Property | Required | Type   | Description                       |
|----------|----------|--------|-----------------------------------|
| src      | Yes      | string | The source URL of the slide image |
| alt      | No       | string | Alternative text for the image    |
| title    | No       | string | Title text for the slide          |
| link     | No       | string | URL link for the slide            |

#### Autoplay Configuration
| Property             | Type    | Description                                  |
|----------------------|---------|----------------------------------------------|
| delay                | number  | Delay between transitions (in milliseconds)  |
| disableOnInteraction | boolean | Whether to stop autoplay on user interaction |

#### Navigation Configuration
| Property | Type   | Description                                          |
|----------|--------|------------------------------------------------------|
| prevEl   | string | CSS selector or HTML element for the previous button |
| nextEl   | string | CSS selector or HTML element for the next button     |

#### Pagination Configuration
| Property  | Type    | Description                                               |
|-----------|---------|-----------------------------------------------------------|
| el        | string  | CSS selector or HTML element for the pagination container |
| clickable | boolean | If true, pagination bullets will be clickable             |

### Carousel Introduction
___

.. exec::docs.dash_swiper.carousel
    :code: false

# Dynamic Prop Example
.. exec::docs.dash_swiper.basic_carousel
    :code: false


### Carousel Options / Props Tables

| Option          | Default | Choices | Description                                                                                          |
|-----------------|---------|---------|------------------------------------------------------------------------------------------------------|
| id              | `none`  |         | The ID used to identify this component in Dash callbacks                                             |
| activeIndex     | `none`  |         | The index of the currently active slide                                                              |
| activeSlideAlt  | `none`  |         | The alt text of the currently active slide                                                           |
| autoplay        | `none`  |         | Configuration object for autoplay behavior with properties: delay and disableOnInteraction           |
| autoplayEnabled | `none`  |         | Whether autoplay is enabled                                                                          |
| carouselEffect  | `none`  |         | Configuration object for the carousel effect with properties: opacityStep, scaleStep, and sideSlides |
| className       | `none`  |         | Additional CSS class for the root element                                                            |
| grabCursor      | `none`  |         | Whether to change the cursor to "grab" while swiping                                                 |
| loop            | `none`  |         | Whether to enable continuous loop mode                                                               |
| navigation      | `none`  |         | Whether to display navigation buttons                                                                |
| pagination      | `none`  |         | Whether to display pagination dots                                                                   |
| slides          | `none`  |         | An array of objects representing the slides (required)                                               |
| slidesPerView   | `none`  |         | Number of slides per view                                                                            |
| style           | `none`  |         | Custom inline styles to be applied to the carousel container                                         |
| swiperOptions   | `none`  |         | Additional options to pass directly to Swiper instance                                               |

#### Slide Object Properties
| Property    | Required | Type   | Description                       |
|-------------|----------|--------|-----------------------------------|
| src         | Yes      | string | The source URL of the slide image |
| alt         | No       | string | Alternative text for the image    |
| title       | No       | string | Title text for the slide          |
| description | No       | string | Description text for the slide    |

#### Autoplay Configuration
| Property             | Type    | Description                                   |
|----------------------|---------|-----------------------------------------------|
| delay                | number  | Delay between transitions (in milliseconds)   |
| disableOnInteraction | boolean | Whether to pause autoplay on user interaction |

#### Carousel Effect Configuration
| Property    | Type   | Description                                  |
|-------------|--------|----------------------------------------------|
| opacityStep | number | Step value for opacity change between slides |
| scaleStep   | number | Step value for scale change between slides   |
| sideSlides  | number | Number of side slides visible                |