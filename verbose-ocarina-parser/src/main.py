import data_scraper
import file_io


def main():
    raw_data = file_io.read_all_scenes_file()

    (actors, transition_actors, spawns) = data_scraper.get_all_actors(raw_data)

    file_io.write_actors(actors)
    file_io.write_transition_actors(transition_actors)
    file_io.write_spawns(spawns)


if __name__ == '__main__':
    main()
