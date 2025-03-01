import dash
from dash import html, Input, Output, State, callback, _dash_renderer, dcc
import dash_dock
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import os
from dotenv import load_dotenv
from pathlib import Path

dock_config = {
    "global": {
        "tabEnableClose": False,
        "tabEnableFloat": True
    },
    "layout": {
        "type": "row",
        "children": [
            {
                "type": "tabset",
                "children": [
                    {
                        "type": "tab",
                        "name": "Tab 1",
                        "component": "text",
                        "id": "tab-1",
                    }
                ]
            },
            {
                "type": "tabset",
                "children": [
                    {
                        "type": "tab",
                        "name": "Tab 2",
                        "component": "text",
                        "id": "tab-2",
                    }
                ]
            }
        ]
    }
}

# Create tab content components
tab_components = [
    dash_dock.Tab(
        id="tab-1",
        children=[
            html.H3("Tab 1 Content"),
        ]
    ),
    dash_dock.Tab(
        id="tab-2",
        children=[
            html.H3("Tab 2 Content"),
        ]
    )
]

# Main app layout
component = html.Div([
    html.H1("Dash Dock Example"),
    dmc.Box(
        dash_dock.DashDock(
            id='dock-layout',
            model=dock_config,
            children=tab_components,
            useStateForModel=True,
            style={
                'position': 'relative',
                'height': '100%',
                'width': '100%',
                'overflow': 'hidden'
            }
        ),
        style={
            'height': '40vh',
            'width': '100%',
            'position': 'relative',
            'overflow': 'hidden'
        }
    )
])
