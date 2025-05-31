import dash
from dash import html, dcc, callback, Input, Output, State, clientside_callback
import dash_leaflet as dl
import math
import uuid # For generating unique IDs for bullets and enemies

# --- Configuration ---
INITIAL_LAT = 28.142941
INITIAL_LNG = -96.9760726
INITIAL_ZOOM = 17
MOVEMENT_STEP = 0.00015  # Player speed
PLAYER_BULLET_SPEED = 0.0005
ENEMY_MOVEMENT_STEP = 0.00005 # Enemy speed (slower than player)
ENEMY_BULLET_SPEED = 0.0003
UPDATE_INTERVAL_MS = 50
COLLISION_THRESHOLD_PLAYER = 0.00018 # Increased hitbox for player
COLLISION_THRESHOLD_ENEMY = 0.00015
MIN_ENEMY_DISTANCE_TO_PLAYER = 0.0005 # Enemies stop if they get this close

CAR_ICON_URL = "/assets/car.png"
CAR_ICON_SIZE = [30, 50]
CAR_ICON_ANCHOR = [15, 25]

ENEMY_ICON_URL = "/assets/enemy_car.png"
ENEMY_ICON_SIZE = [30, 50]
ENEMY_ICON_ANCHOR = [15, 25]

PLAYER_BULLET_ICON = {
    "iconUrl": "/assets/bullet.png",
    "iconSize": [10, 10],
    "iconAnchor": [5, 5],
}
ENEMY_BULLET_ICON = {
    "iconUrl": "/assets/bullet.png", # Using same bullet icon for now
    "iconSize": [10, 10],
    "iconAnchor": [5, 5],
}

# --- Helper Functions ---
def calculate_bearing(point1, point2):
    lat1 = math.radians(point1['lat'])
    lat2 = math.radians(point2['lat'])
    diff_long = math.radians(point2['lng'] - point1['lng'])
    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diff_long))
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    return (initial_bearing + 360) % 360

def move_point_on_bearing(lat, lng, bearing_degrees, distance_degrees):
    bearing_rad = math.radians(bearing_degrees)
    # More accurate for small distances, especially near poles, but simplified here
    # For a more robust solution, Haversine or Vincenty's formulae are better
    # but for small steps on a map like this, this approximation is often acceptable.
    delta_lat = distance_degrees * math.cos(bearing_rad)
    delta_lng = distance_degrees * math.sin(bearing_rad) / math.cos(math.radians(lat)) # Correction for longitude
    new_lat = lat + delta_lat
    new_lng = lng + delta_lng
    return new_lat, new_lng

