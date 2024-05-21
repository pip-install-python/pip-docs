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

])

@callback(Output('summernote-output', 'value'), Input('summernote', 'value'))
def display_output(value):
    return value