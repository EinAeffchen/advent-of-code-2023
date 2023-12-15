from dataclasses import dataclass
from collections import Counter
from utils import get_data
from pathlib import Path

day = int(Path(__file__).stem)

TEST_DATA = [
    "...#......",
    ".......#..",
    "#.........",
    "..........",
    "......#...",
    ".#........",
    ".........#",
    "..........",
    ".......#..",
    "#...#.....",
]


def expand_universe(input_data: list[str]) -> list[str]:
    expansion_points = [[], []]
    for i, row in enumerate(input_data):
        if len(row) * "." == row:
            expansion_points[0].append(i)
    for c in range(len(input_data[0])):
        if all(row[c] if row[c] == "." else False for row in input_data):
            expansion_points[1].append(c)
    return expansion_points


def get_mod_count(c: int, mod_points: list[int]) -> int:
    return len([i for i in mod_points if i < c])


def get_galaxies(
    input_data: list[str], expansion_points: list[list[int]], modificator: int
) -> dict:
    galaxy_counter = 1
    galaxies = dict()
    for y, row in enumerate(input_data):
        for x, symbol in enumerate(row):
            if symbol == "#":
                y_modifications = get_mod_count(y, expansion_points[0])
                x_modifications = get_mod_count(x, expansion_points[1])
                galaxies[galaxy_counter] = (
                    y + (y_modifications * abs(modificator - 1)),
                    x + (x_modifications * abs(modificator - 1)),
                )
                galaxy_counter += 1
    return galaxies


def calculate_distances(galaxies: dict):
    distances = dict()
    for galaxy, position in galaxies.items():
        for galaxy2, position2 in galaxies.items():
            if galaxy == galaxy2:
                continue
            pair = {galaxy, galaxy2}
            # if distances.get(frozenset(pair)):
            #     continue
            distances[frozenset(pair)] = abs(position2[0] - position[0]) + abs(
                position2[1] - position[1]
            )
    return distances


def task01(input_data: list[str], test=True):
    modificator = 2
    expansion_points = expand_universe(input_data)
    galaxies = get_galaxies(input_data, expansion_points, modificator)
    distances = calculate_distances(galaxies)
    if test:
        assert sum(distances.values()) == 374
    return sum(distances.values())


def task02(input_data: list[str], test=True):
    if test:
        modificator = 10
    else:
        modificator = 1000000
    expansion_points = expand_universe(input_data)
    galaxies = get_galaxies(input_data, expansion_points, modificator)
    distances = calculate_distances(galaxies)
    if test:
        assert sum(distances.values()) == 1030
    return sum(distances.values())


task01(TEST_DATA)
print(task01(get_data(day), test=False))
print(task02(TEST_DATA))
print(task02(get_data(day), test=False))
