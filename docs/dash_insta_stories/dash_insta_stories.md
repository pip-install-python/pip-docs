---
name: Dash Insta Stories
description: Instagram / Snapchat stories component for dash.
endpoint: /pip/dash_insta_stories
package: dash_inta_stories
icon: material-symbols:web-stories-outline
---

.. toc::

[Visit GitHub Repo](https://github.com/pip-install-python/dash_insta_stories)

### Installation

```bash
pip install dash-insta-stories
```

### Introduction

This is an example of dash insta stories component. 

.. exec::docs.dash_insta_stories.introduction

## Props

| Property               | Type            | Default                   | Description                                                                                                                                                         |
| ---------------------- | --------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stories`              | [String/Object] | `required`                | An array of image urls or array of story objects (options described below)                                                                                          |
| `renderers` ⚡️        | [Object]        | `[]`                      | An array of renderer objects (options described below)                                                                                                              |
| `defaultInterval`      | Number          | 1200                      | Milliseconds duration for which a story persists                                                                                                                    |
| `loader`               | Component       | Ripple loader             | A loader component as a fallback until image loads from url                                                                                                         |
| `header`               | Component       | Default header as in demo | A header component which sits at the top of each story. It receives the `header` object from the `story` object. Data for header to be sent with each story object. |
| `storyContainerStyles` | Object          | `{}`                      | Styles object for the outer container                                                                                                                               |
| `width`                | Number/String   | 360                       | Width of the component, e.g. 600 or '100vw' or 'inherit'                                                                                                            |
| `height`               | Number/String   | 640                       | Height of the component, e.g. 1000 or '100%' or 'inherit'                                                                                                           |
| `storyStyles`          | Object          | none                      | Override the default story styles mentioned below.                                                                                                                  |
| `progressContainerStyles` | Object          | `{}`                      | Styles object for the container wrapping the progress bars                                                                                                                 |
| `progressWrapperStyles` | Object          | `{}`                      | Styles object for the container wrapping each progress bar bars                                                                                                                 |
| `progressStyles`       | Object          | `{}`                      | Styles object for the progress bars                                                                                                                 |
| `loop`                 | Boolean         | false                     | The last story loop to the first one and restart the stories.                                                                                                       |
| **New props**          | ⭐️             | ⭐️                       | ⭐️                                                                                                                                                                 |
| `isPaused`             | Boolean         | false                     | Toggle story playing state                                                                                                                                          |
| `currentIndex`         | Number          | undefined                 | Set the current story index                                                                                                                                         |
| `onStoryStart`         | Function        | -                         | Callback when a story starts                                                                                                                                        |
| `onStoryEnd`           | Function        | -                         | Callback when a story ends                                                                                                                                          |
| `onAllStoriesEnd`      | Function        | -                         | Callback when all stories in the array have ended                                                                                                                   |
| `onNext`               | Function        | -                         | Callback when the user taps/press to proceed to the next story                                                                                                                   |
| `onPrevious`           | Function        | -                         | Callback when the user taps/press to go back to the previous story                                                                                                                    |
| `keyboardNavigation`   | Boolean         | false                     | Attaches arrow key listeners to navigate between stories if true. Also adds up arrow key listener for opening See More and Escape/down arrow for closing it         |
| `preventDefault`       | Boolean         | false                     | Disable the default behavior when user click the component                                                                                                          |
| `preloadCount`         | number          | 1                         | Determines how many stories should be preloaded ahead of the current story index.                                                                                   |

### Story object

Instead of simple string url, a comprehensive 'story object' can also be passed in the `stories` array.

| Property          | Description                                                                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `url`             | The url of the resource, be it image or video.                                                                                                |
| `type`            | Optional. Type of the story. `type: 'video'`                                                                                                  |
| `duration`        | Optional. Duration for which a story should persist.                                                                                          |
| `header`          | Optional. Adds a header on the top. Object with `heading`, `subheading` and `profileImage` properties.                                        |
| `seeMore`         | Optional. Adds a see more icon at the bottom of the story. On clicking, opens up this component. (v2: updated to Function instead of element) |
| `seeMoreCollapsed`| Optional. Send custom component to be rendered instead of the default 'See More' text.                                                         |
| `styles`          | Optional. Override the default story styles mentioned below.                                                                                  |
| `preloadResource` | Optional. Whether to preload the resource or not, defaults to `true` for images and `false` for videos (video preloading is experimental)     |

