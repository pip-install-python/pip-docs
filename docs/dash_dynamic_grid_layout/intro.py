from dash import *
import dash_dynamic_grid_layout as dgl
from dash.dependencies import Input, Output
import plotly.express as px
import dash_leaflet as dl
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash.exceptions import PreventUpdate
from datetime import datetime
import json
import random
import string
import full_calendar_component as fcc

# Sample data for the graph
df = px.data.iris()

today = datetime.now()
# Format the date
formatted_date = today.strftime("%Y-%m-%d")

# Create a Random String ID for the new component
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


component = html.Div(
    [
        html.Center(html.H4("json.dumps(current_layout)")),
        html.Hr(),
        html.Div(children=[], id="layout-output"),
        html.Hr(),
        dmc.Group([
            html.H4("Add items or edit the layout ->"),
            dmc.Menu(
                [
                    dmc.MenuTarget(
                        dmc.ActionIcon(
                            DashIconify(icon="icon-park:add-web", width=20),
                            size="lg",
                            color="#fff",
                            variant="filled",
                            id="action-icon",
                            n_clicks=0,
                            mb=8,
                            style={"backgroundColor": "#fff"},
                        )
                    ),
                    dmc.MenuDropdown(
                        [
                            dmc.MenuItem(
                                "Add Dynamic Component",
                                id="add-dynamic-component",
                                n_clicks=0,
                            ),
                            dmc.MenuItem(
                                "Edit Dynamic Layout", id="edit-mode", n_clicks=0
                            ),
                        ]
                    ),
                ],
                transitionProps={
                    "transition": "rotate-right",
                    "duration": 150,
                },
                position="right",
            ),
        ]),
        html.Div(
            dgl.DashGridLayout(
                id="grid-layout",
                items=[
                    dgl.DraggableWrapper(
                        children=[
                            dl.Map(
                                dl.TileLayer(),
                                center=[56, 10],
                                zoom=6,
                                style={
                                    "height": "100vh",
                                    "width": "100vw",
                                },
                            ),
                        ],
                        id="draggable-map",
                        handleBackground="rgb(85,85,85)",
                    ),
                    dgl.DraggableWrapper(
                        html.Img(
                            src="https://picsum.photos/200/300",
                            style={
                                "width": "100%",
                                "height": "100%",
                                "objectFit": "cover",
                            },
                        ),
                        id="draggable-image",
                    ),
                    dgl.DraggableWrapper(
                        dcc.Graph(
                            id="example-graph",
                            figure=px.scatter(
                                df,
                                x="sepal_width",
                                y="sepal_length",
                                color="species",
                            ),
                            style={"height": "100%"},
                        ),
                        id="draggable-graph",
                    ),
                    dgl.DraggableWrapper(
                        dmc.ColorPicker(
                            id="qr-color-picker",
                            format="rgba",
                            value="rgba(0, 0, 0, 1)",
                            fullWidth=True,
                        ),
                        id="draggable-color-picker",
                    ),
                    dgl.DraggableWrapper(
                        fcc.FullCalendarComponent(
                            id="api_calendar",
                            initialView='dayGridMonth',
                            headerToolbar={
                                "left": "prev,next today",
                                "center": "",
                                "right": "",
                            },
                            initialDate=f"{formatted_date}",
                            editable=True,
                            selectable=True,
                            events=[],
                            nowIndicator=True,
                            navLinks=True,
                        ),
                        id="draggable-calendar"
                    ),
                ],
                itemLayout=[
                    {'i': 'draggable-image', 'x': 0, 'y': 0, 'w': 2, 'h': 2},
                    {'i': 'draggable-color-picker', 'x': 0, 'y': 2, 'w': 3, 'h': 2},
                    {'i': 'draggable-graph', 'x': 0, 'y': 4, 'w': 6, 'h': 4},
                    {'i': 'draggable-map', 'x': 6, 'y': 0, 'w': 6, 'h': 4},
                    {'i': 'draggable-calendar', 'x': 6, 'y': 4, 'w': 6, 'h': 4}
                ],
                showRemoveButton=False,
                showResizeHandles=False,
                rowHeight=150,
                cols={"lg": 12, "md": 10, "sm": 6, "xs": 4, "xxs": 2},
                style={"height": "800px"},
                compactType="horizontal",
                persistence=True,
            ),
            className="grid-container"
        ),
        dcc.Store(id="layout-store"),
    ],
    className="main-container"
)


@callback(Output("layout-store", "data"), Input("grid-layout", "currentLayout"))
def store_layout(current_layout):
    return current_layout


@callback(
    Output("grid-layout", "showRemoveButton"),
    Output("grid-layout", "showResizeHandles"),
    Output("draggable-map", "handleBackground"),
    Input("edit-mode", "n_clicks"),
    State("grid-layout", "showRemoveButton"),
    State("grid-layout", "showResizeHandles"),
    prevent_initial_call=True,
)
def enter_editable_mode(n_clicks, current_remove, current_resize):
    if n_clicks is None:
        raise PreventUpdate
    return not current_remove, not current_resize, "red"


@callback(Output("layout-output", "children"), Input("grid-layout", "itemLayout"))
def display_layout(current_layout):
    if current_layout and isinstance(current_layout, list):
        print("debug")
        print("Current Layout:", current_layout)  # Debug print
        return html.Div(json.dumps(current_layout))
    return "No layout data available"

@callback(
    Output("grid-layout", "items"),
    Output("grid-layout", "itemLayout"),
    Input("add-dynamic-component", "n_clicks"),
    prevent_initial_call=True,
)
def add_dynamic_component(n):
    if n:
        items = Patch()
        new_id = generate_random_string(10)
        items.append(
            dgl.DraggableWrapper(
                dcc.Graph(
                    figure=px.scatter(
                        df, x="petal_width", y="petal_length", color="species"
                    ),
                    style={"height": "100%"},
                ),
                id=new_id
            )
        )
        itemLayout = Patch()
        itemLayout.append({"i": f"{new_id}", "w": 6})
        return items, itemLayout
    return no_update, no_update


@callback(
    Output("grid-layout", "items", allow_duplicate=True),
    Input("grid-layout", "itemToRemove"),
    State("grid-layout", "itemLayout"),
    prevent_initial_call=True,
)
def remove_component(key, layout):
    if key:
        items = Patch()
        for i in range(len(layout)):
            if layout[i]['i'] == key:
                del items[i]
                break
        return items
    return no_update