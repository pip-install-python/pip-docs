import dash
from dash import html, Input, Output, State, callback, _dash_renderer, dcc
from dash_planet import DashPlanet
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(env_path)

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

styles = {
    'root': {
        'display': 'flex',
        'flex': '1',
        'width': '100%',
        'backgroundColor': 'white',
        'justifyContent': 'center',
        'alignItems': 'center',
        'flexDirection': 'column',
        'position': 'relative',
        # 'marginTop': '100px',
        'gap': '20px'
    },
    'satellite': {
        'height': '40px',
        'width': '40px',
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'color': 'white',
        'cursor': 'pointer',
        'zIndex': 1
    },
    'form': {
        'width': '300px',
        'margin': '20px auto',
        'padding': '20px',
        'backgroundColor': '#f5f5f5',
        'borderRadius': '8px',
    }
}


def generate_satellites(count, empty_divs=5):
    """Generate satellite elements with icons"""
    icons = [
        "fxemoji:email",
        "noto:calendar",
        "emojione-v1:bar-chart",
        "emojione:gear",
        "flat-color-icons:file",
        "emojione-v1:open-folder",
        "twemoji:heart-on-fire",
        "flat-color-icons:home",
    ]

    empty_div_style = {
        'width': '40px',
        'height': '40px',
        'transition': 'transform 0.3s ease-in-out'
    }

    return [
        html.Div([
            DashIconify(icon=icons[i % len(icons)], width=40, height=40, color="white")
        ], style=styles['satellite'], id={'type': 'satellite', 'index': i})
        for i in range(count)
    ] + [html.Div(style=empty_div_style) for _ in range(empty_divs)]


component = dmc.Box([
    dcc.Input(
        id='api-key-input',
        type='text',
        value='O3iEIQMkVzbbdgs-ZSfBotNt3WoLhqGjID0fMrhuN64',
        style={'display': 'none'}
    ),

    dmc.Grid([
    # Add form controls
    dmc.GridCol([
        dmc.Paper([
            dmc.Text("Menu Semicircle Controls", size="lg", fw=500, ta="center", mb="md"),
            dmc.NumberInput(
                id="menu-planet-empty-divs-input",
                label="Number of Empty Divs",
                value=5,
                min=0,
                max=10,
                step=1,
                mb="sm"
            ),
            dmc.NumberInput(
                id="menu-planet-rotation-input",
                label="Rotation (degrees)",
                value=0,
                min=0,
                max=360,
                step=45,
                mb="sm"
            ),
            dmc.NumberInput(
                id="menu-planet-orbit-radius-input",
                label="Orbit Radius",
                value=80,
                min=40,
                max=200,
                step=10,
                mb="sm"
            ),
        ], p="md", shadow="sm", withBorder=True, style=styles['form'])
    ], span={'md': 5, 'sm': 12}),

    dmc.GridCol([
        DashPlanet(
            id='menu-planet',
            centerContent=dmc.Indicator(
                dmc.Avatar(
                    size="lg",
                    radius="xl",
                    src="https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-3.png",
                ),
                inline=True,
                offset=7,
                position="bottom-end",
                color="red",
                withBorder=True,
                size=16,
            ),
            open=True,
            orbitRadius=80,
            hideOrbit=True,
            bounce=True,
            bounceOnOpen=True,
            rotation=90,
            dragablePlanet=True,
            dragableSatellites=True,
            satelliteOrientation='DEFAULT',
            children=generate_satellites(3),
            mass=4,
            tension=500,
            friction=19,
            apiKey='API_KEY'
        )
    ], style=styles['root'], span={'md': 4, 'sm': 12}),
        dmc.GridCol(span={'md': 3, 'sm': 12})
        ])
])


@callback(
    Output('menu-planet', 'children'),
    Output('menu-planet', 'rotation'),
    Input('menu-planet-empty-divs-input', 'value'),
    Input('menu-planet-rotation-input', 'value')
)
def update_satellites(empty_divs, rotation):
    return generate_satellites(3, empty_divs), rotation

@callback(
    Output("menu-planet", "orbitRadius"),
    Input("menu-planet-orbit-radius-input", "value"),
    prevent_initial_call=True,
)
def update_orbit_radius(value):
    return value
