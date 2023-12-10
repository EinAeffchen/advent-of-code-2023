from dataclasses import dataclass
from collections import Counter
from utils import get_data
from pathlib import Path

day = int(Path(__file__).stem)

TEST_DATA = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483",
]


def task01(input_data: list[str], test=True):
    pass


def task02(input_data: list[str], test=True):
    pass


task01(TEST_DATA)
print(task01(get_data(day), test=False))
task02(TEST_DATA)
print(task02(get_data(day), test=False))
