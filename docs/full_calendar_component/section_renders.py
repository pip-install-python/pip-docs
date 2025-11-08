from datetime import datetime, timedelta

import dash_fullcalendar as dcal
import dash_mantine_components as dmc
from dash import Input, Output, callback, html

CALENDAR_STYLE = {
    "--fc-page-bg-color": "#101113",
    "--fc-neutral-bg-color": "#1a1b1e",
    "--fc-neutral-text-color": "#f1f3f5",
    "--fc-border-color": "#2c2e33",
    "--fc-button-text-color": "#f1f3f5",
    "--fc-button-bg-color": "#2c2e33",
    "--fc-button-border-color": "#373a40",
    "--fc-event-text-color": "#f8f9fa",
}

BASE_VIEWS = [
    ("dayGridMonth", "Monthly grid (dayGridMonth)"),
    ("timeGridWeek", "Weekly schedule (timeGridWeek)"),
    ("timeGridDay", "Single day (timeGridDay)"),
    ("listWeek", "Agenda list (listWeek)"),
    ("listDay", "Agenda day (listDay)"),
    ("multiMonthYear", "Multi-month year (multiMonthYear)"),
]

HAS_RESOURCE_API = "resources" in getattr(dcal.FullCalendar, "available_properties", [])

PREMIUM_VIEW_OPTIONS = [
    ("resourceTimelineWeek", "Resource timeline week*"),
    ("resourceTimeGridDay", "Resource time grid day*"),
]

VIEW_OPTIONS = BASE_VIEWS + (PREMIUM_VIEW_OPTIONS if HAS_RESOURCE_API else [])
PREMIUM_VIEWS = {value for value, _ in PREMIUM_VIEW_OPTIONS} if HAS_RESOURCE_API else set()

RESOURCES = [
    {"id": "room-1", "title": "Room 101"},
    {"id": "room-2", "title": "Room 202"},
    {"id": "hybrid", "title": "Remote Crew"},
]


def _build_events():
    base_day = datetime.now().date()

    def slot(title, day_offset, hour, duration, resource, color, context):
        start = datetime.combine(base_day + timedelta(days=day_offset), datetime.min.time()) + timedelta(hours=hour)
        end = start + timedelta(hours=duration)
        event = {
            "id": title.lower().replace(" ", "-"),
            "title": title,
            "start": start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%S"),
            "className": color,
            "extendedProps": {"context": context},
        }
        if resource:
            event["resourceId"] = resource
        return event

    return [
        slot("Product Kickoff", 0, 9, 1.5, "room-1", "bg-gradient-success", "Launch plan and scope review."),
        slot("Design Review", 1, 11, 1, "room-2", "bg-gradient-info", "UX polish and acceptance."),
        slot("Customer Sync", 2, 14, 1, "hybrid", "bg-gradient-warning", "Weekly touchpoint with enterprise clients."),
        slot("Deployment Window", 3, 21, 2, "room-1", "bg-gradient-danger", "Late-night release window."),
        slot("Sprint Demo", 4, 13, 1.5, "room-2", "bg-gradient-primary", "Showcase progress to stakeholders."),
    ]


component = dmc.SimpleGrid(
    cols={"base": 1, "sm": 1, "lg": 4},
    spacing="2rem",
    children=[
        dmc.Paper(
            html.Div(id="view-fcc"),
            id="intro-wrapper-fcc",
            style={"gridColumn": "1 / 4"},
            withBorder=True,
            radius="md",
            p="md",
        ),
        dmc.Stack(
            [
                dmc.RadioGroup(
                    label="Choose the initial view (premium views marked with *)",
                    id="intro-view-fcc",
                    value="dayGridMonth",
                    children=dmc.Stack(
                        [dmc.Radio(label=label, value=value) for value, label in VIEW_OPTIONS],
                        gap="0.4rem",
                    ),
                ),
                dmc.Text(
                    "Resource views load automatically when Scheduler plugins and license keys are available."
                    if HAS_RESOURCE_API
                    else "Install the latest dash-fullcalendar (Scheduler build) to try the resource views.",
                    size="sm",
                    c="dimmed",
                ),
            ]
        ),
    ],
    style={"padding": "1.5rem 0"},
)


@callback(Output("view-fcc", "children"), Input("intro-view-fcc", "value"))
def update_form(render: str):
    events = _build_events()
    calendar_id = f"view-calendar-preview-{render}"
    calendar_kwargs = {
        "id": calendar_id,
        "initialView": render,
        "initialDate": events[0]["start"].split("T")[0],
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay,listWeek,listDay,multiMonthYear",
        },
        "events": events,
        "navLinks": True,
        "weekends": True,
        "nowIndicator": True,
        "height": "750px",
    }

    if render in PREMIUM_VIEWS and HAS_RESOURCE_API:
        calendar_kwargs.update(
            {
                "schedulerLicenseKey": "GPL-My-Project-Is-Open-Source",
                "plugins": ["resourceTimeline", "resourceTimeGrid", "resource"],
                "resources": RESOURCES,
            }
        )

    return html.Div(
        dcal.FullCalendar(**calendar_kwargs),
        className="dark-calendar",
        style=CALENDAR_STYLE,
    )
