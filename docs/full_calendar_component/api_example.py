import re
from datetime import datetime, timedelta
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlparse

import dash_fullcalendar as dcal
from dash import Input, Output, State, callback, callback_context, dcc, html, no_update
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from data import api

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

CARD_STYLE = {
    "backgroundColor": "var(--mantine-color-dark-6)",
    "border": "1px solid var(--mantine-color-dark-4)",
    "color": "var(--mantine-color-gray-0)",
}

FIELDSET_STYLES = {
    "root": {
        **CARD_STYLE,
        "borderRadius": "var(--mantine-radius-md)",
        "padding": "var(--mantine-spacing-lg)",
    },
}

CATEGORY_OPTIONS = [
    {"value": "plotly", "label": "Plotly"},
    {"value": "dash", "label": "Dash"},
    {"value": "python", "label": "Python"},
]

VIEW_OPTIONS = [
    {"label": "Month", "value": "dayGridMonth"},
    {"label": "Week", "value": "timeGridWeek"},
    {"label": "Day", "value": "timeGridDay"},
    {"label": "List", "value": "listWeek"},
]

DEFAULT_CONTEXT_PLACEHOLDER = "No description provided."
SAFE_PROTOCOLS = {"http", "https", "mailto", "tel", ""}
TAG_REGEX = re.compile(r"<[^>]+>")


