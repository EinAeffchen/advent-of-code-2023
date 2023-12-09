from dataclasses import dataclass
from utils import get_data
from math import lcm
from tqdm import tqdm

TEST_DATA = [
    "LLR",
    "",
    "AAA = (BBB, BBB)",
    "BBB = (AAA, ZZZ)",
    "ZZZ = (ZZZ, ZZZ)",
]
TEST_DATA2 = [
    "LR",
    "",
    "11A = (11B, XXX)",
    "11B = (XXX, 11Z)",
    "11Z = (11B, XXX)",
    "22A = (22B, XXX)",
    "22B = (22C, 22C)",
    "22C = (22Z, 22Z)",
    "22Z = (22B, 22B)",
    "XXX = (XXX, XXX)",
]


@dataclass
class Route:
    name: str
    left: str
    right: str

    def go_left(self):
        return self.left

    def go_right(self):
        return self.right


class Path:
    path: dict
    current: Route
    steps: 0

    def __init__(self, routes: list[Route], sequence: str):
        self.path = dict()
        for route in routes:
            self.path[route.name] = route
        self.steps = 0
        self.moves = {"L": "go_left", "R": "go_right"}
        self.sequence = sequence
        self.current = None

    def walk(self, start_node: str = "AAA", ghost_mode: bool = False):
        if not self.current:
            self.current = self.path[start_node]
        if ghost_mode:
            while self.current.name[-1] != "Z":
                self.step(start_node)
        else:
            while self.current.name != "ZZZ":
                self.step(start_node)
        return self.steps

    def step(self, start_node: str = "AAA"):
        if not self.current:
            self.current = self.path[start_node]
        route_name = getattr(
            self.current,
            self.moves[self.sequence[self.steps % len(self.sequence)]],
        )()
        self.current = self.path[route_name]
        self.steps += 1


class GhostMode:
    paths: list[Path]
    start_nodes: list[str]
    steps = 0

    def __init__(self, paths: list[Path], start_nodes: list[str]) -> None:
        assert len(paths) == len(start_nodes)
        self.paths = paths
        self.start_nodes = start_nodes

    def all_reached_goal(self):
        return all(
            [
                (
                    True
                    if path.current and path.current.name.endswith("Z")
                    else False
                )
                for path in self.paths
            ]
        )

    def walk(self):
        steps = list()
        while not self.all_reached_goal():
            for i, start_node in tqdm(enumerate(self.start_nodes)):
                steps.append(self.paths[i].walk(start_node, ghost_mode=True))
        return lcm(*steps)


def process_inputs(input_data: list[str]) -> tuple[str, list[Route]]:
    sequence = input_data[0]
    raw_routes = input_data[2:]
    routes = list()
    for raw_route in raw_routes:
        if raw_route == "":
            continue
        current, directions = raw_route.split("=")
        left, right = directions.split(",")
        routes.append(
            Route(
                current.strip(),
                left=left.replace("(", "").strip(),
                right=right.replace(")", "").strip(),
            )
        )
    return sequence, routes


def task01(input_data: list[str], test=True):
    seq, routes = process_inputs(input_data)
    p = Path(routes, seq)
    steps = p.walk()
    if test:
        assert steps == 6
    return steps


def task02(input_data: list[str], test=True):
    seq, routes = process_inputs(input_data)
    p = Path(routes, seq)
    start_points = [route for route in p.path.keys() if route[-1] == "A"]
    gm = GhostMode(
        [Path(routes, seq) for _ in range(len(start_points))], start_points
    )
    steps = gm.walk()
    if test:
        assert steps == 6
    return steps


task01(TEST_DATA)
print(task01(get_data(8), test=False))
task02(TEST_DATA2)
print(task02(get_data(8), test=False))
