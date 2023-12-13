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
    visited: set

    def __post_init__(self):
        self.START = "S"
        self.number_maze = [[0 for _ in row] for row in self.raw_maze]
        self.route = []

    def get_start_point(self):
        for y, row in enumerate(self.raw_maze):
            x = row.find(self.START)
            if x != -1:
                self.number_maze[y][x] = 0
                self.start_position = (y, x)

    def position_iterator(self, position: tuple[int, int], steps: int = 0):
        y = position[0]
        x = position[1]
        symbol = self.raw_maze[y][x]
        previous_position = list(self.route[steps - 1].keys())[0]
        if symbol == ".":
            return
        elif symbol == self.START:
            next_position = self.position_iterator((y - 1, x))
            if next_position:
                return (y - 1, x)
            next_position = self.position_iterator((y + 1, x))
            if next_position:
                return (y + 1, x)
            next_position = self.position_iterator((y, x - 1))
            if next_position:
                return (y, x - 1)
            next_position = self.position_iterator((y, x + 1))
            if next_position:
                return (y, x + 1)
        elif symbol == "|":
            if previous_position and previous_position == (y - 1, x):
                return (y + 1, x)  # north
            else:
                return (y - 1, x)  # south
        elif symbol == "-":
            if previous_position and previous_position == (y, x - 1):
                return (y, x + 1)  # right
            else:
                return (y, x - 1)  # left
        elif symbol == "L":
            if previous_position and previous_position == (y, x + 1):
                return (y - 1, x)  # north
            else:
                return (y, x + 1)  # east
        elif symbol == "J":
            if previous_position and previous_position == (y, x - 1):
                return (y - 1, x)  # north
            else:
                return (y, x - 1)  # west
        elif symbol == "7":
            if previous_position and previous_position == (y, x - 1):
                return (y + 1, x)  # south
            else:
                return (y, x - 1)  # west
        elif symbol == "F":
            if previous_position and previous_position == (y, x + 1):
                return (y + 1, x)  # south
            else:
                return (y, x + 1)  # west

    def walk_maze(self) -> list[tuple[int, int]]:
        next_position = self.start_position
        steps = 0
        self.route.append({(next_position[0], next_position[1]): self.START})
        while next_position := self.position_iterator(next_position, steps):
            if next_position == self.start_position:
                break
            previous_position = list(self.route[steps].keys())[0]
            y = next_position[0]
            x = next_position[1]
            self.number_maze[y][x] = (
                self.number_maze[previous_position[0]][previous_position[1]]
                + 1
            )
            self.visited.add((y, x))
            self.route.append({(y, x): self.raw_maze[y][x]})
            steps += 1

    def get_max_distance(self):
        return (max(sum(self.number_maze, [])) + 1) / 2


def task01(input_data: list[str], test=True):
    maze = Maze(input_data, set())
    maze.get_start_point()
    if test:
        assert maze.start_position == (2, 0)
    maze.walk_maze()
    max_dist = maze.get_max_distance()
    if test:
        assert max_dist == 8
    return max_dist


def task02(input_data: list[str], test=True):
    maze = Maze(input_data, set())
    maze.get_start_point()
    maze.walk_maze()
    with open("maze.txt", "w") as f_out:
        for row in maze.number_maze:
            f_out.write("".join(["█" if s > 0 else " " for s in row]) + "\n")


task01(TEST_DATA)
print(task01(get_data(day), test=False))
# task02(TEST_DATA)
print(task02(get_data(day), test=False))

# form into Nodes in a graph
# calculate distance for every node to another
#
