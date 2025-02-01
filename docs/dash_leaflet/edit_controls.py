import dash
from dash import html, dcc, callback_context, _dash_renderer, Input, Output, State, callback
import dash_leaflet as dl
from dash_leaflet import EditControl, TileLayer, FeatureGroup, EasyButton
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash_emoji_mart import DashEmojiMart
import dash_ag_grid as dag
import json
from dash.exceptions import PreventUpdate


# Add these class definitions
class Popup(dl.Popup):
    def __init__(self, children=None, **kwargs):
        super().__init__(children=children, **kwargs)


class Tooltip(dl.Tooltip):
    def __init__(self, children=None, **kwargs):
        super().__init__(children=children, **kwargs)

def rgb_to_hex(rgb_str):
    """Convert RGB string to hex color"""
    rgb = rgb_str.replace('rgb(', '').replace(')', '').split(',')
    r, g, b = [int(x.strip()) for x in rgb]
    return f'#{r:02x}{g:02x}{b:02x}'

# Create color picker component
color_input = dmc.ColorInput(
    id="color-picker",
    w='100%',
    format="rgb",
    value="rgb(51, 136, 255)"  # Default Leaflet blue color
)

# Create color controls
color_controls = html.Div([
    dmc.SimpleGrid(
        spacing="xs",
        cols=2,
        children=[
            color_input,
            dmc.Tooltip(
                label="Apply Color",
                position="right",
                offset=3,
                children=[
                    dmc.ActionIcon(
                        DashIconify(icon="noto-v1:paintbrush"),
                        color='blue',
                        size='lg',
                        variant="filled",
                        id="apply-color-button",
                        style={"marginTop": "10px"}
                    )
                ]
            )
        ]
    )
], id="color-picker-container")


