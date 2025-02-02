import dash
from dash import html, dcc, callback, Input, Output, State
import dash_leaflet as dl
import json
import math

track_data = [
    {
      'lat': 34.25615548523744,
      'lng': 108.91164044842363,
    },
    {
      'lat': 34.256155386830855,
      'lng': 108.91179023713374,
    },
    {
      'lat': 34.256155386830855,
      'lng': 108.91179023713374,
    },
    {
      'lat': 34.25607942383744,
      'lng': 108.91177925878043,
    },
    {
      'lat': 34.255720609670156,
      'lng': 108.91171038494707,
    },
    {
      'lat': 34.255607664345405,
      'lng': 108.91169441655762,
    },
    {
      'lat': 34.25553269366626,
      'lng': 108.91169442258713,
    },
    {
      'lat': 34.25544769867856,
      'lng': 108.91173736885014,
    },
    {
      'lat': 34.25544769867856,
      'lng': 108.91173736885014,
    },
    {
      'lat': 34.25541482067108,
      'lng': 108.91157060617357,
    },
    {
      'lat': 34.255437230925885,
      'lng': 108.91091151687152,
    },
    {
      'lat': 34.2554647726071,
      'lng': 108.90999074936826,
    },
    {
      'lat': 34.255474922592086,
      'lng': 108.90972209999609,
    },
    {
      'lat': 34.255470035735925,
      'lng': 108.90952435653506,
    },
    {
      'lat': 34.25546585239153,
      'lng': 108.90796530095042,
    },
    {
      'lat': 34.255466079902156,
      'lng': 108.90748786950532,
    },
    {
      'lat': 34.255466139078585,
      'lng': 108.90736001962813,
    },
    {
      'lat': 34.25546047844199,
      'lng': 108.90659889522819,
    },
    {
      'lat': 34.25545553696015,
      'lng': 108.90646504623344,
    },
    {
      'lat': 34.255455684520776,
      'lng': 108.90610644487133,
    },
    {
      'lat': 34.25543990484673,
      'lng': 108.90555904106137,
    },
    {
      'lat': 34.255434929044085,
      'lng': 108.90550010453336,
    },
    {
      'lat': 34.25671044153241,
      'lng': 108.90546803620235,
    },
    {
      'lat': 34.256994331993134,
      'lng': 108.9054630187248,
    },
    {
      'lat': 34.2573861821876,
      'lng': 108.90545199896282,
    },
    {
      'lat': 34.2583997892619,
      'lng': 108.90543593456538,
    },
    {
      'lat': 34.25896857276571,
      'lng': 108.90541491120209,
    },
    {
      'lat': 34.2600241555513,
      'lng': 108.90541482639716,
    },
    {
      'lat': 34.26038901329847,
      'lng': 108.9054088034598,
    },
    {
      'lat': 34.260957801498556,
      'lng': 108.9053717970368,
    },
    {
      'lat': 34.261048767618306,
      'lng': 108.90536579609017,
    },
    {
      'lat': 34.26174549083055,
      'lng': 108.90536574011179,
    },
    {
      'lat': 34.262888033588865,
      'lng': 108.9053716419483,
    },
    {
      'lat': 34.263321862668384,
      'lng': 108.90536561345179,
    },
    {
      'lat': 34.26381066919356,
      'lng': 108.90536057947523,
    },
    {
      'lat': 34.264314469827035,
      'lng': 108.90535454535133,
    },
    {
      'lat': 34.264416428997436,
      'lng': 108.90535453715839,
    },
    {
      'lat': 34.264545377344014,
      'lng': 108.90535452679667,
    },
    {
      'lat': 34.26485025108296,
      'lng': 108.90536549063917,
    },
    {
      'lat': 34.26494221420379,
      'lng': 108.90536548324928,
    },
    {
      'lat': 34.265745895588346,
      'lng': 108.9053544303257,
    },
    {
      'lat': 34.26596581086138,
      'lng': 108.90534442324677,
    },
    {
      'lat': 34.2664006399377,
      'lng': 108.90533339995,
    },
    {
      'lat': 34.26711335674291,
      'lng': 108.90532235431407,
    },
    {
      'lat': 34.267682127119045,
      'lng': 108.90532230860484,
    },
    {
      'lat': 34.267977007932025,
      'lng': 108.90532228490632,
    },
    {
      'lat': 34.26842182796332,
      'lng': 108.90532224915717,
    },
    {
      'lat': 34.26893662309246,
      'lng': 108.90531221835984,
    },
    {
      'lat': 34.26961734908727,
      'lng': 108.90530616999233,
    },
    {
      'lat': 34.27079687296456,
      'lng': 108.90529608575685,
    },
    {
      'lat': 34.27079687296456,
      'lng': 108.90529608575685,
    },
    {
      'lat': 34.270796835711245,
      'lng': 108.90539697877264,
    },
    {
      'lat': 34.27080243135706,
      'lng': 108.90641586657812,
    },
    {
      'lat': 34.270802076591195,
      'lng': 108.9072299373526,
    },
    {
      'lat': 34.270812817234265,
      'lng': 108.90777629238795,
    },
    {
      'lat': 34.270822675023936,
      'lng': 108.90806094950152,
    },
    {
      'lat': 34.27082259586891,
      'lng': 108.90822075550248,
    },
    {
      'lat': 34.27082849640933,
      'lng': 108.9084135191401,
    },
    {
      'lat': 34.27083332877497,
      'lng': 108.90873512064815,
    },
    {
      'lat': 34.27083823372032,
      'lng': 108.90891189899708,
    },
    {
      'lat': 34.270843970260856,
      'lng': 108.9093942860198,
    },
    {
      'lat': 34.270843671165785,
      'lng': 108.90992459787954,
    },
    {
      'lat': 34.27084322644142,
      'lng': 108.91067459821011,
    },
    {
      'lat': 34.270842940218785,
      'lng': 108.91113596785353,
    },
    {
      'lat': 34.270842859216124,
      'lng': 108.91126379113685,
    },
    {
      'lat': 34.270847625398574,
      'lng': 108.91162328889843,
    },
    {
      'lat': 34.27084755144006,
      'lng': 108.91173612991112,
    },
    {
      'lat': 34.27085335722669,
      'lng': 108.91202471962777,
    },
    {
      'lat': 34.270852784122816,
      'lng': 108.9128555142759,
    },
    {
      'lat': 34.27085267748,
      'lng': 108.91300529292631,
    },
    {
      'lat': 34.27085254672574,
      'lng': 108.91318702269936,
    },
    {
      'lat': 34.27085205628723,
      'lng': 108.91385101989933,
    },
    {
      'lat': 34.27087119213721,
      'lng': 108.91615435172467,
    },
    {
      'lat': 34.27087566746897,
      'lng': 108.91675434843464,
    },
    {
      'lat': 34.2708814553737,
      'lng': 108.91698994875553,
    },
    {
      'lat': 34.27085429757733,
      'lng': 108.9171776307563,
    },
    {
      'lat': 34.27080602434836,
      'lng': 108.91749908177066,
    },
    {
      'lat': 34.27080602434836,
      'lng': 108.91749908177066,
    },
    {
      'lat': 34.270751948023054,
      'lng': 108.91760590116054,
    },
    {
      'lat': 34.27073590010758,
      'lng': 108.9176648001958,
    },
    {
      'lat': 34.270708807347326,
      'lng': 108.91777660774166,
    },
    {
      'lat': 34.27070375357,
      'lng': 108.91783650359831,
    },
    {
      'lat': 34.270708656282736,
      'lng': 108.91793832501797,
    },
    {
      'lat': 34.27073056759363,
      'lng': 108.91802317433239,
    },
    {
      'lat': 34.270778426427114,
      'lng': 108.91815194371763,
    },
    {
      'lat': 34.27082633013241,
      'lng': 108.91823279701194,
    },
    {
      'lat': 34.27090620143976,
      'lng': 108.91833361195992,
    },
    {
      'lat': 34.27096613594049,
      'lng': 108.91837653091702,
    },
    {
      'lat': 34.27103006872475,
      'lng': 108.91841944945133,
    },
    {
      'lat': 34.271094016769126,
      'lng': 108.91844639632818,
    },
    {
      'lat': 34.27115297737252,
      'lng': 108.91846236313094,
    },
    {
      'lat': 34.27124992726748,
      'lng': 108.91847333575198,
    },
    {
      'lat': 34.271362907088765,
      'lng': 108.91844637465212,
    },
    {
      'lat': 34.27141590080522,
      'lng': 108.9184303988106,
    },
    {
      'lat': 34.27146990941202,
      'lng': 108.91839845127609,
    },
    {
      'lat': 34.271506924906745,
      'lng': 108.91836650505593,
    },
    {
      'lat': 34.27161499324317,
      'lng': 108.91824870518059,
    },
    {
      'lat': 34.27165204453143,
      'lng': 108.91817882572266,
    },
    {
      'lat': 34.27169010556983,
      'lng': 108.91809796526304,
    },
    {
      'lat': 34.27170014671252,
      'lng': 108.91805004879423,
    },
    {
      'lat': 34.27170014671252,
      'lng': 108.91805004879423,
    },
    {
      'lat': 34.271813130666544,
      'lng': 108.91801809584462,
    },
    {
      'lat': 34.271926114560934,
      'lng': 108.91798614283951,
    },
    {
      'lat': 34.27202208565869,
      'lng': 108.91797515437597,
    },
    {
      'lat': 34.27211304847173,
      'lng': 108.91797514704386,
    },
    {
      'lat': 34.27364144760009,
      'lng': 108.91794807112001,
    },
    {
      'lat': 34.27430117651852,
      'lng': 108.91794801793834,
    },
    {
      'lat': 34.27430117651852,
      'lng': 108.91794801793834,
    },
    {
      'lat': 34.27452116643137,
      'lng': 108.91786215053015,
    },
    {
      'lat': 34.27504196130342,
      'lng': 108.91785212600149,
    },
    {
      'lat': 34.275856640147865,
      'lng': 108.91783608824171,
    },
    {
      'lat': 34.27635543402423,
      'lng': 108.91783604803085,
    },
    {
      'lat': 34.27635543402423,
      'lng': 108.91783604803085,
    },
    {
      'lat': 34.277267066837524,
      'lng': 108.91782499372012,
    },
    {
      'lat': 34.27870948266951,
      'lng': 108.91780890532164,
    },
    {
      'lat': 34.27895038797587,
      'lng': 108.91780289635481,
    },
    {
      'lat': 34.2793632206358,
      'lng': 108.91779787178181,
    },
    {
      'lat': 34.28040878884263,
      'lng': 108.91779279619023,
    },
    {
      'lat': 34.28146034867298,
      'lng': 108.91779271140113,
    },
    {
      'lat': 34.28146034867298,
      'lng': 108.91779271140113,
    },
    {
      'lat': 34.28263387644584,
      'lng': 108.91777065508535,
    },
    {
      'lat': 34.28417326218677,
      'lng': 108.91773359532593,
    },
    {
      'lat': 34.28442516136318,
      'lng': 108.91772758544468,
    },
    {
      'lat': 34.28569565334534,
      'lng': 108.91769553859388,
    },
    {
      'lat': 34.28609849266868,
      'lng': 108.9176845252085,
    },
    {
      'lat': 34.28774477772293,
      'lng': 108.91770036464814,
    },
    {
      'lat': 34.289932847077175,
      'lng': 108.91769519685113,
    },
    {
      'lat': 34.29036166314886,
      'lng': 108.91769516226238,
    },
    {
      'lat': 34.29064054341951,
      'lng': 108.91769513976726,
    },
    {
      'lat': 34.291648114741015,
      'lng': 108.91769006717632,
    },
    {
      'lat': 34.29183603934873,
      'lng': 108.91768406243645,
    },
    {
      'lat': 34.29314945213906,
      'lng': 108.91770591827063,
    },
    {
      'lat': 34.293712204034165,
      'lng': 108.9177108641832,
    },
    {
      'lat': 34.294226985630914,
      'lng': 108.91770583134237,
    },
    {
      'lat': 34.29428596006031,
      'lng': 108.9177058265846,
    },
    {
      'lat': 34.29436110539907,
      'lng': 108.9175131548741,
    },
    {
      'lat': 34.29435643485554,
      'lng': 108.91715377349566,
    },
    {
      'lat': 34.29435732039652,
      'lng': 108.916147466944,
    },
    {
      'lat': 34.29435732039652,
      'lng': 108.916147466944,
    },
    {
      'lat': 34.294572232299814,
      'lng': 108.91614145952745,
    },
    {
      'lat': 34.29463620453703,
      'lng': 108.91614145436851,
    },
    {
      'lat': 34.29495306695566,
      'lng': 108.91614142881548,
    },
    {
      'lat': 34.29495306695566,
      'lng': 108.91614142881548,
    },
    {
      'lat': 34.29496736180883,
      'lng': 108.91578701078069,
    },
  ]


