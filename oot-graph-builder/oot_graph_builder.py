from __future__ import annotations

import collections
import math
from typing import Any

import networkx as nx
import pandas as pd

ACTOR_LABEL = 'actor'
TRANSITION_ACTOR_LABEL = 'transition_actor'
SPAWN_LABEL = 'spawn'
NODE_TYPE_LABEL = 'node_type'
SAVEW_EDGE_LABEL = 'save_warp'
DEATHW_EDGE_LABEL = 'death_warp'
SONGW_EDGE_LABEL = 'song_warp'
BLUEW_EDGE_LABEL = 'blue_warp'
EDGE_TYPE_LABEL = 'edge_type'

CHILD_OW_SW = (52, 0)
ADULT_OW_SW = (67, 7)

# TODO: Handle requirements in SW
_SW_SCENE_TO_TARGET_SCENES_AUX = {
    # Dungeons
    0: [0],
    1: [1],
    2: [2],
    3: [3],
    4: [4],
    5: [5],
    6: [6],
    7: [7],
    8: [8],
    9: [9],
    10: [10],
    11: [11],
    12: [12],
    13: [13],

    # Boss Rooms
    17: [0],
    18: [1],
    19: [2],
    20: [3],
    21: [4],
    22: [5],
    23: [6],
    24: [7],
    25: [10],

    # Post Ganondorf
    14: [10],
    15: [10],
    26: [10],
    79: [10],

    # Link's House
    52: [52],
}

SW_SCENE_TO_TARGET_SCENES = {
    i: [CHILD_OW_SW[0], ADULT_OW_SW[0]]
    for i in range(101)
}

SW_SCENE_TO_TARGET_SCENES.update(_SW_SCENE_TO_TARGET_SCENES_AUX)

SCENE_TRANSITION_LIST = (
    # Kok to Link's House
    ('s-459', 's-162'),
    # Link's House to Kok
    ('s-162', 's-459'),

    # Kok to Kok Shop
    ('s-460', 's-151'),
    # Kok Shop to Kok
    ('s-151', 's-460'),

    # Kok to Twins'
    ('s-464', 's-144'),
    # Twins' to Kok
    ('s-144', 's-464'),

    # Kak to Saria's
    ('s-466', 's-146'),
    # Saria's to Kak
    ('s-146', 's-466'),

    # Kok to Mido's
    ('s-465', 's-145'),
    # Mido's to Kok
    ('s-145', 's-465'),

    # Kok to Lost Woods (upper)
    ('s-462', 's-587'),
    # Lost Woods (upper) to Kok
    ('s-587', 's-462'),

    # Kok to Know-It-All's
    ('s-461', 's-143'),
    # Know-It-All's to Kok
    ('s-143', 's-461'),

    # Kok to Lost Woods (Bridge)
    ('s-458', 's-596'),
    # Lost Woods (Bridge) to Kok
    ('s-596', 's-458'),

    # Kok to Deku Tree
    ('s-457', 's-0'),
    # Deku Tree to Kok
    ('s-0', 's-457'),

    # Deku Tree to Gohma's Lair
    ('s-1', 's-61'),
    # Gohma's Lair to Deku Tree
    ('s-61', 's-1'),

    # Lost Woods to Hyrule Field
    ('s-595', 's-281'),
    # Hyrule Field to Lost Woods
    ('s-281', 's-595'),

    # Hyrule Field to Gerudo Valley
    ('s-283', 's-574'),
    # Gerudo Valley to Hyrule Field
    ('s-574', 's-283'),

    # Gerudo Valley to Gerudo's Fortress
    ('s-577', 's-627'),
    # Gerudo's Fortress to Gerudo Valley
    ('s-627', 's-577'),

    # Gerudo's Fortress to Haunted Wasteland
    ('s-642', 's-701'),
    # Haunted Wasteland to Gerudo's Fortress
    ('s-701', 's-642'),

    # Haunted Wasteland to Desert Colossus
    ('s-702', 's-608'),
    # Desert Colossus to Haunted Wasteland
    ('s-608', 's-702'),

    # Ice cavern to Zora's Fountain s2
    ('s-21', 's-560'),

    # Zora's Fountain s2 to Ice Cavern
    ('s-560', 's-21'),

    # Windmill to Kak s0
    ('s-260', 's-349'),

    # Kak s0 to Windmill
    ('s-349', 's-260'),

    # ## Transitions for single component with warps ##

    # GTG to GF s2
    ('s-27', 's-659'),

    # GF s2 to GTG
    ('s-659', 's-27'),

    # Ganon's Castle to Ganon's Tower
    ('s-42', 's-24'),

    # Ganon's Tower to Ganon's Castle
    ('s-24', 's-42'),
)

