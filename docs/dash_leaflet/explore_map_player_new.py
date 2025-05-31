import dash
from dash import html, dcc, callback, Input, Output, State, clientside_callback
import dash_leaflet as dl
import math
import uuid
import json
import os
import numpy as np
from shapely.geometry import Point, LineString
# from shapely.ops import nearest_points # Not used in current code
import networkx as nx

# from collections import defaultdict # Not used in current code

# --- Configuration ---
INITIAL_LAT = 28.142941
INITIAL_LNG = -96.9760726
INITIAL_ZOOM = 17
MOVEMENT_STEP = 0.0002  # Player speed along roads
PLAYER_BULLET_SPEED = 0.0005
ENEMY_MOVEMENT_STEP = 0.00008  # Enemy speed along roads
ENEMY_BULLET_SPEED = 0.0003
UPDATE_INTERVAL_MS = 50
COLLISION_THRESHOLD_PLAYER = 0.00018
COLLISION_THRESHOLD_ENEMY = 0.00015
MIN_ENEMY_DISTANCE_TO_PLAYER = 0.0005  # For non-road fallback or close encounters
ROAD_SNAP_DISTANCE = 0.005
INTERSECTION_THRESHOLD = 0.0001

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
    "iconUrl": "/assets/bullet.png",
    "iconSize": [10, 10],
    "iconAnchor": [5, 5],
}


