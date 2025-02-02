---
name: Full Calendar
description: Use Full Calendar Component to create a dash calendar.
endpoint: /pip/full_calendar_component
package: full_calendar_component
icon: line-md:calendar
---

.. toc::

[Visit GitHub Repo](https://github.com/pip-install-python/full_calendar_component)

### Installation

```bash
pip install full-calendar-component
```

### Introduction

This is an example of a full event calendar with all views: `listWeek`,`timeGridDay`,`timeGridWeek`,`dayGridMonth`. You can add events to your calendar with `Clicking` on a day wich will pop open a modal form for you to enter content for a new event.

.. exec::docs.full_calendar_component.introduction
    :code: false

.. sourcetabs::docs/full_calendar_component/introduction.py
    :defaultExpanded: false
    :withExpandedButton: true

### Render intialView

You have access to these views: `dayGridMonth`, `timeGridWeek`, `timeGridDay`, `listWeek`, `dayGridWeek`, `dayGridYear`, `multiMonthYear`, `resourceTimeline`, `resourceTimeGridDay`, `resourceTimeLineWeek`. You can choose to render all or some of them via passing them as options in the headerToolbar.

.. exec::docs.full_calendar_component.section_renders
    :code: false

### Header Toolbar

The Calendar header is broken into 3 parts `left`, `center`, `right`. You can customize the header by passing in the `headerToolbar` prop with the desired configuration `title`, `prev`, `next`, `prevYear`, `today` or in intialView prop `dayGridMonth`, `timeGridWeek`, `timeGridDay`, `listWeek`, `dayGridWeek`, `dayGridYear`, `multiMonthYear`, `resourceTimeline`, `resourceTimeGridDay`, `resourceTimeLineWeek`. 
.. exec::docs.full_calendar_component.header_toolbar
    :code: false

### API Example

.. exec::docs.full_calendar_component.api_example
    :code: false

### Event
Calendars can have events displayed via a list provided the events prop, which is a list of dictionaries with the following keys: `title`, `start`, `end`, `allDay`, `resourceId`, `classNames`, `display`, `extendedProps`, `id`. Start and end are datetime strings in the format `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD`. AllDay is a boolean. ResourceId is a string. ClassNames is a list of strings. Display is a string. ExtendedProps is a dictionary. Id is a string.