class _SafeHTMLToMarkdown(HTMLParser):
    """Convert limited HTML snippets into Markdown while stripping unsafe markup."""

    _BLOCK_TAGS = {
        "p",
        "div",
        "section",
        "article",
        "header",
        "footer",
    }
    _SKIP_TAGS = {"script", "style"}
    _BOLD_TAGS = {"strong", "b"}
    _ITALIC_TAGS = {"em", "i"}
    _CODE_TAGS = {"code", "kbd", "samp"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.fragments = []
        self.anchor_stack = []
        self.list_stack = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in self._SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return

        if tag == "br":
            self.fragments.append("  \n")
        elif tag in self._BOLD_TAGS:
            self.fragments.append("**")
        elif tag in self._ITALIC_TAGS:
            self.fragments.append("*")
        elif tag in self._CODE_TAGS:
            self.fragments.append("`")
        elif tag == "a":
            href = ""
            for attr, value in attrs:
                if attr.lower() == "href":
                    href = _sanitize_href(value)
                    break
            self.anchor_stack.append(href)
            self.fragments.append("[")
        elif tag == "ul":
            self.list_stack.append({"ordered": False, "count": 0})
        elif tag == "ol":
            self.list_stack.append({"ordered": True, "count": 0})
        elif tag == "li":
            if not self.list_stack:
                self.list_stack.append({"ordered": False, "count": 0})
            entry = self.list_stack[-1]
            entry["count"] += 1
            bullet = f"{entry['count']}." if entry["ordered"] else "-"
            indent = "  " * (len(self.list_stack) - 1)
            if not self.fragments or not self.fragments[-1].endswith("\n"):
                self.fragments.append("\n")
            self.fragments.append(f"{indent}{bullet} ")
        elif tag in self._BLOCK_TAGS:
            if self.fragments and not self.fragments[-1].endswith("\n\n"):
                if not self.fragments[-1].endswith("\n"):
                    self.fragments.append("\n")
                if not self.fragments[-1].endswith("\n\n"):
                    self.fragments.append("\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self._SKIP_TAGS:
            if self.skip_depth:
                self.skip_depth -= 1
            return
        if self.skip_depth:
            return

        if tag in self._BOLD_TAGS:
            self.fragments.append("**")
        elif tag in self._ITALIC_TAGS:
            self.fragments.append("*")
        elif tag in self._CODE_TAGS:
            self.fragments.append("`")
        elif tag == "a":
            href = self.anchor_stack.pop() if self.anchor_stack else ""
            if href:
                self.fragments.append(f"]({href})")
            else:
                self.fragments.append("]")
        elif tag == "li":
            if not self.fragments or not self.fragments[-1].endswith("\n"):
                self.fragments.append("\n")
        elif tag in {"ul", "ol"}:
            if self.list_stack:
                self.list_stack.pop()
            if not self.fragments or not self.fragments[-1].endswith("\n"):
                self.fragments.append("\n")
        elif tag in self._BLOCK_TAGS:
            if not self.fragments or not self.fragments[-1].endswith("\n"):
                self.fragments.append("\n")
            if not self.fragments[-1].endswith("\n\n"):
                self.fragments.append("\n")

    def handle_data(self, data):
        if self.skip_depth or not data:
            return
        normalized = data.replace("\xa0", " ")
        if not normalized.strip():
            if self.fragments and not self.fragments[-1].endswith((" ", "\n")):
                self.fragments.append(" ")
            return
        normalized = re.sub(r"\s+", " ", normalized)
        self.fragments.append(normalized)

    def get_value(self):
        text = "".join(self.fragments)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def _sanitize_href(value):
    if not value:
        return ""
    candidate = value.strip()
    if not candidate:
        return ""
    if candidate.lower().startswith("javascript:"):
        return ""
    try:
        parsed = urlparse(candidate)
    except ValueError:
        return ""
    scheme = (parsed.scheme or "").lower()
    if scheme and scheme not in SAFE_PROTOCOLS:
        return ""
    return candidate


def _strip_tags(value):
    if not value:
        return ""
    without_tags = TAG_REGEX.sub(" ", value)
    without_tags = unescape(without_tags)
    without_tags = re.sub(r"\s+", " ", without_tags)
    return without_tags.strip()


def _to_markdown(value):
    if not value:
        return DEFAULT_CONTEXT_PLACEHOLDER
    parser = _SafeHTMLToMarkdown()
    try:
        parser.feed(str(value))
        parser.close()
    except Exception:
        cleaned = _strip_tags(str(value))
        return cleaned or DEFAULT_CONTEXT_PLACEHOLDER

    cleaned = parser.get_value()
    if cleaned:
        return cleaned
    cleaned = _strip_tags(str(value))
    return cleaned or DEFAULT_CONTEXT_PLACEHOLDER


def _render_description(markdown_text, *, style=None):
    return dcc.Markdown(markdown_text, style=style or {}, link_target="_blank")


def _load_events(categories):
    categories = categories or ["plotly"]
    combined = []
    for cat in categories:
        dataset = api.get_events_by_category(cat) or []
        for idx, event in enumerate(dataset):
            normalized = {
                "title": event.get("title") or f"{cat.title()} event",
                "start": event.get("start"),
                "end": event.get("end"),
                "allDay": event.get("allDay", False),
                "className": event.get("className", "bg-gradient-primary"),
                "extendedProps": {**event.get("extendedProps", {}), "category": cat.title()},
                "id": event.get("id") or f"{cat}-{idx}",
            }
            combined.append(normalized)
    combined.sort(key=lambda e: e.get("start") or "")
    return _normalize_event_dates(combined)


def _normalize_event_dates(events):
    if not events:
        return events

    today = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    normalized = []
    for idx, event in enumerate(events):
        start_iso = event.get("start")
        end_iso = event.get("end")

        target_day = today + timedelta(days=idx)

        def parse_iso(value):
            if not value:
                return None
            try:
                cleaned = value.replace("Z", "")
                return datetime.fromisoformat(cleaned)
            except ValueError:
                return None

        start_dt = parse_iso(start_iso)
        end_dt = parse_iso(end_iso)

        if start_dt:
            new_start = datetime.combine(target_day.date(), start_dt.time())
        else:
            new_start = target_day

        if end_dt:
            duration = end_dt - start_dt if start_dt else timedelta(hours=1)
            new_end = new_start + duration
        else:
            new_end = new_start + timedelta(hours=1)

        event = {**event, "start": new_start.isoformat(), "end": new_end.isoformat()}
        normalized.append(event)

    return normalized


formatted_date = datetime.now().strftime("%Y-%m-%d")
initial_events = _load_events(["plotly"])


component = html.Div(
    [
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
        dmc.Stack(
            [
                dmc.Fieldset(
                    legend="API Controls",
                    styles=FIELDSET_STYLES,
                    children=[
                        dmc.MultiSelect(
                            label="Categories",
                            id="api_category_select",
                            data=CATEGORY_OPTIONS,
                            value=["plotly"],
                            clearable=False,
                        ),
                        dmc.Group(
                            [
                                dmc.SegmentedControl(
                                    id="api_view_control",
                                    data=VIEW_OPTIONS,
                                    value="dayGridMonth",
                                    color="indigo",
                                ),
                                dmc.Button(
                                    "Refresh events",
                                    id="api_refresh_button",
                                    variant="outline",
                                ),
                            ],
                            justify="space-between",
                        ),
                        dmc.Group(
                            [
                                dmc.Switch(label="Show weekends", id="api_toggle_weekends", checked=True, color="indigo"),
                                dmc.Switch(label="Enable nav links", id="api_toggle_navlinks", checked=True, color="indigo"),
                                dmc.Switch(label="Allow selection", id="api_toggle_selectable", checked=True, color="indigo"),
                            ],
                            justify="flex-start",
                        ),
                    ],
                ),
                dmc.Alert(
                    "Select different data categories, change views, or toggle interactions to see how dash-fullcalendar reacts to API-fed data.",
                    color="indigo",
                    variant="light",
                    radius="md",
                ),
                dmc.Flex(
                    [
                        dmc.Paper(
                            html.Div(
                                dcal.FullCalendar(
                                    id="api_calendar",
                                    initialView="dayGridMonth",
                                    headerToolbar={"left": "prev,next today", "center": "", "right": ""},
                                    initialDate=formatted_date,
                                    editable=True,
                                    selectable=True,
                                    events=initial_events,
                                    nowIndicator=True,
                                    navLinks=True,
                                ),
                                className="dark-calendar",
                                style=CALENDAR_STYLE,
                            ),
                            radius="md",
                            withBorder=True,
                            p="md",
                            style={**CARD_STYLE, "flex": 2},
                        ),
                        dmc.Paper(
                            dmc.Stack(
                                [
                                    dmc.Badge(f"{len(initial_events)} events loaded", id="api_event_count_badge"),
                                    dmc.ScrollArea(
                                        html.Div(id="api_event_summary"),
                                        h=320,
                                    ),
                                    dmc.Divider(label="Last clicked event"),
                                    html.Div(
                                        "Click an event on the calendar to preview its details here.",
                                        id="api_event_preview",
                                        style={"minHeight": "80px"},
                                    ),
                                ],
                                gap="md",
                            ),
                            radius="md",
                            withBorder=True,
                            p="md",
                            style={**CARD_STYLE, "flex": 1},
                        ),
                    ],
                    gap="1.5rem",
                    direction={"base": "column", "lg": "row"},
                    style={"width": "100%"},
                ),
            ],
            gap="md",
        ),
    ],
    style={"padding": "1.5rem 0"},
)


@callback(
    Output("api_calendar", "events"),
    Output("api_event_summary", "children"),
    Output("api_event_count_badge", "children"),
    Input("api_category_select", "value"),
    Input("api_refresh_button", "n_clicks"),
    prevent_initial_call=False,
)
def update_api_events(categories, _):
    events = _load_events(categories)
    summary_children = []
    for event in events[:15]:
        summary_children.append(
            dmc.Paper(
                dmc.Group(
                    [
                        dmc.Stack(
                            [
                                dmc.Text(event["title"], fw=600),
                                dmc.Text(
                                    f"{event.get('start', '')} → {event.get('end', 'open')}",
                                    size="sm",
                                    c="dimmed",
                                ),
                            ],
                            gap=2,
                        ),
                        dmc.Badge(event["extendedProps"].get("category", ""), color="violet", variant="light"),
                    ],
                    justify="space-between",
                ),
                withBorder=True,
                radius="md",
                p="sm",
            )
        )
    summary = (
        dmc.Stack(summary_children, gap="sm")
        if summary_children
        else dmc.Text("No events returned from the API.", c="dimmed")
    )
    badge_text = f"{len(events)} events loaded"
    return events, summary, badge_text


@callback(
    Output("api_calendar", "weekends"),
    Output("api_calendar", "navLinks"),
    Output("api_calendar", "selectable"),
    Input("api_toggle_weekends", "checked"),
    Input("api_toggle_navlinks", "checked"),
    Input("api_toggle_selectable", "checked"),
)
def toggle_calendar_behavior(weekends, nav_links, selectable):
    return bool(weekends), bool(nav_links), bool(selectable)


@callback(
    Output("api_calendar", "command"),
    Input("api_view_control", "value"),
)
def change_view(view_value):
    if not view_value:
        return no_update
    return {"type": "changeView", "view": view_value}


@callback(
    Output("api_event_modal", "opened"),
    Output("api_event_modal", "title"),
    Output("api_event_modal_display_context", "children"),
    Output("api_event_preview", "children"),
    Input("api_event_modal_close_button", "n_clicks"),
    Input("api_calendar", "eventClick"),
    State("api_event_modal", "opened"),
    prevent_initial_call=True,
)
def open__api_event_modal(n, event_click, opened):
    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "api_calendar" and event_click is not None:
        event_title = event_click.get("title", "Selected event")
        extended_props = event_click.get("extendedProps") or {}
        event_context = extended_props.get("context", DEFAULT_CONTEXT_PLACEHOLDER)
        category = extended_props.get("category", "API")
        safe_description = _to_markdown(event_context or "")
        preview = dmc.Stack(
            [
                dmc.Text(event_title, fw=600),
                dmc.Text(f"Category: {category}", size="sm", c="dimmed"),
                _render_description(safe_description, style={"fontSize": "0.9rem"}),
            ],
            gap=4,
        )

        return (
            True,
            event_title,
            _render_description(safe_description),
            preview,
        )
    if button_id == "api_event_modal_close_button" and n is not None:
        return False, no_update, no_update, no_update

    return opened, no_update, no_update, no_update
