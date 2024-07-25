import full_calendar_component as fcc
from dash import *
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from datetime import datetime, date, timedelta
from data import api
import dash_dangerously_set_inner_html

# Get today's date
today = datetime.now()

# Format the date
formatted_date = today.strftime("%Y-%m-%d")

events = api.get_events_by_category("plotly")


component = html.Div([
        dmc.MantineProvider(
            theme={"colorScheme": "dark"},
            children=[
                dmc.Modal(
                    id="api_event_modal",
                    size="xl",
                    title="Event Details",
                    zIndex=10000,
                    centered=True,
                    children=[
                        html.Div(id="api_event_modal_display_context"),
                        dmc.Space(h=20),
                        dmc.Group(
                            [
                                dmc.Button(
                                    "Close",
                                    color="red",
                                    variant="outline",
                                    id="api_event_modal_close_button",
                                ),
                            ],
                            align="right",
                        ),
                    ],
                )
            ],
        ),
        fcc.FullCalendarComponent(
            id="api_calendar",  # Unique ID for the component
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
    ]
)

@callback(
    Output("api_event_modal", "opened"),
    Output("api_event_modal", "title"),
    Output("api_event_modal_display_context", "children"),
    Input("api_event_modal_close_button", "n_clicks"),
    Input("api_calendar", "clickedEvent"),
    State("api_event_modal", "opened"),
    prevent_initial_call=True  # Set this to True
)
def open__api_event_modal(n, clickedEvent, opened):

    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "api_calendar" and clickedEvent is not None:
        event_title = clickedEvent["title"]
        event_context = clickedEvent["extendedProps"]["context"]

        return (
            True,
            event_title,
            html.Div(
            dash_dangerously_set_inner_html.DangerouslySetInnerHTML(f'''
                {event_context}
                '''),
                style={"width": "100%", "overflowY": "auto"},
            ),
        )
    elif button_id == "modal-close-button" and n is not None:
        return False, dash.no_update, dash.no_update

    return opened, dash.no_update, dash.no_update