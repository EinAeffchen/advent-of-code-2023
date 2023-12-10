from dataclasses import dataclass
from collections import Counter
from utils import get_data
from pathlib import Path

day = int(Path(__file__).stem)

TEST_DATA = ["0 3 6 9 12 15", "1 3 6 10 15 21", "10 13 16 21 30 45"]


def predict_next_value(row: list[int]):
    return [row[i + 1] - number for i, number in enumerate(row[:-1])]


def parse_input(input_data: list[str]):
    for row in input_data:
        if row:
            yield [int(symbol) for symbol in row.split()]


def fill_gap(prediction_set: list[list[int]]):
    filled_set = list()
    for row in prediction_set[-1::-1]:
        if all_zeros(row):
            appendix = 0
        else:
            appendix = row[-1] + appendix
        filled_set.append(row + [appendix])
    return filled_set


def fill_gap_reverse(prediction_set: list[list[int]]):
    filled_set = list()
    for row in prediction_set[-1::-1]:
        if all_zeros(row):
            prependix = 0
        else:
            prependix = row[0] - prependix
        filled_set.append([prependix] + row)
    return filled_set


def all_zeros(row):
    return row[0] == 0 and len(set(row)) == 1


def task01(input_data: list[str], test=True):
    data = parse_input(input_data)
    parsed_data = list()
    for history in data:
        prediction = history
        prediction_set = [prediction]
        while not all_zeros(prediction):
            prediction = predict_next_value(prediction)
            prediction_set.append(prediction)
        parsed_data.append(fill_gap(prediction_set))
    result = sum([row[-1][-1] for row in parsed_data])
    if test:
        assert result == 114
    return result


def task02(input_data: list[str], test=True):
    data = parse_input(input_data)
    parsed_data = list()
    for history in data:
        prediction = history
        prediction_set = [prediction]
        while not all_zeros(prediction):
            prediction = predict_next_value(prediction)
            prediction_set.append(prediction)
        parsed_data.append(fill_gap_reverse(prediction_set))
    result = sum([row[-1][0] for row in parsed_data])
    if test:
        assert result == 2
    return result


task01(TEST_DATA)
print(task01(get_data(day), test=False))
task02(TEST_DATA)
print(task02(get_data(day), test=False))
