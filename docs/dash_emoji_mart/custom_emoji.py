from dash import *
from dash_ace import DashAceEditor
from pprint import pformat

# in this format use get_asset_url for local files or use the url directly for external files
custom = [
    {
        'id': 'custom',
        'name': 'Custom',
        'emojis': [
            {
                'id': 'party_parrot',
                'name': 'Party Parrot',
                'short_names': ['party_parrot'],
                'keywords': ['dance', 'dancing'],
                'skins': [{'src': "dash.get_asset_url('party_parrot.gif')"}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'plotly',
                'name': 'Plotly',
                'short_names': ['plotly'],
                'keywords': ['plotly', 'dash'],
                'skins': [{'src': 'https://store-images.s-microsoft.com/image/apps.36868.bfb0e2ee-be9e-4c73-807f-e0a7b805b1be.712aff5d-5800-47e0-97be-58d17ada3fb8.a46845e6-ce94-44cf-892b-54637c6fcf06'}],
                'native': '',
                'unified': 'custom',
            },
        ],
    },
]

component = [
DashAceEditor(
    id='ace-editor',
    value=pformat(custom),
    theme='monokai',
    mode='python',
    tabSize=2,
    enableBasicAutocompletion=True,
    enableLiveAutocompletion=True,
    autocompleter='/autocompleter?prefix=',
    placeholder='Python code ...',
    readOnly=True,
    style={'height': '300px', 'width': '100%'},
)
]