SAMPLE_TRANSITION_LIST = (
    # Kok to Link's House
    ('s-459', 's-162'),
    # Link's House to Kok
    ('s-162', 's-459'),

    # Kok to Kok Shop
    ('s-460', 's-151'),
    # Kok Shop to Kok
    ('s-151', 's-460'),

    # Kok to Twins'
    ('s-464', 's-144'),
    # Twins' to Kok
    ('s-144', 's-464'),

    # Kak to Saria's
    ('s-466', 's-146'),
    # Saria's to Kak
    ('s-146', 's-466'),

    # Kok to Mido's
    ('s-465', 's-145'),
    # Mido's to Kok
    ('s-145', 's-465'),

    # Kok to Lost Woods (upper)
    ('s-462', 's-587'),
    # Lost Woods (upper) to Kok
    ('s-587', 's-462'),

    # Kok to Know-It-All's
    ('s-461', 's-143'),
    # Know-It-All's to Kok
    ('s-143', 's-461'),

    # Kok to Lost Woods (Bridge)
    ('s-458', 's-596'),
    # Lost Woods (Bridge) to Kok
    ('s-596', 's-458'),

    # Kok to Deku Tree
    ('s-457', 's-0'),
    # Deku Tree to Kok
    ('s-0', 's-457'),

    # Deku Tree to Gohma's Lair
    ('s-1', 's-61'),
    # Gohma's Lair to Deku Tree
    ('s-61', 's-1'),

    # Gohma's Blue Warp to Kok
    ('2633', 's-467'),
)

BLUE_WARP_EDGE_LIST = (
    # Queen Gohma to Kok
    ('2633', 's-467'),

    # King Dodongo to DMT
    ('2643', 's-713'),

    # Barinade to ZF
    ('2650', 's-545'),

    # Phantom Ganon to
    ('2657', 's-510'),

    # Volvagia to DMC
    ('2659', 's-735'),

    # Morpha to LH
    ('2660', 's-531'),

    # Twinrova to DC
    ('2731', 's-624'),

    # Bongo Bongo to Graveyard
    ('2741', 's-434'),
)

# TODO: Add requirements
SONG_WARP_DESTINATION_LIST = [
    # Minuet
    's-510',
    # Buleru
    's-735',
    # Serenade
    's-531',
    # Requiem
    's-624',
    # Nocturne
    's-434',
    # Prelude
    's-230'
]

NO_WARP_SONGS_SCENES = {
    11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 66, 68, 69, 70, 71, 73, 74, 75, 78, 79,
}


