---
name: Dash Summernote
description: Rich text editor summernote for dash.
endpoint: /pip/dash_summernote
package: dash_summernote
icon: line-md:text-box-multiple
---

.. toc::

[Visit GitHub Repo](https://github.com/pip-install-python/dash_summernote)

### Installation

```bash
pip install dash-summernote
```

### Introduction

This is an example of a rich text editor summernote component. You can add text to your summernote and see the response of the content.

.. exec::docs.dash_summernote.introduction

### toolbar

The toolbar is a prop in DashSummernote that allows you to add a toolbar to the editor. You can add a `style`, `font`, `fontname`, `fontsize`, `color`, `para`, `height`, `table`, `insert`, `view`, `help` toolbar to the editor. Can either be a string with a single toolbar or a selection of toolbars in a list.
You can compose a toolbar with pre-shipped buttons.

Insert
* `picture`: open image dialog
* `link`: open link dialog
* `video`: open video dialog
* `table`: insert a table
* `hr`: insert a horizontal rule

Font Style
* `fontname`: set font family
* `fontsize`: set font size
* `fontsizeunit`: set font size unit
* `color`: set foreground and background color
* `forecolor`: set foreground color
* `backcolor`: set background color
* `bold`: toggle font weight
* `italic`: toggle italic
* `underline`: toggle underline
* `strikethrough`: toggle strikethrough
* `superscript`: toggle superscript
* `subscript`: toggle subscript
* `clear`: clear font style

Paragraph style
* `style`: format selected block
* `ol`: toggle ordered list
* `ul`: toggle unordered list
* `paragraph`: dropdown for paragraph align
* `height`: set line height

Misc
* `fullscreen`: toggle fullscreen editing mode
* `codeview`: toggle wysiwyg and html editing mode
* `undo`: undo
* `redo`: redo
* `help`: open help dialog

### bugs

* Upload images doesn't work but upload image url does.

