import dash_summernote
from dash import *
import dash_mantine_components as dmc
from dash_iconify import DashIconify

demo_py = """
import dash
from dash import *
import dash_mantine_components as dmc

app = dash.Dash(__name__, external_stylesheets=dmc.styles.ALL)

 app.layout = dmc.MantineProvider([dmc.Stack([
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
    )
], style={'width': '100%', 'overflow':'auto'})
])

@callback(Output('summernote-output', 'value'), Input('summernote', 'value'))
def display_output(value):
    return value

if __name__ == '__main__':
    app.run_server(debug=True, port='8050')
"""

code = [
    {
        "fileName": "summernote_example.py",
        "code": demo_py,
        "language": "python",
        "icon": DashIconify(icon="skill-icons:python-dark", width=20),
    },
]

component =  dmc.Stack([
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
dmc.CodeHighlightTabs(
    code=code,
    withExpandButton=True,
    expandCodeLabel="Show full code",
    collapseCodeLabel="Show less",
    defaultExpanded=False,
    maxCollapsedHeight=200  # Height in collapsed state (in pixels)
)
])

@callback(Output('summernote-output', 'value'), Input('summernote', 'value'))
def display_output(value):
    return value
