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

### Introduction

This is an example of a dash swiper component with swipe transitions for images. You can add images to your swiper with `slides` witch can be cycled with arrow keys, automatic transitioned or swiped on mobile which will shade to the next image.

.. exec::docs.dash_swiper.introduction

### shader
shader is a prop in DashSwiper that allows you to add a shader to the image. You can add a `random`, `dots`, `flyeye`, `morph-x`, `morph-y`, `page-curl`, `peel-x`, `peel-y`, `polygons-fall`, `polygons-morph`, `polygons-wind`, `pixelize`, `ripple`, `shutters`, `slices`, `squares`, `stretch`, `wave-x`, `wind` shader to the image. Can either be a string with a single shader or a selection of shaders in a list.

.. exec::docs.dash_swiper.shaders
    :code: false

### swiperOptions

.. exec::docs.dash_swiper.swiper_options
    :code: false

