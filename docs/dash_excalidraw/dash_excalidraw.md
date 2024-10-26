---
name: Dash Excalidraw
description: Notebook, Freeform, Drawing type of component.
endpoint: /pip/dash_excalidraw
package: dash_excalidraw
icon: simple-icons:libreofficedraw
---

.. toc::

[Visit GitHub Repo](https://github.com/pip-install-python/dash_emoji_mart)

Features
The Excalidraw editor (pip dash package) supports:

- 💯 Free & open-source.
- 🎨 Infinite, canvas-based whiteboard.
- ✍️ Hand-drawn like style.
- 🌓 Dark mode.
- 🏗️ Customizable.
- 📷 Image support.
- 😀 Shape libraries support.
- 👅 Localization (i18n) support.
- 🖼️ Export to PNG, SVG & clipboard.
- 💾 Open format - export drawings as an .excalidraw json file.
- ⚒️ Wide range of tools - rectangle, circle, diamond, arrow, line, free-draw, eraser...
- ➡️ Arrow-binding & labeled arrows.
- 🔙 Undo / Redo.
- 🔍 Zoom and panning support.
- 🚀 +Many more...

### Installation

```bash
pip install dash-excalidraw
```

### Introduction

.. exec::docs.dash_excalidraw.introduction

### Simple Example

.. exec::docs.dash_excalidraw.simple_example

### Options / Props

| Option                 | Default                          | Choices                                       | Description                                               |
|------------------------|----------------------------------|-----------------------------------------------|-----------------------------------------------------------|
| id                     | `none`                           |                                               | The ID used to identify this component in Dash callbacks  |
| width                  | `'100%'`                         |                                               | The width of the Excalidraw component                     |
| height                 | `'400px'`                        |                                               | The height of the Excalidraw component                    |
| initialData            | `{ elements: [], appState: {} }` |                                               | Initial data to load into the Excalidraw component        |
| elements               | `[]`                             |                                               | The current elements in the Excalidraw scene              |
| appState               | `{}`                             |                                               | The current application state of Excalidraw               |
| files                  | `{}`                             |                                               | Files associated with the Excalidraw scene                |
| serializedData         | `''`                             |                                               | Serialized data of the entire Excalidraw scene            |
| excalidrawAPI          | `null`                           |                                               | Callback to access the Excalidraw API                     |
| isCollaborating        | `true`                           |                                               | Indicates if the component is in collaboration mode       |
| onPointerUpdate        | `null`                           |                                               | Callback triggered on pointer update                      |
| onPointerDown          | `null`                           |                                               | Callback triggered on pointer down event                  |
| onScrollChange         | `null`                           |                                               | Callback triggered on scroll change                       |
| onPaste                | `null`                           |                                               | Callback triggered on paste event                         |
| onLibraryChange        | `null`                           |                                               | Callback triggered when the library changes               |
| onLinkOpen             | `null`                           |                                               | Callback triggered when a link is opened                  |
| langCode               | `'en'`                           |                                               | The language code for localization                        |
| renderTopRightUI       | `null`                           |                                               | Function to render custom UI in the top right corner      |
| renderCustomStats      | `null`                           |                                               | Function to render custom stats                           |
| viewModeEnabled        | `false`                          |                                               | Enables view-only mode                                    |
| zenModeEnabled         | `false`                          |                                               | Enables zen mode                                          |
| gridModeEnabled        | `true`                           |                                               | Enables grid mode                                         |
| libraryReturnUrl       | `''`                             |                                               | URL to return to after using the library                  |
| theme                  | `'light'`                        | light, dark                                   | The theme of the Excalidraw component                     |
| name                   | `''`                             |                                               | Name of the drawing                                       |
| UIOptions              | `{}`                             |                                               | UI options for customizing the Excalidraw interface       |
| detectScroll           | `true`                           |                                               | Determines whether to detect scroll events                |
| handleKeyboardGlobally | `false`                          |                                               | Determines whether to handle keyboard events globally     |
| autoFocus              | `true`                           |                                               | Determines whether to auto-focus the Excalidraw component |
| generateIdForFile      | `null`                           |                                               | Function to generate ID for files                         |
| validateEmbeddable     | `true`                           | boolean, string[], RegExp, RegExp[], function | Function or value to validate embeddable content          |
| renderEmbeddable       | `null`                           |                                               | Function to render embeddable content                     |