def calculate_bearing(point1, point2):
    """Calculate the bearing between two points."""
    lat1 = math.radians(point1['lat'])
    lat2 = math.radians(point2['lat'])
    diff_long = math.radians(point2['lng'] - point1['lng'])

    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diff_long))
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)

    # Convert to compass bearing
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing


car_icon = {
    "iconUrl": "/assets/car.png",
    "iconSize": [15, 25],
    "iconAnchor": [10, 10],
    "popupAnchor": [0, 0],
}

component = html.Div([
    dl.Map([
        dl.TileLayer(),
        dl.AntPath(
            positions=[],  # Start empty
            id='track-path',
            color="#0000FF",
            pulseColor="#FFFFFF",
            delay=800,
            weight=10,
            dashArray=[1, 100],
        ),
        dl.RotatedMarker(
            position=track_data[0],
            icon=car_icon,
            rotationOrigin='center',
            rotationAngle=90,
            id='moving-marker'
        ),
    ],
        style={'width': '100%', 'height': '600px'},
        center=track_data[0],

        zoom=15,
        id='map',
        className='leaflet-container'
    ),

    # Updated control panel with slider
    html.Div([
        # Button container
        html.Div([
            html.Button('Play', id='play-button', n_clicks=0),
            html.Button('Stop', id='stop-button', n_clicks=0),
            html.Button('Restart', id='restart-button', n_clicks=0),
        ], style={'marginBottom': '10px'}),

        # Slider container
        html.Div([
            html.Label('Speed Control:', style={'marginRight': '10px'}),
            dcc.Slider(
                id='speed-slider',
                min=0.5,
                max=10,
                step=0.5,
                value=1,
                marks={i: f'{i}x' for i in range(1, 11)},
            )
        ], style={'width': '300px', 'margin': 'auto', 'display': 'none'})
    ], style={'margin': '10px', 'textAlign': 'center'}),
    dcc.Store(id='traveled-path', data=[track_data[0]]),  # Start with just the first point


    dcc.Store(id='track-data', data=track_data),
    dcc.Store(id='animation-state',
              data={'playing': False, 'current_index': 0, 'bearing': 0}),
    dcc.Interval(
        id='animation-interval',
        interval=50,  # This will be updated by the slider
        disabled=True
    ),
])


