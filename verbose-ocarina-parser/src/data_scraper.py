import re


def _get_desc_pos_rot(line: str) -> tuple[str, tuple[int, ...], tuple[int, ...]]:
    pos_split = re.search(r"\(-?\d+, -?\d+, -?\d+\) \([0-9A-F]{4}, [0-9A-F]{4}, [0-9A-F]{4}\)", line).start()
    pos_rot = [x.strip(",()") for x in line[pos_split:].split()]

    position = tuple(int(x) for x in pos_rot[:3])
    rotation = tuple(int(x, 16) for x in pos_rot[3:])
    description = line[:pos_split].strip()
    return description, position, rotation


def get_transition_actors_from_scene_setup(scene_setup: list[str], scene_idx: int) -> list[dict]:
    is_cutscene = scene_setup[0].startswith("Cutscene ")
    setup_idx = int(scene_setup[0].split()[1][:-1])
    start_index = 0
    stop_index = 0
    for i, line in enumerate(scene_setup):
        if line.startswith("0E: There are ") and "transition actor(s)" in line:
            start_index = i + 1
            continue
        if start_index and ("->" not in line):
            stop_index = i
            break
    line_list = scene_setup[start_index:stop_index]

    res = []
    for line_idx, line in enumerate(line_list):
        transition, params, rest = line.split(',', 2)

        transition_split = transition.split()
        exiting_room = int(transition_split[0])
        entering_room = int(transition_split[3])

        description, position, rotation = _get_desc_pos_rot(rest)

        res.append({
            "scene": scene_idx,
            "is_cutscene": is_cutscene,
            "setup": setup_idx,
            "idx": line_idx,
            "exiting_room": exiting_room,
            "entering_room": entering_room,
            "transition": transition.strip(),
            "params": params.strip(),
            "description": description,
            "pos_x": position[0],
            "pos_y": position[1],
            "pos_z": position[2],
            "rot_x": rotation[0],
            "rot_y": rotation[1],
            "rot_z": rotation[2],
        })
    return res


def get_spawns_from_scene_setup(scene_setup: list[str], scene_idx: int) -> list[dict]:
    is_cutscene = scene_setup[0].startswith("Cutscene ")
    setup_idx = int(scene_setup[0].split()[1][:-1])
    positions_start = 0
    positions_stop = 0
    for i, line in enumerate(scene_setup):
        if line.startswith("00: There are ") and "position(s)" in line:
            positions_start = i + 1
            continue
        if positions_start and ("Link" not in line):
            positions_stop = i
            break
    position_lines = scene_setup[positions_start:positions_stop]

    spawn_rooms_start = 0
    spawn_rooms_stop = 0
    for i, line in enumerate(scene_setup):
        if line.startswith("06: Entrance Index Definitions starts at"):
            spawn_rooms_start = i + 1
            continue
        if spawn_rooms_start and ("Spawn" not in line or "Room" not in line):
            spawn_rooms_stop = i
            break
    spawn_rooms_lines = scene_setup[spawn_rooms_start:spawn_rooms_stop]
    spawn_rooms_dict = {int(line.split(',')[0].split()[1]): int(line.split(',')[1].split()[1])
                        for line in spawn_rooms_lines}

    res = []
    for line_idx, line in enumerate(position_lines):
        params, rest = line.split(' ', 1)

        description, position, rotation = _get_desc_pos_rot(rest)

        res.append({
            "scene": scene_idx,
            "is_cutscene": is_cutscene,
            "setup": setup_idx,
            "idx": line_idx,
            "room": spawn_rooms_dict[line_idx],
            "params": params.strip(),
            "description": description,
            "pos_x": position[0],
            "pos_y": position[1],
            "pos_z": position[2],
            "rot_x": rotation[0],
            "rot_y": rotation[1],
            "rot_z": rotation[2],
        })
    return res


def get_actors_from_room_setup(room_setup: list[str], scene_idx: int, room_idx: int) -> list[dict]:
    is_cutscene = room_setup[0].startswith("Cutscene ")
    setup_idx = int(room_setup[0].split()[1][:-1])
    actor_list = []
    for i, line in enumerate(room_setup):
        if line.startswith("01: There are ") and "actor(s)" in line:
            actor_list = room_setup[i + 1:]

    res = []
    for line_idx, line in enumerate(actor_list):
        params, rest = line.split(' ', 1)

        description, position, rotation = _get_desc_pos_rot(rest)

        res.append({
            "scene": scene_idx,
            "is_cutscene": is_cutscene,
            "setup": setup_idx,
            "room": room_idx,
            "idx": line_idx,
            "params": params.strip(),
            "description": description,
            "pos_x": position[0],
            "pos_y": position[1],
            "pos_z": position[2],
            "rot_x": rotation[0],
            "rot_y": rotation[1],
            "rot_z": rotation[2],
        })
    return res


def get_all_actors(raw_data: list[str]) -> tuple[list, list, list]:
    all_actors = []
    all_transition_actors = []
    all_spawns = []

    # Cleanup list
    raw_data = [li.rstrip() for li in raw_data if li.rstrip()]

    # Split list into scenes
    scene_list_raw = []
    current_scene_list = []
    for line in raw_data:
        if line.startswith("-- SCENE "):
            current_scene_list = []
            scene_list_raw.append(current_scene_list)
        current_scene_list.append(line)

    # Split scenes into scene setup headers and rooms
    for scene_idx, scene in enumerate(scene_list_raw):

        scene_setups_raw = []
        room_setups_raw = []
        for line_idx, line in enumerate(scene):
            if line.startswith("Room "):
                scene_setups_raw = scene[:line_idx]
                room_setups_raw = scene[line_idx:]
                break

        # Split up scene setups
        scene_setup_list = []
        current_scene_setup = []
        for line in scene_setups_raw:
            if line.startswith(("Setup ", "Cutscene ")):
                current_scene_setup = []
                scene_setup_list.append(current_scene_setup)
            current_scene_setup.append(line)

        # Get transition actors and spawns from scene setups
        for scene_setup in scene_setup_list:
            scene_transition_actors = get_transition_actors_from_scene_setup(scene_setup, scene_idx)
            all_transition_actors.extend(scene_transition_actors)
            scene_spawns = get_spawns_from_scene_setup(scene_setup, scene_idx)
            all_spawns.extend(scene_spawns)

        # Split up Rooms
        room_list_raw = []
        current_room = []
        for line in room_setups_raw:
            if line.startswith("Room ") and len(line) <= 7:
                current_room = []
                room_list_raw.append(current_room)
            current_room.append(line)

        for room_idx, room in enumerate(room_list_raw):

            # Split up room setups
            room_setup_list = []
            current_room_setup = []
            for line in room:
                if line.startswith(("Setup ", "Cutscene ")):
                    current_room_setup = []
                    room_setup_list.append(current_room_setup)
                current_room_setup.append(line)

            # Get room actors from room setups
            for room_setup in room_setup_list:
                actors = get_actors_from_room_setup(room_setup, scene_idx, room_idx)
                all_actors.extend(actors)

    # print(*all_transition_actors, sep="\n")
    # print(len(all_transition_actors))

    # print(*all_spawns, sep="\n")
    # print(len(all_spawns))

    # print(*all_actors, sep="\n")
    # print(len(all_actors))

    return all_actors, all_transition_actors, all_spawns
