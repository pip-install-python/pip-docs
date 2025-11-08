from datetime import date, datetime, time, timedelta

import dash_fullcalendar as dcal
import dash_mantine_components as dmc
import dash_quill
from dash import Input, Output, State, callback, callback_context, dcc, html, no_update
from dash.exceptions import PreventUpdate

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

quill_mods = [
    [{"header": "1"}, {"header": "2"}, {"font": []}],
    [{"size": []}],
    ["bold", "italic", "underline", "strike", "blockquote"],
    [{"list": "ordered"}, {"list": "bullet"}, {"indent": "-1"}, {"indent": "+1"}],
    ["link", "image"],
]

# Get today's date
today = datetime.now()

# Format the date
formatted_date = today.strftime("%Y-%m-%d")


def _parse_calendar_datetime(value):
    """Best-effort parser for FullCalendar ISO strings or datetime objects."""
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, time):
        return datetime.combine(datetime.now().date(), value)
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value)
    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned.endswith("Z"):
            cleaned = cleaned[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(cleaned)
        except ValueError:
            try:
                parsed = datetime.strptime(cleaned, "%Y-%m-%d")
            except ValueError:
                return None
        if parsed.tzinfo:
            return parsed.astimezone().replace(tzinfo=None)
        return parsed
    return None


def _coerce_date_value(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    parsed = _parse_calendar_datetime(value)
    if parsed:
        return parsed.date()
    if isinstance(value, str):
        stripped = value.strip()
        for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
            try:
                return datetime.strptime(stripped, fmt).date()
            except ValueError:
                continue
    return None


def _coerce_time_value(value, date_hint):
    parsed = _parse_calendar_datetime(value)
    if parsed:
        return parsed
    date_hint = date_hint or datetime.now().date()
    if isinstance(value, time):
        return datetime.combine(date_hint, value)
    if isinstance(value, str):
        stripped = value.strip()
        for fmt in ("%H:%M:%S", "%H:%M"):
            try:
                t = datetime.strptime(stripped, fmt).time()
                return datetime.combine(date_hint, t)
            except ValueError:
                continue
        try:
            parsed = datetime.fromisoformat(stripped)
            return parsed.replace(
                year=date_hint.year,
                month=date_hint.month,
                day=date_hint.day,
            )
        except ValueError:
            pass
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value)
    return None


def _extract_date_click_payload(payload):
    if not payload:
        return None, True
    if isinstance(payload, dict):
        date_value = payload.get("dateStr") or payload.get("date")
        view = payload.get("view") or {}
        view_type = view.get("type")
        all_day = payload.get("allDay")
        if all_day is None and view_type:
            all_day = view_type.startswith("dayGrid") or view_type.startswith("multiMonth")
        return date_value, bool(all_day) if all_day is not None else True
    return payload, True


def _build_modal_response(start_dt, end_dt, *, all_day):
    start_dt = start_dt or datetime.now()
    if all_day:
        if not end_dt:
            end_dt = start_dt + timedelta(days=1)
        if end_dt <= start_dt:
            end_dt = start_dt + timedelta(days=1)
        # display end date inclusive
        end_display = end_dt - timedelta(days=1) if end_dt.date() > start_dt.date() else start_dt
        return (
            True,
            start_dt.strftime("%Y-%m-%d"),
            end_display.strftime("%Y-%m-%d"),
            None,
            None,
            {"allDay": True},
        )

    end_dt = end_dt or (start_dt + timedelta(hours=1))
    if end_dt <= start_dt:
        end_dt = start_dt + timedelta(hours=1)
    return (
        True,
        start_dt.strftime("%Y-%m-%d"),
        end_dt.strftime("%Y-%m-%d"),
        start_dt.strftime("%H:%M:%S"),
        end_dt.strftime("%H:%M:%S"),
        {"allDay": False},
    )


component =  html.Div(
    [
        dcc.Store(id="new_event_selection_meta", data={"allDay": False}),
        html.Div(
            dcal.FullCalendar(
                id="calendar",  # Unique ID for the component
                initialView="dayGridMonth",  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
                # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
                headerToolbar={
                    "left": "prev,next today",
                    "center": "",
                    "right": "listWeek,timeGridDay,timeGridWeek,dayGridMonth",
                },  # Calendar header
                initialDate=f"{formatted_date}",  # Start date for calendar
                editable=True,  # Allow events to be edited
                selectable=True,  # Allow dates to be selected
                events=[],
                nowIndicator=True,  # Show current time indicator
                navLinks=True,  # Allow navigation to other dates
            ),
            className="dark-calendar",
            style=CALENDAR_STYLE,
        ),
        dmc.MantineProvider(
            theme={"colorScheme": "dark"},
            children=[
                dmc.Modal(
                    id="modal",
                    size="xl",
                    title="Event Details",
                    zIndex=10000,
                    centered=True,
                    children=[
                        html.Div(id="modal_event_display_context"),
                        dmc.Space(h=20),
                        dmc.Group(
                            [
                                dmc.Button(
                                    "Close",
                                    color="red",
                                    variant="outline",
                                    id="modal-close-button",
                                ),
                            ],
                            align="right",
                        ),
                    ],
                )
            ],
        ),
        dmc.MantineProvider(
            theme={"colorScheme": "dark"},
            children=[
                dmc.Modal(
                    id="add_modal",
                    title="New Event",
                    size="xl",
                    centered=True,
                    children=[
                        dmc.Grid(
                            children=[
                                dmc.GridCol(
                                    html.Div(
                                        dmc.DatePickerInput(
                                            id="start_date",
                                            label="Start Date",
                                            value=datetime.now().date(),
                                            styles={"width": "100%"},
                                            disabled=True,
                                        ),
                                        style={"width": "100%"},
                                    ),
                                    span=6,
                                ),
                                dmc.GridCol(
                                    html.Div(
                                        dmc.TimeInput(
                                            label="Start Time",
                                            withSeconds=True,
                                            value=datetime.now(),
                                            # format="12",
                                            id="start_time",
                                        ),
                                        style={"width": "100%"},
                                    ),
                                    span=6,
                                ),
                            ],
                            gutter="xl",
                        ),
                        dmc.Grid(
                            children=[
                                dmc.GridCol(
                                    html.Div(
                                        dmc.DatePickerInput(
                                            id="end_date",
                                            label="End Date",
                                            value=datetime.now().date(),
                                            styles={"width": "100%"},
                                        ),
                                        style={"width": "100%"},
                                    ),
                                    span=6,
                                ),
                                dmc.GridCol(
                                    html.Div(
                                        dmc.TimeInput(
                                            label="End Time",
                                            withSeconds=True,
                                            value=datetime.now(),
                                            # format="12",
                                            id="end_time",
                                        ),
                                        style={"width": "100%"},
                                    ),
                                    span=6,
                                ),
                            ],
                            gutter="xl",
                        ),
                        dmc.Grid(
                            children=[
                                dmc.GridCol(
                                    span=6,
                                    children=[
                                        dmc.TextInput(
                                            label="Event Title:",
                                            style={"width": "100%"},
                                            id="event_name_input",
                                            required=True,
                                        )
                                    ],
                                ),
                                dmc.GridCol(
                                    span=6,
                                    children=[
                                        dmc.Select(
                                            label="Select event color",
                                            placeholder="Select one",
                                            id="event_color_select",
                                            value="ng",
                                            data=[
                                                {
                                                    "value": "bg-gradient-primary",
                                                    "label": "bg-gradient-primary",
                                                },
                                                {
                                                    "value": "bg-gradient-secondary",
                                                    "label": "bg-gradient-secondary",
                                                },
                                                {
                                                    "value": "bg-gradient-success",
                                                    "label": "bg-gradient-success",
                                                },
                                                {
                                                    "value": "bg-gradient-info",
                                                    "label": "bg-gradient-info",
                                                },
                                                {
                                                    "value": "bg-gradient-warning",
                                                    "label": "bg-gradient-warning",
                                                },
                                                {
                                                    "value": "bg-gradient-danger",
                                                    "label": "bg-gradient-danger",
                                                },
                                                {
                                                    "value": "bg-gradient-light",
                                                    "label": "bg-gradient-light",
                                                },
                                                {
                                                    "value": "bg-gradient-dark",
                                                    "label": "bg-gradient-dark",
                                                },
                                                {
                                                    "value": "bg-gradient-white",
                                                    "label": "bg-gradient-white",
                                                },
                                            ],
                                            style={"width": "100%", "marginBottom": 10},
                                            required=True,
                                        )
                                    ],
                                ),
                            ]
                        ),
                        dash_quill.Quill(
                            id="rich_text_input",
                            modules={
                                "toolbar": quill_mods,
                                "clipboard": {
                                    "matchVisual": False,
                                },
                            },
                        ),
                        dmc.Accordion(
                            children=[
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl("Raw HTML"),
                                        dmc.AccordionPanel(
                                            html.Div(
                                                id="rich_text_output",
                                                style={
                                                    "height": "300px",
                                                    "overflowY": "scroll",
                                                },
                                            )
                                        ),
                                    ],
                                    value="raw_html",
                                ),
                            ],
                        ),
                        dmc.Space(h=20),
                        dmc.Group(
                            [
                                dmc.Button(
                                    "Submit",
                                    id="modal_submit_new_event_button",
                                    color="green",
                                ),
                                dmc.Button(
                                    "Close",
                                    color="red",
                                    variant="outline",
                                    id="modal_close_new_event_button",
                                ),
                            ],
                            align="right",
                        ),
                    ],
                ),
            ],
        ),
    ],
    style={"padding": "1.5rem 0"},
)


