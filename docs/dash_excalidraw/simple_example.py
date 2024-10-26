from dash_excalidraw import DashExcalidraw
from dash import Dash, html, dcc, callback, Input, Output, State

initialCanvasData = {}

component = html.Div([
        DashExcalidraw(
        id='excalidraw-simple',
        width='100%',
        height='80vh',
        initialData=initialCanvasData,
    )
    ])