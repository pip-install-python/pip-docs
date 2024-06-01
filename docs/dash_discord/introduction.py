from dash import *
from dash_discord import *
import json

component = html.Div([
    DiscordWidget(
        id='widget',
        server='1246197743307980940',
        channel='1246197743781810332',
        height='70vh',
        width='100%',
    )
])