# --- Road Network Management ---
class RoadNetwork:
    def __init__(self, road_json_path):
        with open(road_json_path, 'r') as f:
            self.road_segments_data = json.load(f)  # Renamed to avoid conflict

        self.graph = nx.Graph()
        self.road_lines = []
        self.segment_to_coords = {}
        self.node_to_coords = {}
        self.coords_to_node = {}  # Using string keys for lat,lng
        self.build_network()

    def build_network(self):
        node_id_counter = 0
        for seg_idx, segment_coords_list in enumerate(self.road_segments_data):
            if len(segment_coords_list) < 2:
                continue
            self.segment_to_coords[seg_idx] = segment_coords_list
            line_coords_for_shapely = [(lng, lat) for lat, lng in segment_coords_list]
            self.road_lines.append(LineString(line_coords_for_shapely))

            prev_node_id = None
            for lat, lng in segment_coords_list:
                coord_key = f"{lat:.6f},{lng:.6f}"  # Create a string key for the dictionary
                if coord_key in self.coords_to_node:
                    current_node_id = self.coords_to_node[coord_key]
                else:
                    current_node_id = node_id_counter
                    self.graph.add_node(current_node_id, lat=lat, lng=lng)
                    self.node_to_coords[current_node_id] = (lat, lng)
                    self.coords_to_node[coord_key] = current_node_id
                    node_id_counter += 1

                if prev_node_id is not None and prev_node_id != current_node_id:
                    distance = self.calculate_distance(
                        self.node_to_coords[prev_node_id],
                        self.node_to_coords[current_node_id]
                    )
                    self.graph.add_edge(prev_node_id, current_node_id, weight=distance, segment_idx=seg_idx)
                prev_node_id = current_node_id

    def calculate_distance(self, coord1, coord2):
        lat1, lng1 = coord1
        lat2, lng2 = coord2
        return math.sqrt((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2)

    def find_nearest_road_point(self, lat, lng):
        point = Point(lng, lat)  # Shapely uses (x,y) which is (lng, lat)
        min_distance = float('inf')
        nearest_road_point_geom = None
        nearest_segment_idx = None

        if not self.road_lines:  # Handle case with no roads loaded
            return None, None, None

        for i, line in enumerate(self.road_lines):
            # Project point onto line and find the point on the line closest to the given point
            projected_point_on_line = line.interpolate(line.project(point))
            distance = point.distance(projected_point_on_line)

            if distance < min_distance:
                min_distance = distance
                nearest_road_point_geom = projected_point_on_line
                nearest_segment_idx = i

        if nearest_road_point_geom is None or min_distance > ROAD_SNAP_DISTANCE:
            return None, None, None

        return nearest_road_point_geom.y, nearest_road_point_geom.x, nearest_segment_idx  # lat, lng

    def find_nearest_node(self, lat, lng):
        min_dist_sq = float('inf')
        found_node = None
        for node_id, (node_lat, node_lng) in self.node_to_coords.items():
            dist_sq = (lat - node_lat) ** 2 + (lng - node_lng) ** 2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                found_node = node_id
        return found_node

    def get_path_to_target(self, start_lat, start_lng, target_lat, target_lng):
        start_node = self.find_nearest_node(start_lat, start_lng)
        target_node = self.find_nearest_node(target_lat, target_lng)

        if start_node is None or target_node is None or start_node == target_node:
            return []
        try:
            path_nodes = nx.shortest_path(self.graph, source=start_node, target=target_node, weight='weight')
            return [self.node_to_coords[node] for node in path_nodes]
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

    def move_along_road(self, current_lat, current_lng, desired_target_lat, desired_target_lng, step_size,
                        current_player_angle, current_segment_idx_hint=None):
        # print(f"  move_along_road: cur=({current_lat:.5f},{current_lng:.5f}), desired_target=({desired_target_lat:.5f},{desired_target_lng:.5f}), angle={current_player_angle:.1f}")
        snapped_lat, snapped_lng, actual_segment_idx = self.find_nearest_road_point(current_lat, current_lng)

        if snapped_lat is None:
            # print("  move_along_road: Too far from any road.")
            return current_lat, current_lng, current_player_angle, current_segment_idx_hint

        move_direction_rad = math.atan2(desired_target_lng - snapped_lng, desired_target_lat - snapped_lat)
        nearest_graph_node = self.find_nearest_node(snapped_lat, snapped_lng)

        if nearest_graph_node is None:
            # print("  move_along_road: No nearest graph node found.")
            return snapped_lat, snapped_lng, current_player_angle, actual_segment_idx

        best_score = -float('inf')
        candidate_next_pos = None
        candidate_segment_idx = actual_segment_idx

        for neighbor_node_id in self.graph.neighbors(nearest_graph_node):
            neighbor_lat, neighbor_lng = self.node_to_coords[neighbor_node_id]
            dir_to_neighbor_rad = math.atan2(neighbor_lng - snapped_lng, neighbor_lat - snapped_lat)
            angle_diff = abs(move_direction_rad - dir_to_neighbor_rad)
            if angle_diff > math.pi: angle_diff = 2 * math.pi - angle_diff
            score = math.cos(angle_diff)
            if score > best_score:
                best_score = score
                candidate_next_pos = (neighbor_lat, neighbor_lng)
                edge_data = self.graph.get_edge_data(nearest_graph_node, neighbor_node_id)
                if edge_data: candidate_segment_idx = edge_data.get('segment_idx', actual_segment_idx)

        if candidate_next_pos and best_score > -0.5:
            dist_to_candidate = self.calculate_distance((snapped_lat, snapped_lng), candidate_next_pos)
            moved_lat, moved_lng = snapped_lat, snapped_lng
            if dist_to_candidate < 1e-6:
                moved_lat, moved_lng = candidate_next_pos[0], candidate_next_pos[1]
            elif dist_to_candidate <= step_size:
                moved_lat, moved_lng = candidate_next_pos[0], candidate_next_pos[1]
            else:
                ratio = step_size / dist_to_candidate
                moved_lat = snapped_lat + (candidate_next_pos[0] - snapped_lat) * ratio
                moved_lng = snapped_lng + (candidate_next_pos[1] - snapped_lng) * ratio

            new_angle = current_player_angle
            if abs(moved_lat - snapped_lat) > 1e-7 or abs(moved_lng - snapped_lng) > 1e-7:
                new_angle = calculate_bearing({'lat': snapped_lat, 'lng': snapped_lng},
                                              {'lat': moved_lat, 'lng': moved_lng})
            # print(f"  move_along_road: Moved to ({moved_lat:.5f},{moved_lng:.5f}), new_angle={new_angle:.1f}")
            return moved_lat, moved_lng, new_angle, candidate_segment_idx
        else:
            # print("  move_along_road: No suitable move found, staying put.")
            return snapped_lat, snapped_lng, current_player_angle, actual_segment_idx


# Initialize road network
road_network = None
try:
    json_path = 'aransas_county.json'
    if os.path.exists(json_path):
        road_network = RoadNetwork(json_path)
        print(
            f"Successfully loaded road network with {len(road_network.road_segments_data)} segments and {road_network.graph.number_of_nodes()} nodes.")
    else:
        print(f"Warning: {json_path} not found. Game will run without road constraints.")
except Exception as e:
    print(f"Error loading road network: {e}")
    road_network = None


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
    delta_lat = distance_degrees * math.cos(bearing_rad)
    delta_lng = distance_degrees * math.sin(bearing_rad) / math.cos(math.radians(lat))
    new_lat = lat + delta_lat
    new_lng = lng + delta_lng
    return new_lat, new_lng


def snap_to_road(lat, lng):
    if road_network:
        road_lat, road_lng, _ = road_network.find_nearest_road_point(lat, lng)
        if road_lat is not None:
            return road_lat, road_lng
    return lat, lng


INITIAL_PLAYER_LAT, INITIAL_PLAYER_LNG = INITIAL_LAT, INITIAL_LNG
if road_network:
    snapped_lat, snapped_lng = snap_to_road(INITIAL_LAT, INITIAL_LNG)
    if snapped_lat is not None:
        INITIAL_PLAYER_LAT, INITIAL_PLAYER_LNG = snapped_lat, snapped_lng
        print(f"Initial player position (snapped): {INITIAL_PLAYER_LAT}, {INITIAL_PLAYER_LNG}")
    else:
        print(f"Initial player position (default, snapping failed): {INITIAL_PLAYER_LAT}, {INITIAL_PLAYER_LNG}")
else:
    print("No road network loaded - using default player position")


def get_initial_enemies():
    enemies = []
    initial_positions_data = [
        (INITIAL_LAT + 0.005, INITIAL_LNG + 0.005, 50, 90),
        (INITIAL_LAT - 0.005, INITIAL_LNG - 0.003, 80, 120),
        (INITIAL_LAT + 0.002, INITIAL_LNG - 0.006, 20, 100),
    ]
    for i, (lat, lng, cooldown, interval) in enumerate(initial_positions_data):
        e_lat, e_lng = snap_to_road(lat, lng)
        _, _, segment_idx = road_network.find_nearest_road_point(e_lat, e_lng) if road_network else (None, None, None)
        enemies.append({'id': str(uuid.uuid4()), 'lat': e_lat, 'lng': e_lng, 'angle': 0, 'active': True,
                        'shoot_cooldown': cooldown, 'enemy_shoot_interval': interval, 'current_segment': segment_idx})
    return enemies


INITIAL_GAME_STATE = {'score': 0, 'game_over': False, 'next_bullet_id': 0, 'player_shoot_cooldown': 0,
                      'player_shoot_interval': 15, 'player_segment': None}
if road_network:
    _, _, seg = road_network.find_nearest_road_point(INITIAL_PLAYER_LAT, INITIAL_PLAYER_LNG)
    INITIAL_GAME_STATE['player_segment'] = seg

app = dash.Dash(__name__, assets_folder='assets')

road_polylines_for_map = []
if road_network:
    for seg_coords in road_network.road_segments_data:
        if len(seg_coords) >= 2: road_polylines_for_map.append(
            dl.Polyline(positions=seg_coords, color='grey', weight=3, opacity=0.7))

app.layout = html.Div([
    dl.Map([
        dl.TileLayer(url="https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}",
                     minZoom=0, maxZoom=16, attribution="USGS"),
        dl.TileLayer(
            url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            minZoom=17, maxZoom=19, attribution="Esri"),
        dl.LayerGroup(road_polylines_for_map, id='road-layer'),
        dl.RotatedMarker(position=[INITIAL_PLAYER_LAT, INITIAL_PLAYER_LNG],
                         icon={"iconUrl": CAR_ICON_URL, "iconSize": CAR_ICON_SIZE, "iconAnchor": CAR_ICON_ANCHOR},
                         rotationOrigin='center center', rotationAngle=0, id='moving-marker'),
        dl.LayerGroup(id='enemy-layer'),
        dl.LayerGroup(id='player-bullet-layer'),
        dl.LayerGroup(id='enemy-bullet-layer'),
    ], style={'width': '100%', 'height': '80vh'}, center=[INITIAL_PLAYER_LAT, INITIAL_PLAYER_LNG], zoom=INITIAL_ZOOM,
        id='map'),
    dcc.Store(id='marker-state', data={'lat': INITIAL_PLAYER_LAT, 'lng': INITIAL_PLAYER_LNG, 'angle': 0}),
    dcc.Store(id='key-press-store',
              data={'ArrowUp': False, 'ArrowDown': False, 'ArrowLeft': False, 'ArrowRight': False, 'Space': False,
                    'last_direction_key': None}),
    dcc.Store(id='player-bullets-store', data=[]),
    dcc.Store(id='enemy-cars-store', data=get_initial_enemies()),
    dcc.Store(id='enemy-bullets-store', data=[]),
    dcc.Store(id='game-state-store', data=INITIAL_GAME_STATE.copy()),
    dcc.Interval(id='movement-interval', interval=UPDATE_INTERVAL_MS, n_intervals=0),
    html.Div(id='dummy-input-for-clientside', style={'display': 'none'}),
    html.Div(id='dummy-output-for-clientside', style={'display': 'none'}),
    html.Div([
        html.Div(id='status-display', style={'fontSize': '18px', 'fontFamily': 'monospace', 'marginBottom': '10px'}),
        html.Button('Reset Game', id='reset-button', n_clicks=0),
        html.Div("Use arrow keys to move, Space to shoot", style={'marginTop': '10px', 'fontSize': '14px'})
    ], style={'padding': '10px', 'textAlign': 'center'}),
])

app.clientside_callback(
    """
    function(dummy_input_value) {
        const dc = window.dash_clientside;
        if (!dc) { console.error("CRITICAL: window.dash_clientside is not available."); return dc.no_update; }
        const store_id = 'key-press-store';

        if (!window.dash_live_key_state_game_v3) {
            if (!dc.callback_context || !dc.callback_context.states || typeof dc.callback_context.states[store_id + '.data'] === 'undefined') {
                 window.dash_live_key_state_game_v3 = { ArrowUp: false, ArrowDown: false, ArrowLeft: false, ArrowRight: false, Space: false, last_direction_key: null };
            } else {
                 window.dash_live_key_state_game_v3 = JSON.parse(JSON.stringify(dc.callback_context.states[store_id + '.data']));
            }
            // console.log("Initialized window.dash_live_key_state_game_v3:", window.dash_live_key_state_game_v3);
        }

        const live_key_state = window.dash_live_key_state_game_v3;

        if (!window.dash_game_key_listeners_attached_v3) {
            window.dash_game_key_listeners_attached_v3 = true;
            // console.log("Attaching key listeners v3.");

            document.addEventListener('keydown', (event) => {
                const valid_keys = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '];
                const key_to_store = event.key === ' ' ? 'Space' : event.key;

                if (valid_keys.includes(event.key)) {
                    event.preventDefault();
                    let changed = false;
                    if (!live_key_state[key_to_store]) {
                        live_key_state[key_to_store] = true;
                        changed = true;
                    }
                    if (key_to_store !== 'Space' && live_key_state.last_direction_key !== key_to_store) {
                        live_key_state.last_direction_key = key_to_store;
                        changed = true;
                    }
                    if (changed) {
                        // console.log('Key down:', key_to_store, JSON.parse(JSON.stringify(live_key_state)));
                        if (dc && typeof dc.set_props === 'function') {
                            dc.set_props(store_id, { data: JSON.parse(JSON.stringify(live_key_state)) });
                        } else { console.error('ERROR keydown: dc.set_props missing.'); }
                    }
                }
            });

            document.addEventListener('keyup', (event) => {
                const valid_keys = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '];
                const key_to_store = event.key === ' ' ? 'Space' : event.key;

                if (valid_keys.includes(event.key)) {
                    event.preventDefault();
                    if (live_key_state[key_to_store]) {
                        live_key_state[key_to_store] = false;
                        // console.log('Key up:', key_to_store, JSON.parse(JSON.stringify(live_key_state)));
                         if (dc && typeof dc.set_props === 'function') {
                            dc.set_props(store_id, { data: JSON.parse(JSON.stringify(live_key_state)) });
                        } else { console.error('ERROR keyup: dc.set_props missing.'); }
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


# KEEP ALL YOUR EXISTING CODE ABOVE THIS @callback
# ONLY REPLACE THE game_loop FUNCTION

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
              player_bullets, enemy_cars_from_store, enemy_bullets_from_store,
              game_state_from_store):  # Renamed to avoid confusion

    # --- Create mutable copies from stores for this tick's logic ---
    # This is crucial to avoid modifying the Dash store data directly in unexpected ways
    # and to ensure we are working with fresh copies if reset happens.
    current_player_bullets = list(player_bullets)  # Or deepcopy if complex
    current_enemy_cars = [e.copy() for e in enemy_cars_from_store]  # Deep copy for list of dicts
    current_enemy_bullets = list(enemy_bullets_from_store)
    current_game_state = game_state_from_store.copy()
    current_marker_state = marker_state.copy()

    print(f"\n--- Tick {n_intervals} --- KeyStatus: {key_status}")
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(f"Trigger: {triggered_id}, Reset Clicks: {reset_clicks}")

    # Store the n_clicks from the previous callback invocation
    # This helps differentiate a new click from just the interval firing while n_clicks > 0
    # Note: This is a simple way; for more robust detection, you might compare timestamps or use a dedicated store.
    prev_reset_clicks = current_game_state.get('previous_reset_clicks', 0)

    if triggered_id == 'reset-button' and reset_clicks > prev_reset_clicks:
        print(">>> RESET BUTTON CLICKED - Reinitializing game state.")
        current_game_state['previous_reset_clicks'] = reset_clicks  # Update for next time

        snapped_lat, snapped_lng = INITIAL_LAT, INITIAL_LNG
        player_seg = None
        if road_network:
            r_lat, r_lng, seg = road_network.find_nearest_road_point(INITIAL_LAT, INITIAL_LNG)
            if r_lat is not None: snapped_lat, snapped_lng, player_seg = r_lat, r_lng, seg

        current_marker_state = {'lat': snapped_lat, 'lng': snapped_lng, 'angle': 0}
        current_player_bullets = []
        current_enemy_cars = get_initial_enemies()  # This reinitializes the list for this tick
        current_enemy_bullets = []
        current_game_state = INITIAL_GAME_STATE.copy()  # Get a fresh copy
        current_game_state['player_segment'] = player_seg
        current_game_state['previous_reset_clicks'] = reset_clicks  # Store current clicks

        print(f"RESET: Enemies generated: {len(current_enemy_cars)}")
        for i, enemy in enumerate(current_enemy_cars):
            print(f"  RESET Enemy {i}: active={enemy['active']}, pos=({enemy['lat']:.5f},{enemy['lng']:.5f})")
    else:
        # If not a new reset click, ensure 'previous_reset_clicks' is in game_state
        if 'previous_reset_clicks' not in current_game_state:
            current_game_state['previous_reset_clicks'] = reset_clicks

    if current_game_state.get('game_over', False) and not (
            triggered_id == 'reset-button' and reset_clicks > prev_reset_clicks):
        status_text = f"GAME OVER! Final Score: {current_game_state['score']}. Press Reset."
        print(">>> Game Over state (not during a fresh reset).")
        # Marker rendering logic for game over state
        active_enemies_for_render = [e for e in current_enemy_cars if e['active']]
        enemy_markers = [dl.RotatedMarker(id=str(uuid.uuid4()), position=[e['lat'], e['lng']],
                                          icon={"iconUrl": ENEMY_ICON_URL, "iconSize": ENEMY_ICON_SIZE,
                                                "iconAnchor": ENEMY_ICON_ANCHOR}, rotationAngle=e['angle']) for e in
                         active_enemies_for_render]
        player_bullet_markers = [dl.Marker(id=str(uuid.uuid4()), position=[b['lat'], b['lng']], icon=PLAYER_BULLET_ICON)
                                 for b in current_player_bullets]
        enemy_bullet_markers = [dl.Marker(id=str(uuid.uuid4()), position=[b['lat'], b['lng']], icon=ENEMY_BULLET_ICON)
                                for b in current_enemy_bullets]
        return (
            [current_marker_state['lat'], current_marker_state['lng']], current_marker_state['angle'],
            [current_marker_state['lat'], current_marker_state['lng']],  # map center
            current_marker_state, status_text, current_player_bullets, current_enemy_cars, current_enemy_bullets,
            current_game_state,
            enemy_markers, player_bullet_markers, enemy_bullet_markers
        )

    # --- Player Variables ---
    p_cur_lat, p_cur_lng, p_cur_angle = current_marker_state['lat'], current_marker_state['lng'], current_marker_state[
        'angle']
    p_new_lat, p_new_lng, p_new_angle = p_cur_lat, p_cur_lng, p_cur_angle  # Start with current state
    print(f"PLAYER: Start pos=({p_cur_lat:.5f},{p_cur_lng:.5f}), Angle: {p_cur_angle:.1f}")

    movement_requested = any(key_status.get(k) for k in ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'])
    print(
        f"PLAYER: Movement requested: {movement_requested}. Keys: U:{key_status.get('ArrowUp')} D:{key_status.get('ArrowDown')} L:{key_status.get('ArrowLeft')} R:{key_status.get('ArrowRight')}")

    if road_network:
        snapped_lat, snapped_lng, player_current_segment_idx = road_network.find_nearest_road_point(p_cur_lat,
                                                                                                    p_cur_lng)

        p_logic_lat, p_logic_lng = (snapped_lat, snapped_lng) if snapped_lat is not None else (p_cur_lat, p_cur_lng)
        if snapped_lat is not None:
            current_game_state['player_segment'] = player_current_segment_idx
            print(f"PLAYER: Snapped to: ({p_logic_lat:.5f},{p_logic_lng:.5f}) on seg {player_current_segment_idx}")
        else:
            print(f"PLAYER: Not snapped. Current pos: ({p_cur_lat:.5f},{p_cur_lng:.5f})")

        if movement_requested:
            if snapped_lat is not None:  # Player is on road and wants to move
                # Determine desired target direction based on key presses relative to current snapped position
                temp_desired_lat, temp_desired_lng = p_logic_lat, p_logic_lng
                if key_status.get('ArrowUp'): temp_desired_lat += 0.01  # Arbitrary offset to indicate direction
                if key_status.get('ArrowDown'): temp_desired_lat -= 0.01
                if key_status.get('ArrowLeft'): temp_desired_lng -= 0.01
                if key_status.get('ArrowRight'): temp_desired_lng += 0.01

                print(
                    f"  PLAYER: Attempting road movement from ({p_logic_lat:.5f},{p_logic_lng:.5f}) towards key direction approx ({temp_desired_lat:.5f},{temp_desired_lng:.5f}). Current angle: {p_cur_angle}")
                moved_lat, moved_lng, moved_angle, new_segment = road_network.move_along_road(
                    p_logic_lat, p_logic_lng, temp_desired_lat, temp_desired_lng,
                    MOVEMENT_STEP, p_cur_angle, current_game_state.get('player_segment'))

                if abs(moved_lat - p_logic_lat) > 1e-7 or abs(
                        moved_lng - p_logic_lng) > 1e-7:  # Check if actually moved
                    p_new_lat, p_new_lng, p_new_angle = moved_lat, moved_lng, moved_angle
                    print(
                        f"  PLAYER: Road movement SUCCESS. New pos=({p_new_lat:.5f},{p_new_lng:.5f}), Angle: {p_new_angle:.1f}, Seg: {new_segment}")
                else:
                    p_new_lat, p_new_lng, p_new_angle = p_logic_lat, p_logic_lng, p_cur_angle  # Stay at snapped if no move
                    print(f"  PLAYER: Road movement NO CHANGE. Staying at snapped ({p_new_lat:.5f},{p_new_lng:.5f})")
                current_game_state['player_segment'] = new_segment
            else:  # Player is not on road, but wants to move (free movement)
                print("  PLAYER: Attempting free movement (not snapped but keys pressed).")
                delta_lat_free, delta_lng_free = 0, 0
                if key_status.get('ArrowUp'): delta_lat_free += MOVEMENT_STEP
                if key_status.get('ArrowDown'): delta_lat_free -= MOVEMENT_STEP
                if key_status.get('ArrowLeft'): delta_lng_free -= MOVEMENT_STEP
                if key_status.get('ArrowRight'): delta_lng_free += MOVEMENT_STEP

                p_new_lat = p_cur_lat + delta_lat_free  # Move from original if not snapped
                p_new_lng = p_cur_lng + delta_lng_free
                if abs(delta_lat_free) > 1e-7 or abs(delta_lng_free) > 1e-7:
                    p_new_angle = calculate_bearing({'lat': p_cur_lat, 'lng': p_cur_lng},
                                                    {'lat': p_new_lat, 'lng': p_new_lng})
                    print(
                        f"  PLAYER: Free movement SUCCESS. New pos=({p_new_lat:.5f},{p_new_lng:.5f}), Angle: {p_new_angle:.1f}")
                else:
                    p_new_angle = p_cur_angle  # No actual movement, keep angle
                    print(f"  PLAYER: Free movement NO CHANGE. Staying at ({p_new_lat:.5f},{p_new_lng:.5f})")
        else:  # No movement keys pressed
            p_new_lat, p_new_lng = p_logic_lat, p_logic_lng  # Stay at snapped (if snapped) or current pos
            p_new_angle = p_cur_angle  # Keep current angle
            print(f"PLAYER: No movement keys pressed. Staying at ({p_new_lat:.5f},{p_new_lng:.5f})")
    else:  # Fallback to original free movement if no road network
        print("PLAYER: No road network - using original free movement.")
        # ... (original free movement logic) ...
        pass

    current_marker_state = {'lat': p_new_lat, 'lng': p_new_lng, 'angle': p_new_angle}
    map_center = [p_new_lat, p_new_lng]
    print(f"PLAYER: Final for tick: pos=({p_new_lat:.5f},{p_new_lng:.5f}), Angle: {p_new_angle:.1f}")

    # --- Player Shooting ---
    current_game_state['player_shoot_cooldown'] = max(0, current_game_state.get('player_shoot_cooldown', 0) - 1)
    if key_status.get('Space') and current_game_state['player_shoot_cooldown'] == 0:
        print(">>> Player Shoots!")
        bullet_id = current_game_state['next_bullet_id']
        current_game_state['next_bullet_id'] += 1
        current_player_bullets.append(
            {'id': f"pb_{bullet_id}", 'lat': p_new_lat, 'lng': p_new_lng, 'angle': p_new_angle})
        current_game_state['player_shoot_cooldown'] = current_game_state['player_shoot_interval']

    # --- Bullet Movement (Player) ---
    active_player_bullets_after_move = []
    for bullet in current_player_bullets:  # Use the copied list
        b_lat, b_lng = move_point_on_bearing(bullet['lat'], bullet['lng'], bullet['angle'], PLAYER_BULLET_SPEED)
        if abs(b_lat - INITIAL_LAT) < 0.1 and abs(b_lng - INITIAL_LNG) < 0.1:  # Bullet range limit
            active_player_bullets_after_move.append(
                {'id': bullet['id'], 'lat': b_lat, 'lng': b_lng, 'angle': bullet['angle']})
    current_player_bullets = active_player_bullets_after_move  # Update the copied list

    # --- Enemy Logic ---
    processed_enemy_cars = []  # New list for this tick's enemy updates
    print(f"ENEMIES: Processing {len(current_enemy_cars)} enemies from store/reset.")
    for enemy_data in current_enemy_cars:  # Iterate over the copied list
        # enemy_data = enemy.copy() # Work on a copy of the enemy dict
        if not enemy_data['active']:
            processed_enemy_cars.append(enemy_data)
            continue

        e_cur_lat, e_cur_lng, e_cur_angle = enemy_data['lat'], enemy_data['lng'], enemy_data['angle']
        e_new_lat, e_new_lng, e_new_angle = e_cur_lat, e_cur_lng, e_cur_angle

        if road_network:
            # Enemy aims for player's current position (p_new_lat, p_new_lng)
            path_coords = road_network.get_path_to_target(e_cur_lat, e_cur_lng, p_new_lat, p_new_lng)
            if len(path_coords) > 1:  # Path found with at least one step
                next_wp_lat, next_wp_lng = path_coords[1]  # Target the next waypoint

                e_moved_lat, e_moved_lng, e_moved_angle, e_new_segment = road_network.move_along_road(
                    e_cur_lat, e_cur_lng,  # Start from enemy's current
                    next_wp_lat, next_wp_lng,  # Aim towards this specific waypoint
                    ENEMY_MOVEMENT_STEP,
                    e_cur_angle,
                    enemy_data.get('current_segment')
                )
                e_new_lat, e_new_lng, e_new_angle = e_moved_lat, e_moved_lng, e_moved_angle
                enemy_data['current_segment'] = e_new_segment  # Update segment
            else:  # No path, or already very close. Face player.
                e_new_angle = calculate_bearing({'lat': e_cur_lat, 'lng': e_cur_lng},
                                                {'lat': p_new_lat, 'lng': p_new_lng})
        else:  # Fallback enemy movement (direct pursuit)
            dist_to_player = math.hypot(p_new_lat - e_cur_lat, p_new_lng - e_cur_lng)
            if dist_to_player > MIN_ENEMY_DISTANCE_TO_PLAYER:
                bearing_to_player = calculate_bearing({'lat': e_cur_lat, 'lng': e_cur_lng},
                                                      {'lat': p_new_lat, 'lng': p_new_lng})
                e_new_lat, e_new_lng = move_point_on_bearing(e_cur_lat, e_cur_lng, bearing_to_player,
                                                             ENEMY_MOVEMENT_STEP)
                e_new_angle = bearing_to_player

        enemy_data['lat'], enemy_data['lng'], enemy_data['angle'] = e_new_lat, e_new_lng, e_new_angle

        # Enemy Shooting
        enemy_data['shoot_cooldown'] = max(0, enemy_data.get('shoot_cooldown', 0) - 1)
        if enemy_data['shoot_cooldown'] == 0:
            dist_to_player_shoot = math.hypot(p_new_lat - e_new_lat, p_new_lng - e_new_lng)
            if dist_to_player_shoot < 0.01:  # Max shooting range
                # print(f"  ENEMY {enemy_data['id']} shoots!")
                angle_for_shot = calculate_bearing({'lat': e_new_lat, 'lng': e_new_lng},
                                                   {'lat': p_new_lat, 'lng': p_new_lng})
                bullet_id = current_game_state['next_bullet_id'];
                current_game_state['next_bullet_id'] += 1
                current_enemy_bullets.append(
                    {'id': f"eb_{bullet_id}", 'lat': e_new_lat, 'lng': e_new_lng, 'angle': angle_for_shot})
                enemy_data['shoot_cooldown'] = enemy_data.get('enemy_shoot_interval', 100)
        processed_enemy_cars.append(enemy_data)
    current_enemy_cars = processed_enemy_cars  # Assign the processed list back

    # --- Bullet Movement (Enemy) ---
    active_enemy_bullets_after_move = []
    for bullet in current_enemy_bullets:  # Use the copied list
        b_lat, b_lng = move_point_on_bearing(bullet['lat'], bullet['lng'], bullet['angle'], ENEMY_BULLET_SPEED)
        if abs(b_lat - INITIAL_LAT) < 0.1 and abs(b_lng - INITIAL_LNG) < 0.1:
            active_enemy_bullets_after_move.append(
                {'id': bullet['id'], 'lat': b_lat, 'lng': b_lng, 'angle': bullet['angle']})
    current_enemy_bullets = active_enemy_bullets_after_move

    # --- Collision Detection ---
    # 1. Player bullets vs Enemies
    coll_enemy_cars = []
    for enemy_obj in current_enemy_cars:  # Iterate over current_enemy_cars
        if not enemy_obj['active']:
            coll_enemy_cars.append(enemy_obj);
            continue
        hit_by_player = False
        surviving_player_bullets_coll = []
        for p_bullet in current_player_bullets:  # Use current_player_bullets
            dist_to_enemy = math.hypot(p_bullet['lat'] - enemy_obj['lat'], p_bullet['lng'] - enemy_obj['lng'])
            if dist_to_enemy < COLLISION_THRESHOLD_ENEMY:
                hit_by_player = True;
                current_game_state['score'] += 10
                print(f"  COLLISION: Player bullet hit Enemy {enemy_obj['id']}")
            else:
                surviving_player_bullets_coll.append(p_bullet)
        current_player_bullets = surviving_player_bullets_coll  # Update current_player_bullets
        if hit_by_player: enemy_obj['active'] = False
        coll_enemy_cars.append(enemy_obj)
    current_enemy_cars = coll_enemy_cars  # Update current_enemy_cars

    # 2. Enemy bullets vs Player
    if not current_game_state.get('game_over', False):
        surviving_enemy_bullets_coll = []
        for e_bullet in current_enemy_bullets:  # Use current_enemy_bullets
            dist_to_player_collision = math.hypot(e_bullet['lat'] - p_new_lat, e_bullet['lng'] - p_new_lng)
            if dist_to_player_collision < COLLISION_THRESHOLD_PLAYER:
                current_game_state['game_over'] = True;
                print(">>> Player hit by enemy bullet! Game Over.");
                break
            else:
                surviving_enemy_bullets_coll.append(e_bullet)
        current_enemy_bullets = surviving_enemy_bullets_coll  # Update current_enemy_bullets

    # --- Status Update ---
    status_text = f"Score: {current_game_state['score']}"
    if road_network and current_game_state.get('player_segment') is not None:
        status_text += " | ON ROAD"
    else:
        status_text += " | OFF ROAD"
    active_enemies_count = len([e for e in current_enemy_cars if e['active']])
    status_text += f" | Enemies: {active_enemies_count}"
    if current_game_state.get('game_over'): status_text = f"GAME OVER! {status_text}"
    # print(f"STATUS: {status_text}")

    # --- Prepare Markers for Rendering (ensure unique IDs for Dash updates) ---
    # Generate unique IDs for markers if they don't have persistent ones that Dash can track for updates.
    # Using uuid.uuid4() for each marker forces Dash to re-render them if their properties change.
    active_enemies_for_render = [e for e in current_enemy_cars if e['active']]
    enemy_markers = [dl.RotatedMarker(id=str(uuid.uuid4()), position=[e['lat'], e['lng']],
                                      icon={"iconUrl": ENEMY_ICON_URL, "iconSize": ENEMY_ICON_SIZE,
                                            "iconAnchor": ENEMY_ICON_ANCHOR}, rotationAngle=e['angle']) for e in
                     active_enemies_for_render]
    player_bullet_markers = [dl.Marker(id=str(uuid.uuid4()), position=[b['lat'], b['lng']], icon=PLAYER_BULLET_ICON) for
                             b in current_player_bullets]
    enemy_bullet_markers = [dl.Marker(id=str(uuid.uuid4()), position=[b['lat'], b['lng']], icon=ENEMY_BULLET_ICON) for b
                            in current_enemy_bullets]

    print(
        f"RENDERING: Player marker pos=({p_new_lat:.5f},{p_new_lng:.5f}). Enemies: {len(enemy_markers)}, P.Bullets: {len(player_bullet_markers)}, E.Bullets: {len(enemy_bullet_markers)}")

    return (
        [p_new_lat, p_new_lng], p_new_angle,  # Player marker
        map_center,  # Map center
        current_marker_state,  # dcc.Store for player
        status_text,
        current_player_bullets,  # dcc.Store
        current_enemy_cars,  # dcc.Store
        current_enemy_bullets,  # dcc.Store
        current_game_state,  # dcc.Store
        enemy_markers,  # LayerGroup children
        player_bullet_markers,  # LayerGroup children
        enemy_bullet_markers  # LayerGroup children
    )


# KEEP ALL YOUR EXISTING CODE BELOW THIS (if __name__ == '__main__': etc.)

if __name__ == '__main__':
    app.run_server(debug=True, port=4333)