def build_room_actors_components(actors_df: pd.DataFrame,
                                 scene: int,
                                 setup: int,
                                 is_cutscene: bool,
                                 node_type: str) -> nx.MultiDiGraph:
    """
    Build a graph with one component for every room in `actors_df` that has at least one actor.

    Each individual component will form a complete graph.
    Additional data in `actors_df` will be added to the nodes as attributes.

    Args:
        actors_df: `pandas.DataFrame` containing the actor data
        scene: scene to build
        setup: setup to pick from scene setups
        is_cutscene: whether to pick cutscene setups
        node_type: label to set the `NODE_TYPE_LABEL` attribute to.
            Must be in ('ACTOR_LABEL', SPAWN_LABEL) (see module constants).
    Returns:
        A new networkx.MultiDiGraph object resembling the given actors.
    """

    if node_type not in (ACTOR_LABEL, SPAWN_LABEL):
        raise ValueError(f"{NODE_TYPE_LABEL} is {node_type},"
                         f"expected one of: {(ACTOR_LABEL, SPAWN_LABEL)} (see vars of ogb)")

    scene_actors_df = actors_df.loc[(actors_df['scene'] == scene) &
                                    (actors_df['setup'] == setup) &
                                    (actors_df['is_cutscene'] == is_cutscene)]
    if len(scene_actors_df.index) == 0:
        return nx.MultiDiGraph()

    rooms = {x['room'] for _, x in scene_actors_df.iterrows()}
    room_actors_dfs = [scene_actors_df.loc[(scene_actors_df['room']) == r] for r in rooms]

    g_rooms = [nx.complete_graph(x.index, nx.MultiDiGraph) for x in room_actors_dfs]
    room_actors_dicts = [df.to_dict('index') for df in room_actors_dfs]

    for g_room, room_actor_dict in zip(g_rooms, room_actors_dicts):
        nx.set_node_attributes(g_room, room_actor_dict)
        nx.set_node_attributes(g_room, node_type, NODE_TYPE_LABEL)

    return nx.union_all(g_rooms)


def build_transition_actors(transition_actors_df: pd.DataFrame,
                            scene: int,
                            setup: int,
                            is_cutscene: bool) -> nx.MultiDiGraph:
    g_transit = nx.MultiDiGraph()
    scene_transit_df: pd.DataFrame = transition_actors_df.loc[(transition_actors_df['scene'] == scene) &
                                                              (transition_actors_df['setup'] == setup) &
                                                              (transition_actors_df['is_cutscene'] == is_cutscene)]
    if len(scene_transit_df.index) == 0:
        return g_transit

    scene_transit_dict = scene_transit_df.to_dict('index')

    g_transit.add_nodes_from([(k, v) for k, v in scene_transit_dict.items()])
    nodes = g_transit.nodes(data=True)

    # Connect transition nodes with each other if they are adjacent to the same room
    for it, it_data in nodes:
        for other, other_data in nodes:
            if it != other:
                it_targets = {it_data['exiting_room'], it_data['entering_room']}
                other_targets = {other_data['exiting_room'], other_data['entering_room']}
                if not it_targets.isdisjoint(other_targets):
                    g_transit.add_edge(it, other)

    nx.set_node_attributes(g_transit, TRANSITION_ACTOR_LABEL, NODE_TYPE_LABEL)

    return g_transit


def build_scene_graph(spawns_df: pd.DataFrame,
                      actors_df: pd.DataFrame,
                      transit_actors_df: pd.DataFrame,
                      scene: int,
                      setup: int,
                      is_cutscene: bool = False,
                      rename: tuple[str, str, str] = ('s-', '', 't-')) -> nx.MultiDiGraph:
    """
    Builds the entire scene as a `networkx.MultiDiGraph` . Includes room actors, spawns and transition actors.

    Spawns and room actors will be nodes of one complete graph per room, transition actors will be connected with all
    actors in adjacent rooms, including other transition actors.
    Other data in DataField objects will be added as node attributes.
    `NODE_TYPE_LABEL` labeled attribute will be given to all edges (see module constants);
    `ACTOR_LABEL` to room actors, `SPAWN_LABEL` to spawns and `TRANSITION_ACTOR_LABEL` to transition actors.

    Args:
        spawns_df: pandas.DataField with spawn data
        actors_df: pandas.DataField with room actor data
        transit_actors_df: pandas.DataField with transition actor data
        scene: scene to build
        setup: setup to pick from scene setups
        is_cutscene: whether to pick cutscene setups
        rename: renaming tuple (spawns_rename, actors_rename, transit_rename) (see networkx.union() )
    Returns:
        A networkx.MultiDiGraph() with all room actors, transition actors and spawns as nodes.
    """
    g_room_actors = build_room_actors_components(actors_df, scene, setup, is_cutscene, ACTOR_LABEL)
    g_spawns = build_room_actors_components(spawns_df, scene, setup, is_cutscene, SPAWN_LABEL)
    g_transit_actors = build_transition_actors(transit_actors_df, scene, setup, is_cutscene)
    g_spawns_and_actors = union_spawns_and_actors(g_spawns, g_room_actors, rename[:2])
    g_scene = union_actors_and_transition_actors(g_spawns_and_actors, g_transit_actors, node_rename=('', rename[2]))

    return g_scene


