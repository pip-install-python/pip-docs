from typing import Literal

import dash
import dash_mantine_components as dmc
from dash import *
import full_calendar_component as fcc
from datetime import datetime, date, timedelta
from dash.exceptions import PreventUpdate


component = dmc.SimpleGrid(
    [
        dmc.Paper(
            html.Div(id="view-fcc"),
            id="intro-wrapper-fcc",
            style={"gridColumn": "1 / 4"},
        ),
        dmc.Stack(
            [
                dmc.RadioGroup(
                    label="initialView render",
                    id="intro-view-fcc",
                    value="dayGridMonth",  # Set the default value to text-1
                    children=dmc.Stack(
                        [dmc.Radio(label=x, value=x) for x in ["dayGridMonth", "timeGridWeek", "timeGridDay", "listWeek", "dayGridWeek", "dayGridYear", "multiMonthYear", "resourceTimeline", "resourceTimeGridDay"]],
                        gap="0.5rem",
                    ),
                ),
                html.H1(id='test-out')
            ],
        ),
    ],
    cols=4,
    spacing="2rem",
)
@callback(
    Output("view-fcc", "children"),
    # Output('test-out', 'children'),
    Input("intro-view-fcc", "value"),

)
def update_form(render: str):
    # Get today's date
    today = datetime.now()

    # Format the date
    formatted_date = today.strftime("%Y-%m-%d")

    events = [
        {
            "title": "Pip Install Python",
            "start": f"{formatted_date}",
            "end": f"{formatted_date}",
            "className": "bg-gradient-success",
            "context": "Pip Install FullCalendar",
        },
        {
            'title': 'Meeting with the boss',
            'start': f"{formatted_date}T14:30:00",
            'end': f"{formatted_date}T15:30:00",
            'className': 'bg-gradient-info',
            'context': 'Meeting with the boss',
        },
        {
            'title': 'Happy Hour',
            'start': f"{formatted_date}T17:30:00",
            'end': f"{formatted_date}T18:30:00",
            'className': 'bg-gradient-warning',
            'context': 'Happy Hour',
        },
        {
            'title': 'Dinner',
            'start': f"{formatted_date}T20:00:00",
            'end': f"{formatted_date}T21:00:00",
            'className': 'bg-gradient-danger',
            'context': 'Dinner',
        }
    ]
    if render == 'dayGridMonth':
        return fcc.FullCalendarComponent(
            id="view-calendar1",  # Unique ID for the component
            initialView='dayGridMonth',  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": "prev,next today",
                "center": "",
                "right": "",
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=events,
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
        )
    elif render == 'timeGridWeek':
        return fcc.FullCalendarComponent(
            id="view-calendar2",  # Unique ID for the component
            initialView='timeGridWeek',  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": "prev,next today",
                "center": "",
                "right": "",
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=events,
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
        )
    elif render == 'timeGridDay':
        return fcc.FullCalendarComponent(
            id="view-calendar3",  # Unique ID for the component
            initialView='timeGridDay',  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": "prev,next today",
                "center": "",
                "right": "",
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=events,
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
        )
    elif render == 'listWeek':
        return fcc.FullCalendarComponent(
            id="view-calendar4",  # Unique ID for the component
            initialView='listWeek',  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": "prev,next today",
                "center": "",
                "right": "",
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=events,
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
        )
    elif render == 'dayGridWeek':
        return fcc.FullCalendarComponent(
            id="view-calendar5",  # Unique ID for the component
            initialView='dayGridWeek',  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": "prev,next today",
                "center": "",
                "right": "",
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=events,
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
        )
    elif render == 'dayGridYear':
        return fcc.FullCalendarComponent(
            id="view-calendar6",  # Unique ID for the component
            initialView='dayGridYear',  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": "prev,next today",
                "center": "",
                "right": "",
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=events,
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
        )
    elif render == 'multiMonthYear':
        return fcc.FullCalendarComponent(
            id="view-calendar7",  # Unique ID for the component
            initialView='multiMonthYear',  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": "prev,next today",
                "center": "",
                "right": "",
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=events,
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
        )
    elif render == 'resourceTimeline':
        return fcc.FullCalendarComponent(
            id="view-calendar8",  # Unique ID for the component
            initialView='resourceTimeline',  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": "prev,next today",
                "center": "",
                "right": "",
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=events,
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
        )
    elif render == 'resourceTimeGridDay':
        return fcc.FullCalendarComponent(
            id="view-calendar9",  # Unique ID for the component
            initialView='resourceTimeGridDay',  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": "prev,next today",
                "center": "",
                "right": "",
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=events,
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
        )
    return fcc.FullCalendarComponent(
        id="view-calendar",  # Unique ID for the component
        initialView=f"{render}",  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
        # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
        headerToolbar={
            "left": "prev,next today",
            "center": "",
            "right": "",
        },  # Calendar header
        initialDate=f"{formatted_date}",  # Start date for calendar
        editable=True,  # Allow events to be edited
        selectable=True,  # Allow dates to be selected
        events=events,
        nowIndicator=True,  # Show current time indicator
        navLinks=True,  # Allow navigation to other dates
    )