def get_initial_enemies():
    return [
        # Original 3
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.005, 'lng': INITIAL_LNG + 0.005, 'angle': 0, 'active': True, 'shoot_cooldown': 50, 'enemy_shoot_interval': 100},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.005, 'lng': INITIAL_LNG - 0.003, 'angle': 0, 'active': True, 'shoot_cooldown': 80, 'enemy_shoot_interval': 120},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.002, 'lng': INITIAL_LNG - 0.006, 'angle': 0, 'active': True, 'shoot_cooldown': 20, 'enemy_shoot_interval': 90},
        # Added 7 more
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.007, 'lng': INITIAL_LNG + 0.001, 'angle': 0, 'active': True, 'shoot_cooldown': 60, 'enemy_shoot_interval': 110},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.007, 'lng': INITIAL_LNG - 0.001, 'angle': 0, 'active': True, 'shoot_cooldown': 70, 'enemy_shoot_interval': 105},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.001, 'lng': INITIAL_LNG + 0.007, 'angle': 0, 'active': True, 'shoot_cooldown': 40, 'enemy_shoot_interval': 95},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.001, 'lng': INITIAL_LNG - 0.007, 'angle': 0, 'active': True, 'shoot_cooldown': 90, 'enemy_shoot_interval': 130},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.006, 'lng': INITIAL_LNG - 0.004, 'angle': 0, 'active': True, 'shoot_cooldown': 30, 'enemy_shoot_interval': 85},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.004, 'lng': INITIAL_LNG + 0.006, 'angle': 0, 'active': True, 'shoot_cooldown': 100, 'enemy_shoot_interval': 140},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.000, 'lng': INITIAL_LNG + 0.008, 'angle': 0, 'active': True, 'shoot_cooldown': 55, 'enemy_shoot_interval': 115},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.008, 'lng': INITIAL_LNG + 0.000, 'angle': 0, 'active': True, 'shoot_cooldown': 65, 'enemy_shoot_interval': 125},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.008, 'lng': INITIAL_LNG - 0.000, 'angle': 0, 'active': True, 'shoot_cooldown': 75, 'enemy_shoot_interval': 135},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.000, 'lng': INITIAL_LNG - 0.008, 'angle': 0, 'active': True, 'shoot_cooldown': 85, 'enemy_shoot_interval': 145},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.009, 'lng': INITIAL_LNG + 0.002, 'angle': 0, 'active': True, 'shoot_cooldown': 95, 'enemy_shoot_interval': 155},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.002, 'lng': INITIAL_LNG - 0.009, 'angle': 0, 'active': True, 'shoot_cooldown': 105, 'enemy_shoot_interval': 165},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.003, 'lng': INITIAL_LNG + 0.009, 'angle': 0, 'active': True, 'shoot_cooldown': 115, 'enemy_shoot_interval': 175},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.009, 'lng': INITIAL_LNG - 0.003, 'angle': 0, 'active': True, 'shoot_cooldown': 125, 'enemy_shoot_interval': 185},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.004, 'lng': INITIAL_LNG + 0.008, 'angle': 0, 'active': True, 'shoot_cooldown': 135, 'enemy_shoot_interval': 195},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.008, 'lng': INITIAL_LNG + 0.004, 'angle': 0, 'active': True, 'shoot_cooldown': 145, 'enemy_shoot_interval': 205},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.005, 'lng': INITIAL_LNG - 0.007, 'angle': 0, 'active': True, 'shoot_cooldown': 155, 'enemy_shoot_interval': 215},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.007, 'lng': INITIAL_LNG + 0.005, 'angle': 0, 'active': True, 'shoot_cooldown': 165, 'enemy_shoot_interval': 225},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.002, 'lng': INITIAL_LNG - 0.009, 'angle': 0, 'active': True, 'shoot_cooldown': 175, 'enemy_shoot_interval': 235},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.009, 'lng': INITIAL_LNG + 0.002, 'angle': 0, 'active': True, 'shoot_cooldown': 185, 'enemy_shoot_interval': 245},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.006, 'lng': INITIAL_LNG - 0.008, 'angle': 0, 'active': True, 'shoot_cooldown': 195, 'enemy_shoot_interval': 255},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.008, 'lng': INITIAL_LNG + 0.006, 'angle': 0, 'active': True, 'shoot_cooldown': 205, 'enemy_shoot_interval': 265},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.001, 'lng': INITIAL_LNG - 0.005, 'angle': 0, 'active': True, 'shoot_cooldown': 215, 'enemy_shoot_interval': 275},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.005, 'lng': INITIAL_LNG + 0.001, 'angle': 0, 'active': True, 'shoot_cooldown': 225, 'enemy_shoot_interval': 285},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.003, 'lng': INITIAL_LNG - 0.006, 'angle': 0, 'active': True, 'shoot_cooldown': 235, 'enemy_shoot_interval': 295},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.006, 'lng': INITIAL_LNG + 0.003, 'angle': 0, 'active': True, 'shoot_cooldown': 245, 'enemy_shoot_interval': 305},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT + 0.004, 'lng': INITIAL_LNG - 0.002, 'angle': 0, 'active': True, 'shoot_cooldown': 255, 'enemy_shoot_interval': 315},
        {'id': str(uuid.uuid4()), 'lat': INITIAL_LAT - 0.002, 'lng': INITIAL_LNG + 0.004, 'angle': 0, 'active': True, 'shoot_cooldown': 265, 'enemy_shoot_interval': 325},
    ]

INITIAL_GAME_STATE = {
    'score': 0,
    'game_over': False,
    'next_bullet_id': 0,
    'player_shoot_cooldown': 0,
    'player_shoot_interval': 15 # Player can shoot roughly every 15*50ms = 0.75 seconds
}