def union_spawns_and_actors(g_spawns: nx.MultiDiGraph,
                            g_actors: nx.MultiDiGraph,
                            rename: tuple[str, str] = ('s-', ''),
                            set_node_type_label: bool = True) -> nx.MultiDiGraph:
    if not g_spawns and not g_actors:
        return nx.MultiDiGraph()

    if rename[0] == rename[1]:
        raise ValueError(f"{rename = }; elements must differ do distinguish them in union graph.")

    if set_node_type_label:
        nx.set_node_attributes(g_spawns, SPAWN_LABEL, NODE_TYPE_LABEL)
        nx.set_node_attributes(g_actors, ACTOR_LABEL, NODE_TYPE_LABEL)

    spawns = g_spawns.nodes(data='room')
    actors = g_actors.nodes(data='room')

    renamed_spawns = [(rename[0] + str(s), r) for s, r in spawns]
    renamed_actors = [(rename[1] + str(a), r) for a, r in actors]

    g: nx.MultiDiGraph = nx.union(g_spawns, g_actors, rename)

    for spawn, s_room in renamed_spawns:
        for actor, a_room in renamed_actors:
            if s_room == a_room:
                g.add_edge(spawn, actor)
                g.add_edge(actor, spawn)

    return g


def union_actors_and_transition_actors(g_actors: nx.MultiDiGraph,
                                       g_transition_actors: nx.MultiDiGraph,
                                       disjoint: bool = False,
                                       graph_rename: str = None,
                                       node_rename: tuple[str, str] = None,
                                       connect_transition_actors: bool = True,
                                       set_node_type_label: bool = False) -> nx.MultiDiGraph:
    """
    Union actors graph with transition actors graph and connecting actors with transitions.

    With `disjoint=True` : note the relabeling from `0` to `(len(g_actors) + len(g_transition_actors) -1)`.

    Also note that this function will assign an attribute `'node_type'` to the nodes of both input graphs in-place,
    `'actor'` or `'transition_actor'` respectively.

    Args:
        g_actors: networkx.MultiDiGraph containing the actors
        g_transition_actors: networkx.MultiDiGraph containing the transition actors
        disjoint: Whether or not to do a disjoint union (see networkx.union() and networkx.disjoint_union() )
        graph_rename: Name of the resulting new graph when using non-disjoint union (see networkx.union() )
        node_rename: Renaming tuple when using non-disjoint union (see networkx.union() )
        connect_transition_actors: Whether or not to connect actors with transition actors in the new graph
        set_node_type_label: Whether or not to set NODE_TYPE_LABEL node attribute to
            ACTOR_LABEL and TRANSITION_ACTOR_LABEL (see module constants)
    Returns:
        New graph with connected actors and transition actors
    """

    if not g_actors and not g_transition_actors:
        return nx.MultiDiGraph()

    if set_node_type_label:
        nx.set_node_attributes(g_actors, ACTOR_LABEL, NODE_TYPE_LABEL)
        nx.set_node_attributes(g_transition_actors, TRANSITION_ACTOR_LABEL, NODE_TYPE_LABEL)

    if disjoint:
        g: nx.MultiDiGraph = nx.disjoint_union(g_actors, g_transition_actors)
    else:
        g: nx.MultiDiGraph = nx.union(g_actors, g_transition_actors, rename=node_rename, name=graph_rename)

    if connect_transition_actors:
        transit_nodes = []
        actor_nodes = []
        for n, data in g.nodes(data=True):
            node_type = data[NODE_TYPE_LABEL]
            if node_type in (ACTOR_LABEL, SPAWN_LABEL):
                actor_nodes.append((n, data))
            elif node_type == TRANSITION_ACTOR_LABEL:
                transit_nodes.append((n, data))

        transit_edge_list = []
        for t, t_data in transit_nodes:
            for a, a_data in actor_nodes:
                if a_data['room'] in (t_data['entering_room'], t_data['exiting_room']):
                    transit_edge_list.append((a, t))
                    transit_edge_list.append((t, a))

        g.add_edges_from(transit_edge_list)

    return g