@callback(
    Output('animation-interval', 'interval'),
    Input('speed-slider', 'value')
)
def update_interval(speed_value):
    # Convert speed value to interval
    # Speed 1 = 200ms interval (slow)
    # Speed 10 = 20ms interval (fast)
    base_interval = 200
    interval = base_interval / speed_value
    return interval

@callback(
    [Output('animation-interval', 'disabled'),
     Output('animation-state', 'data'),
     Output('track-path', 'positions')],  # Add this output
    [Input('play-button', 'n_clicks'),
     Input('stop-button', 'n_clicks'),
     Input('restart-button', 'n_clicks')],
    [State('animation-state', 'data')]
)
def control_animation(play_clicks, stop_clicks, restart_clicks, animation_state):
    ctx = dash.callback_context
    if not ctx.triggered:
        return True, animation_state, [[track_data[0]['lat'], track_data[0]['lng']]]

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'play-button':
        animation_state['playing'] = True
        # Get current traveled path
        traveled_path = track_data[:animation_state['current_index'] + 1]
        traveled_positions = [[p['lat'], p['lng']] for p in traveled_path]
        return False, animation_state, traveled_positions
    elif button_id == 'stop-button':
        animation_state['playing'] = False
        # Keep current traveled path
        traveled_path = track_data[:animation_state['current_index'] + 1]
        traveled_positions = [[p['lat'], p['lng']] for p in traveled_path]
        return True, animation_state, traveled_positions
    elif button_id == 'restart-button':
        animation_state['playing'] = False
        animation_state['current_index'] = 0
        animation_state['bearing'] = 0
        # Reset to just the first point
        return True, animation_state, [[track_data[0]['lat'], track_data[0]['lng']]]

    return True, animation_state, [[track_data[0]['lat'], track_data[0]['lng']]]

