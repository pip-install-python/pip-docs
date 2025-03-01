import dash
from dash import Input, Output, html, dcc, clientside_callback, callback
import dash_dock
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import os
from dotenv import load_dotenv
from pathlib import Path

# Setup the .env file to protect your API Key
env_path = Path('.') / '.env'
load_dotenv(env_path)

API_KEY = os.getenv("API_KEY")

styles = {
    "container": {
        "width": "100%",
        "height": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "justifyContent": "center",
        "padding": "20px",
    },
    "header": {
        "textAlign": "center",
        "marginBottom": "20px",
        "width": "100%",
        "maxWidth": "600px",
    },
    "apiInput": {
        "width": "100%",
        "maxWidth": "400px",
        "padding": "8px",
        "marginBottom": "10px",
        "border": "1px solid #ccc",
        "borderRadius": "4px",
    },
    "description": {
        "fontSize": "14px",
        "color": "#666",
        "marginBottom": "20px",
        "textAlign": "center",
    },
    "demoArea": {
        "display": "flex",
        "width": "100%",
        "height": "500px",  # Fixed height for demo area
        "backgroundColor": "white",
        "justifyContent": "center",
        "alignItems": "center",
        "position": "relative",
    },
    "planet": {
        "height": "120px",
        "width": "120px",
        "borderRadius": "50%",
        "backgroundColor": "#1976d2",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "color": "white",
        "cursor": "pointer",
        "transition": "all 0.3s",
        "position": "relative",
    },
    "satellite": {
        "height": "40px",
        "width": "40px",
        # 'borderRadius': '50%',
        # 'backgroundColor': '#ff4081',
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "color": "white",
        "cursor": "pointer",
        "zIndex": 1,
    },
    "gridColumn": {
        "height": "300px",
        "width": "100%",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "position": "relative",
        "padding": "20px",
        "boxSizing": "border-box",
    },
    "features": {
        "marginTop": "20px",
        "padding": "20px",
        "backgroundColor": "#f5f5f5",
        "borderRadius": "8px",
        # "maxWidth": "600px",
        "width": "100%",
        'color': 'black'
    },
    "featureList": {"listStyle": "none", "padding": "0", "margin": "0"},
    "featureItem": {
        "padding": "8px 0",
        "display": "flex",
        "alignItems": "center",
        "gap": "8px",
    },
}


# Define the dock layout configuration
dock_config = {
    "global": {
        "tabEnableClose": False,
        "tabEnableFloat": True,
    },
    "borders": [
        {
            "type": "border",
            "location": "bottom",
            "size": 100,
            "children": [
                {
                    "type": "tab",
                    "name": "Console",
                    "component": "text",
                    "id": "console-tab"
                }
            ]
        },
        {
            "type": "border",
            "location": "left",
            "size": 250,
            "children": [
                {
                    "type": "tab",
                    "name": "Explorer",
                    "component": "text",
                    "id": "explorer-tab"
                }
            ]
        }
    ],
    "layout": {
        "type": "row",
        "weight": 100,
        "children": [
            {
                "type": "tabset",
                "weight": 60,
                "selected": 0,
                "children": [
                    {
                        "type": "tab",
                        "name": "Main View",
                        "component": "text",
                        "enableFloat": True,
                        "id": "main-view-tab",
                    }
                ]
            },
            {
                "type": "tabset",
                "weight": 40,
                "selected": 0,
                "children": [
                    {
                        "type": "tab",
                        "name": "Data Properties",
                        "component": "text",
                        "id": "data-properties-tab",
                    },
                    {
                        "type": "tab",
                        "name": "Chart Properties",
                        "component": "text",
                        "id": "chart-properties-tab",
                    }
                ]
            }
        ]
    }
}

# Sample data for charts
chart_data = [
    {"month": "January", "value": 10, "x": 1, "y": 10},
    {"month": "February", "value": 11, "x": 2, "y": 11},
    {"month": "March", "value": 9, "x": 3, "y": 9},
    {"month": "April", "value": 16, "x": 4, "y": 16},
    {"month": "May", "value": 14, "x": 5, "y": 14}
]

# Scatter chart data format is different, so we need to transform it
scatter_data = [
    {
        "color": "blue.6",
        "name": "Sample Data",
        "data": [{"x": d["x"], "y": d["y"]} for d in chart_data]
    }
]

# Create theme switch component
theme_switch = dmc.Switch(
    offLabel=DashIconify(icon="radix-icons:sun", width=15, style={"color": "#FFB300"}),
    onLabel=DashIconify(icon="radix-icons:moon", width=15, style={"color": "#FFD700"}),
    id="color-scheme-switch",
    size="md",
    persistence=True,
    color="gray"
)