def get_telling_unique_node_label(node_dict: dict) -> str:
    node_type = str(node_dict[NODE_TYPE_LABEL]) if NODE_TYPE_LABEL in node_dict else ''
    scene = f"s{str(node_dict['scene'])}"
    room = f"r{str(node_dict['room'])}" if 'room' in node_dict else ''
    setup = f"setup{str(node_dict['setup'])}"
    is_cutscene = 'cutscene' if node_dict['is_cutscene'] else ''
    idx = f"idx{str(node_dict['idx'])}"

    return f"{node_type}{scene}{room}{setup}{is_cutscene}{idx}"


def get_pos_dict(nodes_container: pd.DataFrame | nx.Graph,
                 mirrored_over_x_axis=False) -> dict[Any, tuple[int, int]]:
    try:
        nodes = nodes_container.iterrows()
    except AttributeError:
        try:
            nodes = nodes_container.nodes(data=True)
        except AttributeError:
            raise TypeError("Container is neither a pandas.DataFrame nor a networkx.Graph.")

    return {k: (v['pos_x'], v['pos_z'] if not mirrored_over_x_axis else -v['pos_z'])
            for k, v in nodes}


def get_normalized_pos_dict(nodes_container: pd.DataFrame | nx.Graph,
                            mirrored_over_x_axis=False,
                            preserve_ratio=True) -> dict[Any, tuple[int, int]]:
    res = get_pos_dict(nodes_container, mirrored_over_x_axis)

    # TODO: Maybe work with tuples here?
    pos = [(x, y) for _, (x, y) in res.items()]
    max_x = max(x for x, _ in pos)
    min_x = min(x for x, _ in pos)
    span_x = max_x - min_x
    max_y = max(y for _, y in pos)
    min_y = min(y for _, y in pos)
    span_y = max_y - min_y

    scale_x = (span_x / max(span_x, span_y)) if span_x and preserve_ratio else 1
    scale_y = (span_y / max(span_x, span_y)) if span_y and preserve_ratio else 1
    return {k: ((vx - min_x) / (span_x if span_x else 1) * scale_x,
                (vy - min_y) / (span_y if span_y else 1) * scale_y)
            for k, (vx, vy) in res.items()}


