import dash_summernote
from dash import *

component =  html.Div([
    dash_summernote.DashSummernote(
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
    dash_summernote.DashSummernote(
        id='summernote-output',
        value='output',
        toolbar=[],
        height=300
    ),
    # html.Div(id='output')
])

@callback(Output('summernote-output', 'value'), Input('summernote', 'value'))
def display_output(value):
    return value
