from dataclasses import dataclass
from collections import Counter
from utils import get_data
from pathlib import Path
from copy import deepcopy
from itertools import chain

day = int(Path(__file__).stem)

TEST_DATA = [
    "..F7.",
    ".FJ|.",
    "SJ.L7",
    "|F--J",
    "LJ...",
]


# keep track of split routes for visited spots


@dataclass
class Maze:
    raw_maze: list[str]
    visited = set()

    def __post_init__(self):
        self.V_PIPE = "|"
        self.H_PIPE = "-"
        self.START = "S"
        self.number_maze = [[0 for _ in row] for row in self.raw_maze]

    def get_start_point(self):
        for y, row in enumerate(self.raw_maze):
            x = row.find(self.START)
            if x != -1:
                self.number_maze[y][x] = 0
                return (y, x)

    def position_iterator(self, position: tuple[int, int]):
        y = position[0]
        x = position[1]
        right_bound = len(self.raw_maze[0]) - 1
        lower_bound = len(self.raw_maze) - 1
        if y >= 1:
            if (y - 1, x) not in self.visited:
                upper_symbol = self.raw_maze[y - 1][x]
                if upper_symbol == "|" and y >= 2:
                    yield [(y - 1, x), (y - 2, x)]
                elif upper_symbol == "7" and x >= 1 and y >= 1:
                    yield [(y - 1, x), (y - 1, x - 1)]
                elif upper_symbol == "F" and x < right_bound and y >= 1:
                    yield [(y - 1, x), (y - 1, x + 1)]
        if x >= 1:
            if (y, x - 1) not in self.visited:
                left_symbol = self.raw_maze[y][x - 1]
                if left_symbol == "-" and x >= 2:
                    yield [(y, x - 1), (y, x - 2)]
                elif left_symbol == "L" and x >= 1 and y >= 1:
                    yield [(y, x - 1), (y - 1, x - 1)]
                elif left_symbol == "F" and x >= 1 and y < lower_bound:
                    yield [(y, x - 1), (y + 1, x - 1)]
        if y < len(self.raw_maze) - 1:
            if (y + 1, x) not in self.visited:
                lower_symbol = self.raw_maze[y + 1][x]
                if lower_symbol == "L" and x < right_bound and y < lower_bound:
                    yield [(y + 1, x), (y + 1, x + 1)]
                elif lower_symbol == "J" and x >= 1 and y < lower_bound:
                    yield [(y + 1, x), (y + 1, x - 1)]
                elif lower_symbol == "|" and y < lower_bound - 1:
                    yield [(y + 1, x), (y + 2, x)]
        if x < right_bound:
            if (y, x + 1) not in self.visited:
                right_symbol = self.raw_maze[y][x + 1]
                if right_symbol == "-" and x < right_bound - 1:
                    yield [(y, x + 1), (y, x + 2)]
                elif right_symbol == "J" and x < right_bound and y >= 1:
                    yield [(y, x + 1), (y - 1, x + 1)]
                elif (
                    right_symbol == "7" and x < right_bound and y < lower_bound
                ):
                    yield [(y, x + 1), (y + 1, x + 1)]

    def set_next_fields(
        self, base_position: tuple[int, int]
    ) -> list[tuple[int, int]]:
        fields = []
        for surr_positions in self.position_iterator(base_position):
            for i, surr_position in enumerate(surr_positions):
                y = surr_position[0]
                x = surr_position[1]
                symbol = self.raw_maze[y][x]
                if symbol == "." or symbol == "S":
                    continue
                elif (
                    self.number_maze[y][x]
                    >= self.number_maze[base_position[0]][base_position[1]] + 1
                ):
                    continue
                else:
                    if i == 0:
                        self.number_maze[y][x] = (
                            self.number_maze[base_position[0]][
                                base_position[1]
                            ]
                            + 1
                        )
                        self.visited.add((y, x))
                    if i == 1:
                        self.number_maze[y][x] = (
                            self.number_maze[surr_positions[0][0]][
                                surr_positions[0][1]
                            ]
                            + 1
                        )
                        fields = [(y, x)] + fields
        return fields

    def get_max_distance(self):
        return max(sum(self.number_maze, []))


def task01(input_data: list[str], test=True):
    maze = Maze(input_data)
    start_point = maze.get_start_point()
    if test:
        assert start_point == (2, 0)
    next_positions = [start_point]
    while next_positions:
        position = next_positions.pop(0)
        next_positions += maze.set_next_fields(position)
    max_dist = maze.get_max_distance()
    if test:
        assert max_dist == 8
    return max_dist


def task02(input_data: list[str], test=True):
    pass


task01(TEST_DATA)
print(task01(get_data(day), test=False))
task02(TEST_DATA)
print(task02(get_data(day), test=False))

# form into Nodes in a graph
# calculate distance for every node to another
#
