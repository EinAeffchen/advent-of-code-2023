from dataclasses import dataclass
from functools import reduce
from pathlib import Path


def read_lines(input_file: Path):
    with open(input_file, "r") as f_in:
        return f_in.read().splitlines()


TEST_DATA = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]

data = read_lines(Path(__file__).parent / "input.txt")


@dataclass
class Coord:
    x: int = None
    y: int = 0
    length: int = 0
    value: int = None

    def __hash__(self):
        return hash((getattr(self, key) for key in self.__annotations__))


def parse_schematic(input_data: list):
    numbers = list()
    symbols = dict()
    number = ""
    for y, row in enumerate(input_data):
        if number != "":
            coord.length = len(number)
            coord.value = int(number)
            number = ""
            numbers.append(coord)
            coord = Coord(y=y)
        coord = Coord(y=y)
        for x, symbol in enumerate(row):
            if symbol.isnumeric():
                number += symbol
                if coord.x is None:
                    coord.x = x
            elif symbol != ".":
                symbols[y] = symbols.get(y, []) + [Coord(x, y, 1, symbol)]
                if number != "":
                    coord.length = len(number)
                    coord.value = int(number)
                    number = ""
                    numbers.append(coord)
                    coord = Coord(y=y)
            if number != "" and not symbol.isnumeric():
                coord.length = len(number)
                coord.value = int(number)
                number = ""
                numbers.append(coord)
                coord = Coord(y=y)
    return numbers, symbols


def next_to_symbol(number: Coord, symbols: dict) -> list[Coord]:
    coords = []
    for y in range(number.y - 1, number.y + 2):
        if y < 0:
            continue
        if row := symbols.get(y):
            for i in range(number.x - 1, number.x + number.length + 1):
                for coord in row:
                    if coord.x == i:
                        coords.append(coord)
    return coords


def task01(input_data: list[str], test=True):
    numbers, symbols = parse_schematic(input_data)
    number_sum = 0
    number: Coord
    for number in numbers:
        if next_to_symbol(number, symbols):
            number_sum += number.value
    if test:
        assert number_sum == 4361
    return number_sum


def task02(input_data: list[str], test=True):
    numbers, symbols = parse_schematic(input_data)
    number_sum = 0
    combinations = dict()
    number: Coord
    for number in numbers:
        if coords := next_to_symbol(number, symbols):
            for coord in coords:
                if coord.value == "*":
                    combinations[coord] = combinations.get(coord, []) + [
                        number
                    ]
    for coord, connected_numbers in combinations.items():
        if len(connected_numbers) > 1:
            number_sum += reduce(
                (lambda x, y: x.value * y.value), connected_numbers
            )
    if test:
        assert number_sum == 467835
    return number_sum


task01(TEST_DATA)
print(task01(data, test=False))
task02(TEST_DATA)
print(task02(data, test=False))