@callback(
    [Output('moving-marker', 'position'),
     Output('moving-marker', 'rotationAngle'),
     Output('map', 'viewport'),
     Output('track-path', 'positions', allow_duplicate=True),  # Add this output
     Output('animation-state', 'data', allow_duplicate=True)],
    [Input('animation-interval', 'n_intervals')],
    [State('animation-state', 'data'),
     State('track-data', 'data')],
    prevent_initial_call=True
)
def update_marker_position(n_intervals, animation_state, track_data):
    if animation_state['playing']:
        current_index = animation_state['current_index']

        if current_index < len(track_data) - 1:
            current_position = track_data[current_index]
            next_position = track_data[current_index + 1]

            # Skip identical consecutive points
            while (current_index < len(track_data) - 2 and
                   current_position['lat'] == next_position['lat'] and
                   current_position['lng'] == next_position['lng']):
                current_index += 1
                next_position = track_data[current_index + 1]

            # Calculate rotation angle for marker
            bearing = calculate_bearing(current_position, next_position)
            animation_state['bearing'] = bearing

            print(f"Moving marker - Current Index: {current_index}")
            print(f"Current Position: {current_position}")
            print(f"Next Position: {next_position}")
            print(f"Bearing: {bearing}")

            viewport = {
                "center": [current_position['lat'], current_position['lng']],
                "zoom": 17
            }

            # Get the traveled path up to current position
            traveled_path = track_data[:current_index + 1]

            # Convert points to [lat, lng] format for AntPath
            traveled_positions = [[p['lat'], p['lng']] for p in traveled_path]

            current_index += 1
            animation_state['current_index'] = current_index

            return [current_position['lat'],
                    current_position['lng']], bearing, viewport, traveled_positions, animation_state
        else:
            # We've reached the end of the track
            current_position = track_data[-1]
            animation_state['playing'] = False

            viewport = {
                "center": [current_position['lat'], current_position['lng']],
                "zoom": 17
            }

            # Show complete path at end
            traveled_positions = [[p['lat'], p['lng']] for p in track_data]

            return ([current_position['lat'], current_position['lng']],
                    animation_state['bearing'],
                    viewport,
                    traveled_positions,
                    animation_state)

    # When not playing, keep current position and rotation
    current_position = track_data[animation_state['current_index']]
    viewport = {
        "center": [current_position['lat'], current_position['lng']],
        "zoom": 15
    }

    # Show path up to current position
    traveled_path = track_data[:animation_state['current_index'] + 1]
    traveled_positions = [[p['lat'], p['lng']] for p in traveled_path]

    return ([current_position['lat'], current_position['lng']],
            animation_state.get('bearing', 0),
            viewport,
            traveled_positions,
            animation_state)