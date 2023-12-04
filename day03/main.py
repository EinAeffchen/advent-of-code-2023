from pathlib import Path
from dataclasses import dataclass


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


def parse_schematic(input_data: list):
    numbers = list()
    symbols = dict()
    for y, row in enumerate(input_data):
        number = ""
        coord = Coord(y=y)
        for x, symbol in enumerate(row):
            if symbol.isnumeric():
                number += symbol
                if coord.x is None:
                    coord.x = x
            elif symbol != ".":
                symbols[y] = symbols.get(y, []) + [x]
            if number != "" and not symbol.isnumeric():
                coord.length = len(number)
                coord.value = int(number)
                number = ""
                numbers.append(coord)
                coord = Coord(y=y)
    return numbers, symbols


def next_to_symbol(number: Coord, symbols: dict):
    for y in range(number.y - 1, number.y + 2):
        if row := symbols.get(y):
            if any(
                [
                    True
                    for i in range(number.x - 1, number.x + number.length + 1)
                    if i in row
                ]
            ):
                return True


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


task01(TEST_DATA)
print(task01(data, test=False))
# task02(TEST_DATA)
# print(task02(data, test=False))
