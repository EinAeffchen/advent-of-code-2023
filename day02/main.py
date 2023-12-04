from pathlib import Path
from functools import reduce


def read_lines(input_file: Path):
    with open(input_file, "r") as f_in:
        return f_in.readlines()


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


class NumberBlock:
    value: int
    adjacent = list[str]

    def __init__(self, input_rows: list[str]) -> None:
        raw_value = ""
        for i, row in enumerate(input_rows):
            for symbol in row:
                if symbol.isnumeric() and i == 1:
                    raw_value += symbol
                elif symbol != ".":
                    self.adjacent.append(symbol)


def parse_schematic(input_data: list):
    number_blocks = list()
    for x, row in enumerate(input_data):
        if x == 0:
            x_start = 0
        elif x == len(input_data):
            x_end = x
        else:
            x_start = x - 1
            x_end = x + 1
        for y, symbol in enumerate(row):
            if symbol.isnumeric():
                y_start = y
            else:
                y_end = y
                # TODO add padding around
                number_blocks.append(
                    NumberBlock(
                        [
                            row[y_start:y_end]
                            for row in input_data[x_start:x_end]
                        ]
                    )
                )


task01(TEST_DATA)
print(task01(data, test=False))
task02(TEST_DATA)
print(task02(data, test=False))
