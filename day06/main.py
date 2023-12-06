from pathlib import Path
from tqdm import tqdm
from dataclasses import dataclass
from functools import reduce


def read_lines(input_file: Path):
    with open(input_file, "r") as f_in:
        return f_in.read().splitlines()


def parse_input(input_data: list[str]):
    times = input_data[0].split()[1:]
    distance = input_data[1].split()[1:]
    return list(zip(times, distance))


def parse_input2(input_data: list[str]):
    times = "".join(input_data[0].split()[1:])
    distance = "".join(input_data[1].split()[1:])
    return [[times, distance]]


@dataclass
class Boat:
    speed: int = 0

    def push_button(self, n):
        self.speed = n

    def travel(self, milliseconds: int):
        return self.speed * milliseconds


@dataclass
class Race:
    time: int
    record: int

    def recoard_beat(self, distance: int):
        return self.record < distance


data = read_lines(Path(__file__).parent / "input.txt")

TEST_DATA = ["Time:      7  15   30", "Distance:  9  40  200"]


def task01(input_data: list[str], test=True):
    race_data = parse_input(input_data)
    ways = list()
    for race in race_data:
        wins = 0
        r = Race(int(race[0]), int(race[1]))
        for i in range(r.time):
            boat = Boat()
            boat.push_button(i)
            if r.recoard_beat(boat.travel(r.time - i)):
                wins += 1
        ways.append(wins)
    if test:
        assert reduce((lambda x, y: x * y), ways) == 288
    return reduce((lambda x, y: x * y), ways)


def task02(input_data: list[str], test=True):
    race_data = parse_input2(input_data)
    ways = list()
    for race in race_data:
        wins = 0
        r = Race(int(race[0]), int(race[1]))
        for i in tqdm(list(range(r.time))):
            boat = Boat()
            boat.push_button(i)
            if r.recoard_beat(boat.travel(r.time - i)):
                wins += 1
        ways.append(wins)
    if test:
        assert reduce((lambda x, y: x * y), ways) == 71503
    return reduce((lambda x, y: x * y), ways)


task01(TEST_DATA)
print(task01(data, test=False))
task02(TEST_DATA)
print(task02(data, test=False))