# Create custom emoji list
custom = [
    {
        'id': 'custom',
        'name': 'Custom',
        'emojis': [
            {
                'id': 'alien_face',
                'name': 'Alien Face',
                'short_names': ['alien_face'],
                'keywords': ['alien', 'face'],
                'skins': [{'src': '/assets/emoji/faces/alien_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'concern_face',
                'name': 'Concern Face',
                'short_names': ['concern_face'],
                'keywords': ['concern', 'face'],
                'skins': [{'src': '/assets/emoji/faces/concern_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'cowboy_face',
                'name': 'Cowboy Face',
                'short_names': ['cowboy_face'],
                'keywords': ['cowboy', 'face'],
                'skins': [{'src': '/assets/emoji/faces/cowboy_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'crazy_face',
                'name': 'Crazy Face',
                'short_names': ['crazy_face'],
                'keywords': ['crazy', 'face'],
                'skins': [{'src': '/assets/emoji/faces/crazy_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'daw_face',
                'name': 'Daw Face',
                'short_names': ['daw_face'],
                'keywords': ['daw', 'face'],
                'skins': [{'src': '/assets/emoji/faces/daw_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'eye_roll_face',
                'name': 'Eye Roll Face',
                'short_names': ['eye_roll_face'],
                'keywords': ['eye', 'roll', 'face'],
                'skins': [{'src': '/assets/emoji/faces/eye_roll_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'eye_rolling_shocked_face',
                'name': 'Eye Rolling Shocked Face',
                'short_names': ['eye_rolling_shocked_face'],
                'keywords': ['eye', 'rolling', 'shocked', 'face'],
                'skins': [{'src': '/assets/emoji/faces/eye_rolling_shocked_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'faint_face',
                'name': 'Faint Face',
                'short_names': ['faint_face'],
                'keywords': ['faint', 'face'],
                'skins': [{'src': '/assets/emoji/faces/faint_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'fight_face',
                'name': 'Fight Face',
                'short_names': ['fight_face'],
                'keywords': ['fight', 'face'],
                'skins': [{'src': '/assets/emoji/faces/fight_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'happy_cry_face',
                'name': 'Happy Cry Face',
                'short_names': ['happy_cry_face'],
                'keywords': ['happy', 'cry', 'face'],
                'skins': [{'src': '/assets/emoji/faces/happy_cry_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'hungry_face',
                'name': 'Hungry Face',
                'short_names': ['hungry_face'],
                'keywords': ['hungry', 'face'],
                'skins': [{'src': '/assets/emoji/faces/hungry_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'medic_face',
                'name': 'Medic Face',
                'short_names': ['medic_face'],
                'keywords': ['medic', 'face'],
                'skins': [{'src': '/assets/emoji/faces/medic_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'money_face',
                'name': 'Money Face',
                'short_names': ['money_face'],
                'keywords': ['money', 'face'],
                'skins': [{'src': '/assets/emoji/faces/money_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'nerd_face',
                'name': 'Nerd Face',
                'short_names': ['nerd_face'],
                'keywords': ['nerd', 'face'],
                'skins': [{'src': '/assets/emoji/faces/nerd_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'open_face',
                'name': 'Open Face',
                'short_names': ['open_face'],
                'keywords': ['open', 'face'],
                'skins': [{'src': '/assets/emoji/faces/open_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'rip_face',
                'name': 'RIP Face',
                'short_names': ['rip_face'],
                'keywords': ['rip', 'face'],
                'skins': [{'src': '/assets/emoji/faces/rip_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'shocked_face',
                'name': 'Shocked Face',
                'short_names': ['shocked_face'],
                'keywords': ['shocked', 'face'],
                'skins': [{'src': '/assets/emoji/faces/shocked_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'sick_face',
                'name': 'Sick Face',
                'short_names': ['sick_face'],
                'keywords': ['sick', 'face'],
                'skins': [{'src': '/assets/emoji/faces/sick_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'smile_face',
                'name': 'Smile Face',
                'short_names': ['smile_face'],
                'keywords': ['smile', 'face'],
                'skins': [{'src': '/assets/emoji/faces/smile_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'snicker_face',
                'name': 'Snicker Face',
                'short_names': ['snicker_face'],
                'keywords': ['snicker', 'face'],
                'skins': [{'src': '/assets/emoji/faces/snicker_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'soft_smile_face',
                'name': 'Soft Smile Face',
                'short_names': ['soft_smile_face'],
                'keywords': ['soft', 'smile', 'face'],
                'skins': [{'src': '/assets/emoji/faces/soft_smile_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'sour_face',
                'name': 'Sour Face',
                'short_names': ['sour_face'],
                'keywords': ['sour', 'face'],
                'skins': [{'src': '/assets/emoji/faces/sour_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'startled_face',
                'name': 'Startled Face',
                'short_names': ['startled_face'],
                'keywords': ['startled', 'face'],
                'skins': [{'src': '/assets/emoji/faces/startled_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'whoa_face',
                'name': 'Whoa Face',
                'short_names': ['whoa_face'],
                'keywords': ['whoa', 'face'],
                'skins': [{'src': '/assets/emoji/faces/whoa_face.png'}],
                'native': '',
                'unified': 'custom',
            },
            {
                'id': 'coffee_shop',
                'name': 'Coffee Shop',
                'short_names': ['coffee_shop'],
                'keywords': ['coffee', 'shop'],
                'skins': [{'src': '/assets/emoji/faces/coffee_shop.png'}],
                'native': '',
                'unified': 'custom',
            },
        ],
    },
]

# Create emoji picker
emoji_picker = html.Div(DashEmojiMart(
    id='emoji-picker',
    custom=custom,
    autoFocus=False,
    categories=['custom'],
    dynamicWidth=False,
    emojiButtonSize=36,
    emojiSize=24,
), id="emoji-picker-container")

# Create actions display
actions_display = html.Div([
    dmc.Title("Actions:", order=3),
dmc.CodeHighlight(
    id="actions-content",
    language="json",
    withCopyButton=True,
    code="""
    """,

)

])

# Create EditControl with default options
edit_control = EditControl(
    id="edit_control",
    position="topright",
    draw={
        'polyline': True,
        'polygon': True,
        'circle': True,
        'rectangle': True,
        'marker': True,
        'circlemarker': True,
    }
)

# Update the grid columns definition:
grid_columns = [
    {'field': 'type', 'headerName': 'Type', 'editable': False},
    {'field': '_leaflet_id', 'headerName': 'Leaflet ID', 'editable': False},
    {'field': 'color', 'headerName': 'Color', 'editable': False},
    {
        'field': 'children',
        'headerName': 'Children',
        'editable': {'function': "params.data.type === 'marker'"},
        'cellEditor': 'agSelectCellEditor',
        'cellEditorParams': {
            'values': ['None', 'Popup', 'Tooltip']
        }
    },
    {
        'field': 'content',
        'headerName': 'Content',
        'editable': {'function': "params.data.type === 'marker'"},
        'cellEditor': 'ContentEditor',
        'cellRenderer': 'ContentRenderer',
        'cellEditorPopup': True,
        'flex': 2  # Make this column wider
    },
    {
        'field': 'emoji',
        'headerName': 'Emoji',
        'editable': False,
        'cellRenderer': 'EmojiRenderer'
    },
    {'field': 'geometry_type', 'headerName': 'Geometry Type', 'editable': False},
    {'field': 'coordinates', 'headerName': 'Coordinates', 'editable': False},
]

# Create AG Grid
feature_grid = html.Div([
    dag.AgGrid(
        id='feature-grid',
        columnDefs=grid_columns,
        rowData=[],
        columnSize="sizeToFit",
        defaultColDef={
            'resizable': True,
            'sortable': True,
            'filter': True
        },
        dashGridOptions={
            "reactiveCustomComponents": True,  # Add this to fix React warnings
            "animateRows": False  # Add this to prevent animation issues
        }
    )
], style={'marginBottom': '20px', 'height': '200px', 'width': '100%'})


# Add this near the top of your layout
edit_menu = dmc.Affix(
        dmc.Card(
            children=[
                dmc.CardSection(dmc.Center(dmc.Text("Edit Control"))),
                dmc.Group([
                    dmc.Avatar(dmc.Tooltip(
                        DashIconify(
                            icon="flat-color-icons:add-image",
                            width=45,
                            style={"marginTop": "10px"}
                        ),
                        label="Add Location",
                        position="top",
                    ), color="cyan", radius="xl", size="lg"),
                    dmc.Avatar(dmc.Tooltip(
                        DashIconify(
                            icon="material-symbols:web-stories-outline-sharp",
                            width=45,
                            style={"marginTop": "5px"}
                        ),
                        label="Stories",
                        position="top",
                    ), color="cyan", radius="xl", size="lg"),
                    dmc.Avatar(dmc.Tooltip(
                        DashIconify(
                            icon="arcticons:grid-drawing-for-artist",
                            width=45,
                            style={"marginTop": "8px"}
                        ),
                        label="Notice Board",
                        position="top",
                    ), color="cyan", radius="xl", size="lg"),
                    dmc.Avatar(dmc.Tooltip(
                        DashIconify(
                            icon="solar:panorama-linear",
                            width=45,
                            style={"marginTop": "8px"}
                        ),
                        label="Panorama",
                        position="top",
                    ), color="cyan", radius="xl", size="lg"),
                    dmc.Avatar(dmc.Tooltip(
                        DashIconify(
                            icon="garden:wordmark-sell-26",
                            width=45,
                            style={"marginTop": "8px"}
                        ),
                        label="Sell Something",
                        position="top",
                    ), color="cyan", radius="xl", size="lg"),
                ], justify="center"),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            w=380,
        ),
        position={"bottom": '50%', "right": '39vw', "display": "none", "visibility": "hidden"},
        id="edit-menu-affix"
    )

# Create the layout
component = dmc.Stack([
            color_controls,
            emoji_picker,
            dl.Map(
                [
                    TileLayer(),
                    FeatureGroup([edit_control], id="feature_group"),
                    EasyButton(icon="fa-palette", title="color selector", id="color_selector_icon", n_clicks=1),
                    EasyButton(icon="fa-icons", title="emoji selector", id="emoji_selector_icon", n_clicks=1)
                ],
                center=[51.505, -0.09],
                zoom=13,
                style={'height': '60vh', 'zIndex': 0}
            ),
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.TabsTab("Grid", value="grid"),
                            dmc.TabsTab("Actions", value="actions"),
                        ]
                    ),
                    dmc.TabsPanel(feature_grid, value="grid"),
                    dmc.TabsPanel(actions_display, value="actions"),
                ],
                value="grid",
            ),

        ], style={'overflow': 'auto', 'height': '100vh'})

# Callbacks
@callback(
    Output("color-picker-container", "style"),
    Input("color_selector_icon", "n_clicks")
)
def toggle_color_picker(n_clicks):
    if n_clicks % 2 == 0:
        return {"position": "absolute", "left": "24vw", "zIndex": "1000", 'marginTop':'77px'}
    return {"display": "none"}

@callback(
    Output("emoji-picker-container", "style"),
    Input("emoji_selector_icon", "n_clicks")
)
def toggle_emoji_picker(n_clicks):
    print(n_clicks)
    if n_clicks % 2 == 0:
        return {"position": "absolute", "left": "24vw", 'marginTop':'130px', "zIndex": "1000"}
    return {"display": "none"}

@callback(
    Output("edit_control", "draw"),
    Output("edit_control", "currentColor"),
    Input("color-picker", "value")
)
def update_draw_options(color):
    if not color:
        return dash.no_update, dash.no_update

    hex_color = rgb_to_hex(color)
    shape_options = {
        'shapeOptions': {
            'color': hex_color,
            'fillColor': hex_color,
            'fillOpacity': 0.2,
            'opacity': 0.5,
            'weight': 4
        }
    }

    draw_options = {
        'polyline': shape_options,
        'polygon': shape_options,
        'circle': shape_options,
        'rectangle': shape_options,
        'marker': True,
        'circlemarker': shape_options
    }

    return draw_options, hex_color


@callback(
    Output("edit_control", "geojson"),
    [Input("apply-color-button", "n_clicks"),
     Input("emoji-picker", "value"),
     Input("feature-grid", "cellValueChanged")],
    [State("edit_control", "geojson"),
     State("color-picker", "value"),
     State("feature-grid", "rowData")]
)
def update_features(n_clicks, emoji_value, cell_changed, geojson_data, color, grid_data):
    if not geojson_data or not geojson_data.get('features'):
        raise PreventUpdate

    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    features = list(geojson_data['features'])

    if triggered_id == "feature-grid" and isinstance(cell_changed, dict):
        row_idx = cell_changed.get('rowIndex')
        field = cell_changed.get('colId')
        new_value = cell_changed.get('newValue')

        if row_idx is not None and row_idx < len(features):
            feature = features[row_idx]
            if feature['properties']['type'] == 'marker':
                # Get current state from grid data
                grid_row = grid_data[row_idx]
                current_content = grid_row.get('content', '')
                current_children = grid_row.get('children', 'None')

                if field == 'content':
                    # Update content
                    feature['properties']['content'] = new_value
                    if current_children == 'Popup':
                        feature['properties']['children'] = [
                            {'type': 'Popup', 'children': new_value}
                        ]
                    elif current_children == 'Tooltip':
                        feature['properties']['children'] = [
                            {'type': 'Tooltip', 'children': new_value}
                        ]

                elif field == 'children':
                    # Update children type
                    feature['properties']['children_type'] = new_value
                    if new_value == 'None':
                        feature['properties']['children'] = []
                    elif new_value == 'Popup':
                        feature['properties']['children'] = [
                            {'type': 'Popup', 'children': current_content}
                        ]
                    elif new_value == 'Tooltip':
                        feature['properties']['children'] = [
                            {'type': 'Tooltip', 'children': current_content}
                        ]

    elif triggered_id == "emoji-picker" and emoji_value:
        for feature in reversed(features):
            if feature['properties']['type'] == 'marker':
                feature['properties']['emoji'] = emoji_value
                feature['properties']['icon'] = {
                    'iconUrl': emoji_value,
                    'iconSize': [25, 25],
                    'iconAnchor': [12.5, 12.5]
                }
                # Initialize if not present
                if 'children' not in feature['properties']:
                    feature['properties']['children'] = []
                if 'children_type' not in feature['properties']:
                    feature['properties']['children_type'] = 'None'
                if 'content' not in feature['properties']:
                    feature['properties']['content'] = ''
                break

    elif triggered_id == "apply-color-button" and color and n_clicks:
        hex_color = rgb_to_hex(color)
        for feature in reversed(features):
            if feature['properties']['type'] != 'marker':
                feature['properties']['color'] = hex_color
                break

    return {
        'type': 'FeatureCollection',
        'features': features
    }

@callback(
    Output("actions-content", "code"),
    [Input("edit_control", "geojson"),
     Input("apply-color-button", "n_clicks"),
     Input("emoji-picker", "value")]
)
def display_action_data(geojson_data, n_clicks, emoji_value):
    if not geojson_data or not geojson_data.get('features'):
        return "No features drawn"

    display_geojson = {
        'type': 'FeatureCollection',
        'features': []
    }

    for feature in geojson_data['features']:
        new_feature = {
            'type': 'Feature',
            'properties': {
                'type': feature['properties']['type'],
                '_leaflet_id': feature['properties'].get('leafletId'),
                'color': feature['properties'].get('color')
            },
            'geometry': feature['geometry']
        }

        # Add emoji property for markers
        if feature['properties']['type'] == 'marker' and 'emoji' in feature['properties']:
            new_feature['properties']['emoji'] = feature['properties']['emoji']

        # Add additional properties if present
        for prop in ['radius', 'mRadius', 'bounds']:
            if prop in feature['properties']:
                new_feature['properties'][f'_{prop}'] = feature['properties'][prop]

        display_geojson['features'].append(new_feature)

    return f"""{json.dumps(display_geojson, indent=2)}"""




@callback(
    [Output("feature-grid", "rowData"),
     Output("actions-content", "children", allow_duplicate=True)],
    [Input("edit_control", "geojson"),
     Input("apply-color-button", "n_clicks"),
     Input("emoji-picker", "value")],
    prevent_initial_call=True
)
def update_grid_and_actions(geojson_data, n_clicks, emoji_value):
    if not geojson_data or not geojson_data.get('features'):
        return [], "No features drawn"

    # Prepare grid data
    grid_data = []
    display_features = []

    for feature in geojson_data['features']:
        # Extract coordinates
        geometry_type = feature['geometry']['type']
        coordinates = feature['geometry']['coordinates']
        coords_str = str(coordinates[0]) if geometry_type == 'Polygon' else str(coordinates)

        # Get children info
        feature_children = feature['properties'].get('children', [])
        children_type = 'None'
        content = feature['properties'].get('content', '')

        if feature_children:
            if isinstance(feature_children, list) and len(feature_children) > 0:
                child = feature_children[0]
                if isinstance(child, dict):
                    children_type = child.get('type', 'None')
                    content = child.get('children', content)

        # Create grid row
        row = {
            'type': feature['properties']['type'],
            '_leaflet_id': feature['properties'].get('leafletId'),
            'color': feature['properties'].get('color', ''),
            'children': children_type,
            'content': content,
            'emoji': feature['properties'].get('emoji', ''),
            'geometry_type': geometry_type,
            'coordinates': coords_str,
        }
        grid_data.append(row)

        # Create display feature
        new_feature = {
            'type': 'Feature',
            'properties': {
                'type': feature['properties']['type'],
                '_leaflet_id': feature['properties'].get('leafletId'),
                'color': feature['properties'].get('color'),
                'children': children_type,
                'content': content,
                'icon': feature['properties'].get('icon'),
                'emoji': feature['properties'].get('emoji'),
                'children_type': children_type,
            },
            'geometry': feature['geometry']
        }
        display_features.append(new_feature)

    display_geojson = {
        'type': 'FeatureCollection',
        'features': display_features
    }

    return grid_data, json.dumps(display_geojson, indent=2)


@callback(
    Output("edit-menu-affix", "style"),
    Input("edit_control", "geojson"),
    State("edit-menu-affix", "style"),
    prevent_initial_call=True
)
def show_edit_menu(geojson_data, current_style):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    print('initial')
    print(geojson_data)
    print(current_style)
    if not geojson_data or not geojson_data.get('features'):
        return{"bottom": '50%', "right": '39vw', "display": "none", "visibility": "hidden"}

    features = geojson_data['features']
    if features and features[-1]['properties']['type'] == 'marker':
        print(features)
        return {"bottom": '50%', "right": '39vw', "display": "block", "visibility": "visible"}

    return {"bottom": '50%', "right": '39vw', "display": "none", "visibility": "hidden"}