@callback(
    Output("modal", "opened"),
    Output("modal", "title"),
    Output("modal_event_display_context", "children"),
    Input("modal-close-button", "n_clicks"),
    Input("calendar", "eventClick"),
    State("modal", "opened"),
    prevent_initial_call=True  # Set this to True
)
def open_event_modal(n, event_click, opened):

    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "calendar" and event_click is not None:
        event_title = event_click.get("title", "Selected event")
        extended_props = event_click.get("extendedProps") or {}
        event_context = extended_props.get("context", "No additional details provided.")
        return (
            True,
            event_title,
            html.Div(
                dash_quill.Quill(
                    id="input3",
                    value=f"{event_context}",
                    modules={
                        "toolbar": False,
                        "clipboard": {
                            "matchVisual": False,
                        },
                    },
                ),
                style={"width": "100%", "overflowY": "auto"},
            ),
        )
    elif button_id == "modal-close-button" and n is not None:
        return False, no_update, no_update

    return opened, no_update, no_update


@callback(
    Output("add_modal", "opened"),
    Output("start_date", "value"),
    Output("end_date", "value"),
    Output("start_time", "value"),
    Output("end_time", "value"),
    Output("new_event_selection_meta", "data"),
    Input("calendar", "dateClick"),
    Input("calendar", "select"),
    Input("modal_close_new_event_button", "n_clicks"),
    State("add_modal", "opened"),
)
def open_add_modal(date_clicked, date_selected, close_clicks, opened):
    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate

    trigger = ctx.triggered[0]["prop_id"]

    if trigger == "calendar.dateClick" and date_clicked is not None:
        date_value, is_all_day = _extract_date_click_payload(date_clicked)
        start_dt = _parse_calendar_datetime(date_value) or datetime.now()
        end_dt = start_dt + (timedelta(days=1) if is_all_day else timedelta(hours=1))
        return _build_modal_response(start_dt, end_dt, all_day=is_all_day)

    if trigger == "calendar.select" and date_selected:
        selection = date_selected or {}
        start_dt = _parse_calendar_datetime(selection.get("start")) or datetime.now()
        end_dt = _parse_calendar_datetime(selection.get("end"))

        if not end_dt:
            end_dt = start_dt + timedelta(hours=1)
        is_all_day = bool(selection.get("allDay"))
        if is_all_day and end_dt <= start_dt:
            end_dt = start_dt + timedelta(days=1)
        return _build_modal_response(start_dt, end_dt, all_day=is_all_day)

    if trigger == "modal_close_new_event_button.n_clicks" and close_clicks is not None:
        return False, no_update, no_update, no_update, no_update, {"allDay": False}

    return opened, no_update, no_update, no_update, no_update, {"allDay": False}


