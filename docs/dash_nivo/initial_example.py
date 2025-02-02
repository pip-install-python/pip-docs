import dash_nivo as dn
from dash import Dash, html, dcc, callback, Output, Input, State
import random
import uuid

COLOR_SCHEMES = [
    'nivo', 'category10', 'accent', 'dark2', 'paired', 'pastel1', 'pastel2', 'set1', 'set2', 'set3', 'tableau10',
    'brown_blueGreen', 'purpleRed_green', 'pink_yellowGreen', 'purple_orange', 'red_blue', 'red_grey',
    'red_yellow_blue', 'red_yellow_green', 'spectral', 'blues', 'greens', 'greys', 'oranges', 'purples', 'reds',
    'blue_green', 'blue_purple', 'green_blue', 'orange_red', 'purple_blue_green', 'purple_blue', 'purple_red',
    'red_purple', 'yellow_green_blue', 'yellow_green', 'yellow_orange_brown', 'yellow_orange_red'
]


def generate_circle_data():
    def create_node(name, children=None):
        node = {
            "id": str(uuid.uuid4()),
            "name": name,
        }
        if children:
            node["children"] = children
        else:
            node["loc"] = random.randint(1000, 100000)
        return node

    return create_node("root", [
        create_node(f"group{i}", [
            create_node(f"subgroup{i}-{j}")
            for j in range(random.randint(2, 5))
        ])
        for i in range(random.randint(3, 7))
    ])


def generate_area_bump_data():
    return [
        {
            "id": f"Series {chr(65 + i)}",
            "data": [
                {"x": str(year), "y": max(1, random.randint(1, 100))} for year in range(2000, 2010)
            ]
        } for i in range(random.randint(3, 8))
    ]


component = html.Div([
    dcc.Store(id='circle-data'),
    dcc.Store(id='area-bump-data'),
    dcc.Store(id='color-schemes'),
    html.Div(id='area-bump-container', style={'height': '400px'}),  # Add a container with fixed height
    html.Div(style={'height': '20px'}),  # Spacer
    html.Div(id='responsive-circle-container', style={'height': '400px'}),  # Add a container with fixed height
], style={'backgroundColor': 'white', "color": "black"})


@callback(
    Output('circle-data', 'data'),
    Output('area-bump-data', 'data'),
    Output('color-schemes', 'data'),
    Input('circle-data', 'id')
)
def update_data(_):
    circle_data = generate_circle_data()
    area_bump_data = generate_area_bump_data()
    color_schemes = random.sample(COLOR_SCHEMES, 2)
    return circle_data, area_bump_data, color_schemes


@callback(
    Output('area-bump-container', 'children'),
    Output('responsive-circle-container', 'children'),
    Input('circle-data', 'data'),
    Input('area-bump-data', 'data'),
    Input('color-schemes', 'data')
)
def update_charts(circle_data, area_bump_data, color_schemes):
    area_bump = dn.AreaBump(
        data=area_bump_data,
        colors={'scheme': color_schemes[1]},
        margin={'top': 40, 'right': 100, 'bottom': 40, 'left': 100},
        axisBottom={'tickSize': 5, 'tickPadding': 5, 'tickRotation': 0},
    )

    responsive_circle = dn.ResponsiveCircle(
        data=circle_data,
        colors={'scheme': color_schemes[0]},
        childColor={'from': 'color', 'modifiers': [['brighter', 0.4]]},
        margin={'top': 20, 'right': 20, 'bottom': 20, 'left': 20},
        padding=4,
    )

    return area_bump, responsive_circle