def build_scenes(
        spawns_df: pd.DataFrame,
        actors_df: pd.DataFrame,
        transit_actors_df: pd.DataFrame,
        scenes: list[int],
        setups: list[int],
        cutscenes_included: list[bool],
        scene_transition_list: list[tuple] = None) -> tuple[nx.MultiDiGraph, dict]:
    g_scenes = [g_scene for sc in scenes for is_cutscene in cutscenes_included for se in setups
                if (g_scene := build_scene_graph(spawns_df, actors_df, transit_actors_df, sc, se, is_cutscene))]
    pos_dicts = [get_normalized_pos_dict(g_sc, True) for g_sc in g_scenes]

    # Define how many scene setups to put in each row and column
    rows = math.ceil(len(g_scenes) ** 0.5)

    # Compute coords for orderly lines
    for i, pos_dict in enumerate(pos_dicts):
        pos_dicts[i] = {k: ((x + ((i + rows) % rows) * 1.2), y + (((rows + i) // rows) - 1) * 1.2)
                        for k, (x, y) in pos_dict.items()}

    g_union: nx.MultiDiGraph = nx.union_all(g_scenes)

    if scene_transition_list:
        g_union.add_edges_from(scene_transition_list)

    pos_res = {}
    for d in pos_dicts:
        pos_res |= d

    return g_union, pos_res


def add_save_warps(g_scenes: nx.MultiDiGraph, sw_duration: float = None) -> nx.MultiDiGraph:
    if not g_scenes:
        return nx.MultiDiGraph()

    g: nx.MultiDiGraph = g_scenes.copy()

    # TODO: Handle partial game graphs; add requirements (age)
    nodes = g.nodes(data=True)

    d = {EDGE_TYPE_LABEL: SAVEW_EDGE_LABEL}

    targets = {item for sublist in SW_SCENE_TO_TARGET_SCENES.values() for item in sublist}

    sw_scene_to_spawn = {s: n
                         for n, data in nodes
                         if ((s := data['scene']) in targets
                             and data[NODE_TYPE_LABEL] == SPAWN_LABEL
                             and data['idx'] == (0 if s != ADULT_OW_SW[0]
                                                 else ADULT_OW_SW[1]))}

    for n, data in nodes:
        if (s := data['scene']) in SW_SCENE_TO_TARGET_SCENES:
            for target in SW_SCENE_TO_TARGET_SCENES[s]:
                if sw_duration:
                    g.add_edge(n, sw_scene_to_spawn[target], **d, weight=sw_duration)
                else:
                    g.add_edge(n, sw_scene_to_spawn[target], **d)

    return g


def add_death_warps(g_scenes: nx.MultiDiGraph, dw_duration: float = None) -> nx.MultiDiGraph:
    if not g_scenes:
        return nx.MultiDiGraph()

    g: nx.MultiDiGraph = g_scenes.copy()

    # TODO: Add requirements, Handle Boss rooms better
    nodes = g.nodes(data=True)

    d = {EDGE_TYPE_LABEL: DEATHW_EDGE_LABEL}

    spawn_dict = collections.defaultdict(list)
    node_dict = collections.defaultdict(list)

    # Add nodes to spawn and node pools by scene, cutscene and setup
    for n, data in nodes:
        key = (data['scene'], data['is_cutscene'], data['setup'])
        node_dict[key].append(n)
        if data[NODE_TYPE_LABEL] == SPAWN_LABEL:
            spawn_dict[key].append(n)

    # Connect nodes with spawns of equally keyed pool
    for k, nodes in node_dict.items():
        for node in nodes:
            for spawn in spawn_dict[k]:
                if dw_duration:
                    g.add_edge(node, spawn, **d, weight=dw_duration)
                else:
                    g.add_edge(node, spawn, **d)

    return g


def add_song_warps(g_scenes: nx.MultiDiGraph, sw_duration: float = None) -> nx.MultiDiGraph:
    if not g_scenes:
        return nx.MultiDiGraph()

    g: nx.MultiDiGraph = g_scenes.copy()

    # TODO: Handle partial graphs; add requirements
    nodes = g.nodes(data=True)

    d = {EDGE_TYPE_LABEL: SONGW_EDGE_LABEL}

    for n, data in nodes:
        if data['scene'] not in NO_WARP_SONGS_SCENES:
            for dest in SONG_WARP_DESTINATION_LIST:
                if sw_duration is not None:
                    g.add_edge(n, dest, **d, weight=sw_duration)
                else:
                    g.add_edge(n, dest, **d)

    return g
