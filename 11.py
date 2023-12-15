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

EXPANDED_TEST = [
    "....#........",
    ".........#...",
    "#............",
    ".............",
    ".............",
    "........#....",
    ".#...........",
    "............#",
    ".............",
    ".............",
    ".........#...",
    "#....#.......",
]


def expand_universe(input_data: list[str]) -> list[str]:
    expanded_universe = list()
    for i, row in enumerate(input_data):
        if len(row) * "." == row:
            expanded_universe.append(row)
        expanded_universe.append(row)
    offset = 0
    for c in range(len(input_data[0])):
        if all(row[c] if row[c] == "." else False for row in input_data):
            for i, row in enumerate(expanded_universe):
                expanded_universe[i] = (
                    row[: c + offset] + "." + row[c + offset :]
                )
            offset += 1
    return expanded_universe


def get_galaxies(input_data: list[str]) -> dict:
    galaxy_counter = 1
    galaxies = dict()
    for y, row in enumerate(input_data):
        for x, symbol in enumerate(row):
            if symbol == "#":
                galaxies[galaxy_counter] = (y, x)
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
    expanded_universe = expand_universe(input_data)
    if test:
        assert EXPANDED_TEST == expanded_universe
    galaxies = get_galaxies(expanded_universe)
    print(galaxies)
    distances = calculate_distances(galaxies)
    if test:
        assert sum(distances.values()) == 374
    return sum(distances.values())


def task02(input_data: list[str], test=True):
    pass


task01(TEST_DATA)
print(task01(get_data(day), test=False))
task02(TEST_DATA)
print(task02(get_data(day), test=False))
