from pathlib import Path
from functools import reduce


def read_lines(input_file: Path):
    with open(input_file, "r") as f_in:
        return f_in.readlines()


def split_into_dict(game):
    draw_dict = dict()
    draws = game.split(",")
    for draw in draws:
        count, color = draw.split()
        draw_dict[color] = int(count)
    return draw_dict


def parse_input(data: list[str]) -> dict:
    game_data = dict()
    for row in data:
        game, pulls = row.split(":")
        game_number = int(game[5:])
        pulls = pulls.split(";")
        game_data[game_number] = [split_into_dict(pull) for pull in pulls]
    return game_data


TEST_DATA = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]

data = read_lines(Path(__file__).parent / "input.txt")


def sum_ids_by_filter(data: dict, game_filter: dict):
    result = 0
    for game_id, game_data in data.items():
        for color, limit in game_filter.items():
            if any(
                [True for round in game_data if round.get(color, 0) > limit]
            ):
                game_id = 0
        result += game_id
    return result


def get_power_of_minimum_cubes(game_data: dict):
    result = 0
    for drawings in game_data.values():
        minimum_set = dict()
        for drawing in drawings:
            for color, count in drawing.items():
                if minimum_set.get(color, count) <= count:
                    minimum_set[color] = count
        result += reduce((lambda x, y: x * y), minimum_set.values())
    return result


def task01(input_data: list[str], test=True):
    game_data = parse_input(input_data)
    if test:
        assert len(game_data[1]) == 3
    game_filter = {"red": 12, "green": 13, "blue": 14}
    result = sum_ids_by_filter(game_data, game_filter)
    if test:
        assert result == 8
    return result


def task02(input_data: list[str], test=True):
    game_data = parse_input(input_data)
    result = get_power_of_minimum_cubes(game_data)
    if test:
        assert result == 2286
    return result


task01(TEST_DATA)
print(task01(data, test=False))
task02(TEST_DATA)
print(task02(data, test=False))
