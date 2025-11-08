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

BASE_HEADER_CHOICES = [
    {"value": "title", "label": "Title"},
    {"value": "prev", "label": "Prev"},
    {"value": "next", "label": "Next"},
    {"value": "prevYear", "label": "Prev Year"},
    {"value": "today", "label": "Today"},
    {"value": "dayGridMonth", "label": "dayGridMonth"},
    {"value": "timeGridWeek", "label": "timeGridWeek"},
    {"value": "timeGridDay", "label": "timeGridDay"},
    {"value": "listWeek", "label": "listWeek"},
    {"value": "listDay", "label": "listDay"},
    {"value": "multiMonthYear", "label": "multiMonthYear"},
]

HAS_RESOURCE_API = "resources" in getattr(dcal.FullCalendar, "available_properties", [])

PREMIUM_CHOICES = [
    {"value": "resourceTimelineWeek", "label": "resourceTimelineWeek*"},
    {"value": "resourceTimeGridDay", "label": "resourceTimeGridDay*"},
]

HEADER_CHOICES = BASE_HEADER_CHOICES + (PREMIUM_CHOICES if HAS_RESOURCE_API else [])
PREMIUM_KEYS = {choice["value"] for choice in PREMIUM_CHOICES} if HAS_RESOURCE_API else set()

RESOURCES = [
    {"id": "room-1", "title": "Room 101"},
    {"id": "room-2", "title": "Room 202"},
    {"id": "hybrid", "title": "Remote Crew"},
]


def _demo_events():
    base_day = datetime.now().date()

    def block(title, day_offset, hour, duration, resource, color, context):
        start = datetime.combine(base_day + timedelta(days=day_offset), datetime.min.time()) + timedelta(hours=hour)
        end = start + timedelta(hours=duration)
        event = {
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
        block("Roadmap sync", 0, 10, 1.5, "room-1", "bg-gradient-success", "Company-wide goals alignment."),
        block("Design pairing", 1, 13, 1, "room-2", "bg-gradient-info", "Working session with design."),
        block("Support rotation", 1, 16, 2, "hybrid", "bg-gradient-warning", "Handling premium support tickets."),
        block("Deploy", 3, 21, 1.5, "room-1", "bg-gradient-danger", "Nightly deployment window."),
    ]


component = dmc.SimpleGrid(
    cols={"base": 1, "sm": 1, "lg": 4},
    spacing="2rem",
    children=[
        dmc.Paper(
            html.Div(id="view-fcc-2"),
            id="intro-wrapper-fcc-2",
            style={"gridColumn": "1 / 4"},
            withBorder=True,
            radius="md",
            p="md",
        ),
        dmc.Stack(
            [
                dmc.MultiSelect(
                    label="Left of the headerToolbar",
                    placeholder="Pick buttons",
                    id="fcc-headerToolbar-left-muti-select",
                    value=["prev", "today", "next"],
                    data=HEADER_CHOICES,
                    mb=10,
                ),
                dmc.MultiSelect(
                    label="Center of the headerToolbar",
                    placeholder="Pick buttons",
                    id="fcc-headerToolbar-center-muti-select",
                    value=["title"],
                    data=HEADER_CHOICES,
                    mb=10,
                ),
                dmc.MultiSelect(
                    label="Right of the headerToolbar",
                    placeholder="Pick buttons",
                    id="fcc-headerToolbar-right-muti-select",
                    value=["dayGridMonth", "timeGridWeek", "timeGridDay", "listWeek"],
                    data=HEADER_CHOICES,
                    mb=10,
                ),
                dmc.Text(
                    "Buttons marked with * require Scheduler plugins and a license key."
                    if HAS_RESOURCE_API
                    else "Install the Scheduler build of dash-fullcalendar to unlock resource buttons (*).",
                    size="sm",
                    c="dimmed",
                ),
            ]
        ),
    ],
    style={"padding": "1.5rem 0"},
)


@callback(
    Output("view-fcc-2", "children"),
    Input("fcc-headerToolbar-left-muti-select", "value"),
    Input("fcc-headerToolbar-center-muti-select", "value"),
    Input("fcc-headerToolbar-right-muti-select", "value"),
)
def update_form(left_buttons, center_buttons, right_buttons):
    left = ",".join(left_buttons) if left_buttons else ""
    center = ",".join(center_buttons) if center_buttons else ""
    right = ",".join(right_buttons) if right_buttons else ""

    events = _demo_events()
    calendar_kwargs = {
        "id": "view-calendar-toolbar",
        "initialView": "dayGridMonth",
        "initialDate": events[0]["start"].split("T")[0],
        "headerToolbar": {"left": left, "center": center, "right": right},
        "events": events,
        "editable": True,
        "selectable": True,
        "navLinks": True,
        "nowIndicator": True,
        "height": "650px",
    }

    selected = set(left_buttons + center_buttons + right_buttons)
    if HAS_RESOURCE_API and (selected & PREMIUM_KEYS):
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