# --- Dash App Initialization ---
app = dash.Dash(__name__, assets_folder='assets')

# --- App Layout ---
app.layout = html.Div([
    dl.Map([
        dl.TileLayer(
            url="https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}",
            minZoom=0, maxZoom=16, attribution="USGS"),
        dl.TileLayer(
            url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            minZoom=17, maxZoom=19, attribution="Esri"),
        dl.RotatedMarker(
            position=[INITIAL_LAT, INITIAL_LNG],
            icon={"iconUrl": CAR_ICON_URL, "iconSize": CAR_ICON_SIZE, "iconAnchor": CAR_ICON_ANCHOR},
            rotationOrigin='center center', rotationAngle=0, id='moving-marker'
        ),
        dl.LayerGroup(id='enemy-layer'),
        dl.LayerGroup(id='player-bullet-layer'),
        dl.LayerGroup(id='enemy-bullet-layer'),
    ],
        style={'width': '100%', 'height': '80vh'},
        center=[INITIAL_LAT, INITIAL_LNG], zoom=INITIAL_ZOOM, id='map',
    ),
    dcc.Store(id='marker-state', data={'lat': INITIAL_LAT, 'lng': INITIAL_LNG, 'angle': 0}),
    dcc.Store(id='key-press-store', data={
        'ArrowUp': False, 'ArrowDown': False, 'ArrowLeft': False, 'ArrowRight': False,
        'Space': False, 'last_direction_key': None
    }),
    dcc.Store(id='player-bullets-store', data=[]),
    dcc.Store(id='enemy-cars-store', data=get_initial_enemies()),
    dcc.Store(id='enemy-bullets-store', data=[]),
    dcc.Store(id='game-state-store', data=INITIAL_GAME_STATE.copy()),
    dcc.Interval(id='movement-interval', interval=UPDATE_INTERVAL_MS, n_intervals=0),
    html.Div(id='dummy-input-for-clientside', style={'display': 'none'}),
    html.Div(id='dummy-output-for-clientside', style={'display': 'none'}),
    html.Div([
        html.Div(id='status-display', style={'fontSize': '18px', 'fontFamily': 'monospace', 'marginBottom':'10px'}),
        html.Button('Reset Game', id='reset-button', n_clicks=0)
    ], style={'padding': '10px', 'textAlign': 'center'}),
])

# --- Client-side Callback to Capture Key Presses (Arrows + Space) ---
app.clientside_callback(
    """
    function(dummy_input_value) {
        const dc = window.dash_clientside;
        if (!dc) { console.error("CRITICAL: window.dash_clientside is not available."); return; }
        const store_id = 'key-press-store';

        if (!window.dash_live_key_state_game_v2) { // Changed window variable name to ensure fresh init if structure changed
            if (!dc.callback_context || !dc.callback_context.states) {
                console.error("ERROR: dc.callback_context or states not available for initial store data.", dc);
                return dc.no_update;
            }
            let initial_store_data = dc.callback_context.states[store_id + '.data'];
            if (typeof initial_store_data === 'undefined' || initial_store_data === null) {
                initial_store_data = { ArrowUp: false, ArrowDown: false, ArrowLeft: false, ArrowRight: false, Space: false, last_direction_key: null };
            }
            window.dash_live_key_state_game_v2 = JSON.parse(JSON.stringify(initial_store_data));
        }

        const live_key_state = window.dash_live_key_state_game_v2;

        if (!window.dash_game_key_listeners_attached_v2) { // Changed window variable name
            window.dash_game_key_listeners_attached_v2 = true;

            document.addEventListener('keydown', (event) => {
                const valid_keys = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'];
                if (valid_keys.includes(event.key)) {
                    event.preventDefault();
                    let changed = false;
                    if (!live_key_state[event.key]) {
                        live_key_state[event.key] = true;
                        changed = true;
                    }
                    // For movement keys, update last_direction_key
                    if (event.key !== 'Space' && live_key_state.last_direction_key !== event.key) {
                        live_key_state.last_direction_key = event.key;
                        changed = true; // This ensures update even if key was already true (e.g. switching direction)
                    }
                    if (changed) {
                        if (dc && typeof dc.set_props === 'function') {
                            dc.set_props(store_id, { data: JSON.parse(JSON.stringify(live_key_state)) });
                        } else { console.error('ERROR keydown: dc.set_props missing.', dc); }
                    }
                }
            });

            document.addEventListener('keyup', (event) => {
                const valid_keys = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'];
                if (valid_keys.includes(event.key)) {
                    event.preventDefault();
                    if (live_key_state[event.key]) { // Only update if it was true
                        live_key_state[event.key] = false;
                         if (dc && typeof dc.set_props === 'function') {
                            dc.set_props(store_id, { data: JSON.parse(JSON.stringify(live_key_state)) });
                        } else { console.error('ERROR keyup: dc.set_props missing.', dc); }
                    }
                }
            });
        }
        return dc.no_update;
    }
    """,
    Output('dummy-output-for-clientside', 'children'),
    Input('dummy-input-for-clientside', 'children'),
    State('key-press-store', 'data')
)