# Create the tab content components
tab_components = [
    dash_dock.Tab(
        id="explorer-tab",
        children=[
            html.H4("Explorer"),
            dcc.Checklist(
                id="dataset-selector",
                options=[
                    {"label": "Dataset A", "value": "a"},
                    {"label": "Dataset B", "value": "b"},
                    {"label": "Dataset C", "value": "c"},
                ],
                value=["a"]
            )
        ]
    ),
    dash_dock.Tab(
        id="main-view-tab",
        children=[
            html.H3("Main Visualization"),
            dmc.Box(id="selected-datasets-display"),
            dmc.Box(id="main-chart-container"),  # Container for dynamic chart
        ]
    ),
    dash_dock.Tab(
        id="data-properties-tab",
        children=[
            html.H4("Data Properties"),
            html.Button("Refresh Data", id="refresh-data-btn"),
            dmc.Box(id="data-refresh-status")
        ]
    ),
    dash_dock.Tab(
        id="chart-properties-tab",
        children=[
            html.H4("Chart Properties"),
            dmc.RadioGroup(
                id="chart-type-selector",
                label="Select Chart Type",
                value="line",
                children=dmc.Stack([
                    dmc.Radio(label="Line Chart", value="line"),
                    dmc.Radio(label="Bar Chart", value="bar"),
                    dmc.Radio(label="Scatter Chart", value="scatter"),
                ])
            ),
            dmc.Box(id="selected-chart-type")
        ]
    ),
    dash_dock.Tab(
        id="console-tab",
        children=[
            html.H4("Console"),
            html.Pre(id="console-output", style={"height": "80px", "overflow": "auto"})
        ]
    ),
]

# Custom headers for tabs
custom_headers = {
    "main-view-tab": html.Div([
        DashIconify(icon="fluent-emoji:bar-chart", width=15),
        "Main View"
    ], style={"display": "flex", "alignItems": "center"}),

    "explorer-tab": html.Div([
        DashIconify(icon="flat-color-icons:folder", width=15),
        "Explorer"
    ], style={"display": "flex", "alignItems": "center"})
}

component = dmc.Box(
    html.Div(
        id="app-container",
        children=[
            # Header section - fixed at top
            html.Div(
                id="app-header",
                children=[
                    html.Link(
                        rel="stylesheet",
                        href="https://use.fontawesome.com/releases/v5.15.4/css/all.css"
                    ),
                    dmc.Paper(
                        children=[
                            dmc.Group([
                                dmc.Title("Dash Dock Example", order=3),
                                theme_switch
                            ], justify="apart", align="center")
                        ],
                        p="md",
                        shadow="xs",
                        radius="md",
                        withBorder=True,
                        style={"height": "100%"}
                    ),
                ]
            ),

            # DashDock container - fills remaining space
            html.Div(id="dash-dock-container", children=dash_dock.DashDock(
        id='dock-layout',
        model=dock_config,
        children=tab_components,
        useStateForModel=True,
        headers=custom_headers,
        apiKey=API_KEY,
        debugMode=True,
        supportsPopout=False,
style={
                'position': 'relative',  # Changed from absolute
                'height': '100%',  # Take full height of parent
                'width': '100%',  # Take full width of parent
                'overflow': 'hidden'  # Removed !important and semicolons
            }
    ), style={
            'height': '40vh',  # Fixed height on the container
            'width': '100%',  # Full width
            'position': 'relative',  # Create positioning context
            'overflow': 'hidden'  # Prevent content overflow
        })
        ]
    )
)

# Clientside callback for theme toggle
clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');
       return window.dash_clientside.no_update
    }
    """,
    Output("color-scheme-switch", "id"),
    Input("color-scheme-switch", "checked"),
)


# Callback for dataset selection
@callback(
    Output('selected-datasets-display', 'children'),
    [Input('dataset-selector', 'value')]
)
def update_selected_datasets(selected_datasets):
    if not selected_datasets:
        return "No datasets selected"

    return f"Selected datasets: {', '.join(selected_datasets)}"


# Callback for chart type selection
@callback(
    Output('selected-chart-type', 'children'),
    [Input('chart-type-selector', 'value')]
)
def update_chart_type(chart_type):
    return f"Selected chart type: {chart_type}"


# Callback for data refresh
@callback(
    Output('data-refresh-status', 'children'),
    Output('console-output', 'children'),
    [Input('refresh-data-btn', 'n_clicks')]
)
def refresh_data(n_clicks):
    if not n_clicks:
        return "Data not refreshed yet", "Console initialized. Waiting for events..."

    console_msg = f"Data refresh requested at click {n_clicks}"
    return f"Data refreshed {n_clicks} times", console_msg


# Callback to update the chart based on the selected chart type
@callback(
    Output('main-chart-container', 'children'),
    [Input('chart-type-selector', 'value')]
)
def update_chart(chart_type):
    if chart_type == "line":
        return dmc.LineChart(
            h=400,
            dataKey="month",
            data=chart_data,
            withLegend=True,
            xAxisLabel="Month",
            yAxisLabel="Value",
            series=[
                {"name": "value", "color": "blue.6", "label": "Sample Data"}
            ]
        )
    elif chart_type == "bar":
        return dmc.BarChart(
            h=400,
            dataKey="month",
            data=chart_data,
            withLegend=True,
            xAxisLabel="Month",
            yAxisLabel="Value",
            series=[
                {"name": "value", "color": "blue.6", "label": "Sample Data"}
            ]
        )
    elif chart_type == "scatter":
        return dmc.ScatterChart(
            h=400,
            data=scatter_data,
            dataKey={"x": "x", "y": "y"},
            xAxisLabel="X Value",
            yAxisLabel="Y Value",
            withLegend=True
        )
    else:
        return html.Div("Invalid chart type selected")
