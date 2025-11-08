---
name: Full Calendar
description: Use Dash FullCalendar to embed the entire FullCalendar surface inside Dash.
endpoint: /pip/full_calendar_component
package: dash-fullcalendar
icon: line-md:calendar
---

.. toc::

[Visit GitHub Repo](https://github.com/pip-install-python/dash-fullcalendar)

### Installation

```bash
pip install dash-fullcalendar
```

### Introduction

`dash-fullcalendar` is a thin wrapper around `@fullcalendar/react`, so every prop and callback you see in the FullCalendar docs is available in Dash. The example below recreates the classic "click to add" workflow with modals, rich text notes, and event details powered by `eventClick`/`dateClick`.

.. exec::docs.full_calendar_component.introduction
    :code: false

.. sourcetabs::docs/full_calendar_component/introduction.py
    :defaultExpanded: false
    :withExpandedButton: true

### Views & Layouts

Switch between grid, list, multi-month, and Scheduler views by changing `initialView` (or calling the client-side API). Resource timelines automatically load when a Scheduler key plus premium plugins are supplied.

.. exec::docs.full_calendar_component.section_renders
    :code: false

.. sourcetabs::docs/full_calendar_component/section_renders.py
    :defaultExpanded: false
    :withExpandedButton: true

.. admonition:: Premium Scheduler plugins
    :icon: mdi:star-four-points
    :color: yellow

    Timeline and resource views require FullCalendar Scheduler. Use your commercial key or the open-source key (`GPL-My-Project-Is-Open-Source`) together with `plugins=["resourceTimeline","resourceTimeGrid","resource"]`.

### Header Toolbar & Buttons

FullCalendar's header is just a config object. Populate the `left`, `center`, and `right` slots with navigation controls, view buttons, or even custom buttons returned from Dash callbacks via the `command` prop.

.. exec::docs.full_calendar_component.header_toolbar
    :code: false

.. sourcetabs::docs/full_calendar_component/header_toolbar.py
    :defaultExpanded: false
    :withExpandedButton: true

### Interactive Workflows

The advanced example wires every bi-directional callback: `dateClick`, `select`, `eventDrop`, `eventResize`, `eventClick`, and programmatic navigation through the `command` prop. Switches update `weekends`, `businessHours`, `editable`, and `selectable` live.

.. exec::docs.full_calendar_component.extra_fields
    :code: false

.. sourcetabs::docs/full_calendar_component/extra_fields.py
    :defaultExpanded: false
    :withExpandedButton: true

### Remote Data & API Feeds

Events can arrive from REST, databases, or sockets. Feed a list of dictionaries to the `events` prop, or point `eventSources` to URLs. This example pulls events from a JSON API (and falls back to sample data when offline); click any event to open a Mantine modal showing the extended metadata returned via `eventClick`.

.. exec::docs.full_calendar_component.api_example
    :code: false

.. sourcetabs::docs/full_calendar_component/api_example.py
    :defaultExpanded: false
    :withExpandedButton: true

### Event payloads & callback hooks

Events supplied to `dash_fullcalendar.FullCalendar` mirror the upstream schema:

- Required keys: `title`, `start`, optionally `end` (ISO strings), `allDay` (bool) when appropriate.
- Presentation: `className`/`classNames`, `display`, `resourceId`, `color`, `extendedProps` for any custom metadata.
- Interaction payloads:  
  - `dateClick` → an ISO datetime string of the clicked cell.  
  - `select` → `{"start": str, "end": str, "allDay": bool}`.  
  - `eventClick` → `{"title", "start", "end", "allDay", "extendedProps": {...}}`.  
  - `eventDrop`/`eventResize` → objects containing the new `event`, the `oldEvent`, and `delta`/`relatedEvents`.  
  - `command` → pass dictionaries such as `{"type": "next"}` or `{"type": "changeView", "view": "timeGridWeek"}` to drive the client API from Dash.

Build custom forms, dashboards, or schedulers by combining these props with Dash callbacks—everything displayed above is powered by standard Dash patterns plus the new `dash-fullcalendar` component.