@callback(
    Output("calendar", "events"),
    Output("add_modal", "opened", allow_duplicate=True),
    Output("event_name_input", "value"),
    Output("event_color_select", "value"),
    Output("rich_text_input", "value"),
    Input("modal_submit_new_event_button", "n_clicks"),
    State("start_date", "value"),
    State("start_time", "value"),
    State("end_date", "value"),
    State("end_time", "value"),
    State("event_name_input", "value"),
    State("event_color_select", "value"),
    State("rich_text_output", "children"),
    State("calendar", "events"),
    State("new_event_selection_meta", "data"),
    prevent_initial_call=True  # Set this to True

)
def add_new_event(
    n,
    start_date,
    start_time,
    end_date,
    end_time,
    event_name,
    event_color,
    event_context,
    current_events,
    selection_meta,
):
    if n is None:
        raise PreventUpdate

    selection_meta = selection_meta or {}
    wants_all_day = bool(selection_meta.get("allDay"))
    has_time_inputs = bool(start_time or end_time)
    use_all_day = wants_all_day and not has_time_inputs

    safe_title = event_name or "Untitled event"
    safe_color = event_color or "bg-gradient-primary"
    safe_context = event_context or ""
    events = current_events or []

    start_date_obj = _coerce_date_value(start_date) or datetime.now().date()
    end_date_obj = _coerce_date_value(end_date) or start_date_obj
    if end_date_obj < start_date_obj:
        end_date_obj = start_date_obj

    if use_all_day:
        new_event = {
            "title": safe_title,
            "start": start_date_obj.isoformat(),
            "end": (end_date_obj + timedelta(days=1)).isoformat(),
            "allDay": True,
            "className": safe_color,
            "extendedProps": {"context": safe_context},
        }
    else:
        start_dt = _coerce_time_value(start_time, start_date_obj) or datetime.combine(
            start_date_obj, datetime.min.time()
        )
        end_dt = _coerce_time_value(end_time, end_date_obj) or (start_dt + timedelta(hours=1))

        if end_dt <= start_dt:
            end_dt = start_dt + timedelta(hours=1)

        new_event = {
            "title": safe_title,
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
            "className": safe_color,
            "extendedProps": {"context": safe_context},
        }

    return events + [new_event], False, "", "bg-gradient-primary", ""


@callback(
    Output("rich_text_output", "children"),
    [Input("rich_text_input", "value")],
    [State("rich_text_input", "charCount")],
)
def display_output(value, charCount):
    return value
