import pandas as pd


def read_all_scenes_file() -> list[str]:
    with open("resources/all_scenes.txt") as file:
        return file.readlines()


def write_actors(actors: list[dict]):
    _write_actors("output/data/actors.csv", actors)


def write_transition_actors(transition_actors: list[dict]):
    _write_actors("output/data/transition_actors.csv", transition_actors)


def write_spawns(spawns: list[dict]):
    _write_actors("output/data/spawns.csv", spawns)


def _write_actors(file_path: str, actors: list[dict]):
    pd.DataFrame(actors).to_csv(file_path, index=False, sep=";")