# --- Main Game Loop Callback ---
@callback(
    [Output('moving-marker', 'position'),
     Output('moving-marker', 'rotationAngle'),
     Output('map', 'center'),
     Output('marker-state', 'data'),
     Output('status-display', 'children'),
     Output('player-bullets-store', 'data'),
     Output('enemy-cars-store', 'data'),
     Output('enemy-bullets-store', 'data'),
     Output('game-state-store', 'data'),
     Output('enemy-layer', 'children'),
     Output('player-bullet-layer', 'children'),
     Output('enemy-bullet-layer', 'children')],
    [Input('movement-interval', 'n_intervals'),
     Input('reset-button', 'n_clicks')],
    [State('key-press-store', 'data'),
     State('marker-state', 'data'),
     State('player-bullets-store', 'data'),
     State('enemy-cars-store', 'data'),
     State('enemy-bullets-store', 'data'),
     State('game-state-store', 'data')]
)
def game_loop(n_intervals, reset_clicks, key_status, marker_state,
              player_bullets, enemy_cars, enemy_bullets, game_state):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'reset-button':
        marker_state = {'lat': INITIAL_LAT, 'lng': INITIAL_LNG, 'angle': 0}
        player_bullets = []
        enemy_cars = get_initial_enemies()
        enemy_bullets = []
        game_state = INITIAL_GAME_STATE.copy()


    if game_state.get('game_over', False) and triggered_id != 'reset-button':
        status_text = f"GAME OVER! Final Score: {game_state['score']}. Press Reset."
        enemy_markers = [
            dl.RotatedMarker(position=[e['lat'], e['lng']], icon={"iconUrl": ENEMY_ICON_URL, "iconSize": ENEMY_ICON_SIZE, "iconAnchor": ENEMY_ICON_ANCHOR}, rotationAngle=e['angle'])
            for e in enemy_cars if e['active']
        ]
        player_bullet_markers = [dl.Marker(position=[b['lat'], b['lng']], icon=PLAYER_BULLET_ICON) for b in player_bullets]
        enemy_bullet_markers = [dl.Marker(position=[b['lat'], b['lng']], icon=ENEMY_BULLET_ICON) for b in enemy_bullets]
        return (
            [marker_state['lat'], marker_state['lng']], marker_state['angle'],
            [marker_state['lat'], marker_state['lng']],
            marker_state, status_text, player_bullets, enemy_cars, enemy_bullets, game_state,
            enemy_markers, player_bullet_markers, enemy_bullet_markers
        )

    # --- Player Movement ---
    current_lat, current_lng, current_angle = marker_state['lat'], marker_state['lng'], marker_state['angle']
    delta_lat, delta_lng, moved = 0, 0, False
    if key_status.get('ArrowUp'): delta_lat += MOVEMENT_STEP; moved = True
    if key_status.get('ArrowDown'): delta_lat -= MOVEMENT_STEP; moved = True
    if key_status.get('ArrowLeft'): delta_lng -= MOVEMENT_STEP; moved = True
    if key_status.get('ArrowRight'): delta_lng += MOVEMENT_STEP; moved = True

    new_player_lat, new_player_lng = current_lat + delta_lat, current_lng + delta_lng
    new_player_angle = current_angle
    if moved and (current_lat != new_player_lat or current_lng != new_player_lng):
        new_player_angle = calculate_bearing({'lat': current_lat, 'lng': current_lng}, {'lat': new_player_lat, 'lng': new_player_lng})
    marker_state = {'lat': new_player_lat, 'lng': new_player_lng, 'angle': new_player_angle}
    map_center = [new_player_lat, new_player_lng]

    # --- Player Shooting Cooldown ---
    game_state['player_shoot_cooldown'] = max(0, game_state.get('player_shoot_cooldown', 0) - 1)

    # --- Player Shooting ---
    if key_status.get('Space') and game_state['player_shoot_cooldown'] == 0:
        bullet_id = game_state['next_bullet_id']
        game_state['next_bullet_id'] +=1
        player_bullets.append({
            'id': f"pb_{bullet_id}", 'lat': new_player_lat, 'lng': new_player_lng, 'angle': new_player_angle
        })
        game_state['player_shoot_cooldown'] = game_state['player_shoot_interval'] # Reset cooldown

    # --- Bullet Movement (Player) ---
    active_player_bullets = []
    for bullet in player_bullets:
        b_lat, b_lng = move_point_on_bearing(bullet['lat'], bullet['lng'], bullet['angle'], PLAYER_BULLET_SPEED)
        if abs(b_lat - INITIAL_LAT) < 0.1 and abs(b_lng - INITIAL_LNG) < 0.1: # Basic boundary check
             active_player_bullets.append({'id': bullet['id'], 'lat': b_lat, 'lng': b_lng, 'angle': bullet['angle']})
    player_bullets = active_player_bullets

    # --- Enemy Logic ---
    updated_enemy_cars = []
    for enemy in enemy_cars:
        if not enemy['active']:
            updated_enemy_cars.append(enemy)
            continue

        # Enemy Movement (Follow Player)
        dist_to_player = math.hypot(new_player_lat - enemy['lat'], new_player_lng - enemy['lng'])
        enemy_new_lat, enemy_new_lng = enemy['lat'], enemy['lng']

        if dist_to_player > MIN_ENEMY_DISTANCE_TO_PLAYER: # Only move if not too close
            bearing_to_player = calculate_bearing({'lat': enemy['lat'], 'lng': enemy['lng']}, {'lat': new_player_lat, 'lng': new_player_lng})
            enemy_new_lat, enemy_new_lng = move_point_on_bearing(enemy['lat'], enemy['lng'], bearing_to_player, ENEMY_MOVEMENT_STEP)
            enemy['angle'] = bearing_to_player # Enemy faces direction of movement/player
        elif dist_to_player > 0: # if not on top of player, still face player
             enemy['angle'] = calculate_bearing({'lat': enemy['lat'], 'lng': enemy['lng']}, {'lat': new_player_lat, 'lng': new_player_lng})


        enemy['lat'], enemy['lng'] = enemy_new_lat, enemy_new_lng

        # Enemy Shooting
        enemy['shoot_cooldown'] = max(0, enemy.get('shoot_cooldown',0) - 1)
        if enemy['shoot_cooldown'] == 0:
            # Aim at player (angle already updated if moving, or re-calculate if stationary and aiming)
            angle_for_shot = calculate_bearing({'lat': enemy['lat'], 'lng': enemy['lng']}, {'lat': new_player_lat, 'lng': new_player_lng})

            bullet_id = game_state['next_bullet_id']
            game_state['next_bullet_id'] +=1
            enemy_bullets.append({
                'id': f"eb_{bullet_id}", 'lat': enemy['lat'], 'lng': enemy['lng'], 'angle': angle_for_shot
            })
            enemy['shoot_cooldown'] = enemy.get('enemy_shoot_interval', 100) # Reset enemy's specific cooldown
        updated_enemy_cars.append(enemy)
    enemy_cars = updated_enemy_cars


    # --- Bullet Movement (Enemy) ---
    current_enemy_bullets_next_frame = []
    for bullet in enemy_bullets:
        b_lat, b_lng = move_point_on_bearing(bullet['lat'], bullet['lng'], bullet['angle'], ENEMY_BULLET_SPEED)
        if abs(b_lat - INITIAL_LAT) < 0.1 and abs(b_lng - INITIAL_LNG) < 0.1: # Basic boundary check
            current_enemy_bullets_next_frame.append({'id': bullet['id'], 'lat': b_lat, 'lng': b_lng, 'angle': bullet['angle']})
    enemy_bullets = current_enemy_bullets_next_frame

    # --- Collision Detection ---
    # 1. Player bullets vs Enemies
    enemies_after_hits = []
    for enemy in enemy_cars:
        if not enemy['active']:
            enemies_after_hits.append(enemy)
            continue
        hit_by_player = False
        surviving_player_bullets = []
        for p_bullet in player_bullets:
            dist_to_enemy = math.hypot(p_bullet['lat'] - enemy['lat'], p_bullet['lng'] - enemy['lng'])
            if dist_to_enemy < COLLISION_THRESHOLD_ENEMY:
                hit_by_player = True
                game_state['score'] += 10
                # Bullet is consumed, don't add to surviving_player_bullets
            else:
                surviving_player_bullets.append(p_bullet)
        player_bullets = surviving_player_bullets # Update player_bullets after checking against one enemy

        if hit_by_player:
            enemy['active'] = False # Mark enemy as inactive
            # Don't add to enemies_after_hits if we want them removed immediately,
            # or add with active=False if we want to keep them in the list but not render/interact.
            # Current logic correctly adds it with active=False
        enemies_after_hits.append(enemy)
    enemy_cars = enemies_after_hits

    # 2. Enemy bullets vs Player
    if not game_state.get('game_over', False):
        surviving_enemy_bullets = []
        player_hit_this_frame = False
        for e_bullet in enemy_bullets:
            if player_hit_this_frame: # If player already hit in this frame by another bullet, keep remaining bullets
                surviving_enemy_bullets.append(e_bullet)
                continue

            dist_to_player = math.hypot(e_bullet['lat'] - new_player_lat, e_bullet['lng'] - new_player_lng)
            if dist_to_player < COLLISION_THRESHOLD_PLAYER:
                game_state['game_over'] = True
                player_hit_this_frame = True # Mark player as hit
                # Bullet is consumed, don't add to surviving_enemy_bullets
            else:
                surviving_enemy_bullets.append(e_bullet)
        enemy_bullets = surviving_enemy_bullets

    # --- Status Update ---
    if game_state.get('game_over'):
        status_text = f"GAME OVER! Score: {game_state['score']}. Press Reset."
    else:
        status_text = f"Score: {game_state['score']} | Player Lat: {new_player_lat:.4f}, Lng: {new_player_lng:.4f} | Cooldown: {game_state['player_shoot_cooldown']}"

    # --- Prepare Markers for Rendering ---
    enemy_markers = [
        dl.RotatedMarker(position=[e['lat'], e['lng']], icon={"iconUrl": ENEMY_ICON_URL, "iconSize": ENEMY_ICON_SIZE, "iconAnchor": ENEMY_ICON_ANCHOR}, rotationAngle=e['angle'], id=f"enemy-{e['id']}")
        for e in enemy_cars if e['active']
    ]
    player_bullet_markers = [dl.Marker(position=[b['lat'], b['lng']], icon=PLAYER_BULLET_ICON, id=f"pbullet-{b['id']}") for b in player_bullets]
    enemy_bullet_markers = [dl.Marker(position=[b['lat'], b['lng']], icon=ENEMY_BULLET_ICON, id=f"ebullet-{b['id']}") for b in enemy_bullets]

    return (
        [new_player_lat, new_player_lng], new_player_angle, map_center, marker_state, status_text,
        player_bullets, enemy_cars, enemy_bullets, game_state,
        enemy_markers, player_bullet_markers, enemy_bullet_markers
    )

if __name__ == '__main__':
    app.run_server(debug=True, port=4333)