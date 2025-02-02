from dash_summernote import DashSummernote
from dash import *
import dash_mantine_components as dmc

component = dmc.Stack([
    DashSummernote(
        id='summernote',
        value='my-value',
        toolbar=[
                    ["style", ["style"]],
                    ["font", ["bold", "underline", "clear"]],
                    ["fontname", ["fontname"]],
                    ["para", ["ul", "ol", "paragraph"]],
                    ["table", ["table"]],
                    ["insert", ["link", "picture", "video"]],
                    ["view", ["fullscreen", "codeview"]]
                ],
        height=300
    ),
    html.Center(html.H1('Output')),
    DashSummernote(
        id='summernote-output',
        value='output',
        toolbar=[],
        height=300
    ),
])

@callback(Output('summernote-output', 'value'), Input('summernote', 'value'))
def display_output(value):
    return value
