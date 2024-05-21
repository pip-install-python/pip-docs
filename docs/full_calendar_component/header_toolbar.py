from typing import Literal

import dash
import dash_mantine_components as dmc
from dash import *
import full_calendar_component as fcc
from datetime import datetime, date, timedelta
from dash.exceptions import PreventUpdate


component = dmc.SimpleGrid(
    cols={"base": 1, "sm": 1, "lg": 4},
    children=[
        dmc.Paper(
            html.Div(id="view-fcc-2"),
            id="intro-wrapper-fcc-2",
            style={"gridColumn": "1 / 4"},
        ),
        dmc.Stack(
            [
            dmc.MultiSelect(
                label="Left of the calendar headerToolbar",
                placeholder="Select all you like!",
                id="fcc-headerToolbar-left-muti-select",
                value=['prev','today','next'],
                data=[
                    {"value": "title", "label": "title"},
                    {"value": "prev", "label": "prev"},
                    {"value": "next", "label": "next"},
                    {"value": "prevYear", "label": "prevYear"},
                    {"value": "today", "label": "today"},
                    {"value": "dayGridMonth", "label": "dayGridMonth"},
                    {"value": "timeGridWeek", "label": "timeGridWeek"},
                    {"value": "timeGridDay", "label": "timeGridDay"},
                    {"value": "listWeek", "label": "listWeek"},
                    {"value": "dayGridWeek", "label": "dayGridWeek"},
                    {"value": "dayGridYear", "label": "dayGridYear"},
                    {"value": "multiMonthYear", "label": "multiMonthYear"},
                    {"value": "resourceTimeline", "label": "resourceTimeline"},
                    {"value": "resourceTimeGridDay", "label": "resourceTimeGridDay"}
                ],
                mb=10,
            ),
                dmc.MultiSelect(
                    label="Center of the calendar headerToolbar",
                    placeholder="Select all you like!",
                    id="fcc-headerToolbar-center-muti-select",
                    value=['title'],
                    data=[
                        {"value": "title", "label": "title"},
                        {"value": "prev", "label": "prev"},
                        {"value": "next", "label": "next"},
                        {"value": "prevYear", "label": "prevYear"},
                        {"value": "today", "label": "today"},
                        {"value": "dayGridMonth", "label": "dayGridMonth"},
                        {"value": "timeGridWeek", "label": "timeGridWeek"},
                        {"value": "timeGridDay", "label": "timeGridDay"},
                        {"value": "listWeek", "label": "listWeek"},
                        {"value": "dayGridWeek", "label": "dayGridWeek"},
                        {"value": "dayGridYear", "label": "dayGridYear"},
                        {"value": "multiMonthYear", "label": "multiMonthYear"},
                        {"value": "resourceTimeline", "label": "resourceTimeline"},
                        {"value": "resourceTimeGridDay", "label": "resourceTimeGridDay"}
                    ],
                    mb=10,
                ),
                dmc.MultiSelect(
                    label="Right of the calendar headerToolbar",
                    placeholder="Select all you like!",
                    id="fcc-headerToolbar-right-muti-select",
                    value=['timeGridDay', 'dayGridMonth', 'timeGridWeek'],
                    data=[
                        {"value": "title", "label": "title"},
                        {"value": "prev", "label": "prev"},
                        {"value": "next", "label": "next"},
                        {"value": "prevYear", "label": "prevYear"},
                        {"value": "today", "label": "today"},
                        {"value": "dayGridMonth", "label": "dayGridMonth"},
                        {"value": "timeGridWeek", "label": "timeGridWeek"},
                        {"value": "timeGridDay", "label": "timeGridDay"},
                        {"value": "listWeek", "label": "listWeek"},
                        {"value": "dayGridWeek", "label": "dayGridWeek"},
                        {"value": "dayGridYear", "label": "dayGridYear"},
                        {"value": "multiMonthYear", "label": "multiMonthYear"},
                        {"value": "resourceTimeline", "label": "resourceTimeline"},
                        {"value": "resourceTimeGridDay", "label": "resourceTimeGridDay"}
                    ],
                    mb=10,
                )
                ]
        ),

    ],
    spacing="2rem",
)

@callback(
    Output("view-fcc-2", "children"),
    # Output('test-out', 'children'),
    Input("fcc-headerToolbar-left-muti-select", "value"),
    Input("fcc-headerToolbar-center-muti-select", "value"),
    Input("fcc-headerToolbar-right-muti-select", "value"),

)
def update_form(render, render2, render3):
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
    render_value = ",".join(render)
    render2_value = ",".join(render2)
    render3_value = ",".join(render3)


    return fcc.FullCalendarComponent(
            id="view-calendar9",  # Unique ID for the component
            initialView='dayGridMonth',  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": render_value,
                "center": render2_value,
                "right": render3_value,
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=events,
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
        )