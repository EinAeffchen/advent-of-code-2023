from pathlib import Path
from tqdm import tqdm


def read_lines(input_file: Path):
    with open(input_file, "r") as f_in:
        return f_in.readlines()


class ScratchCard:
    winning_numbers: set[int]
    draws: set[int]
    card_id: int

    def __init__(self, data_row: str):
        card, data = data_row.split(":")
        _, self.card_id = card.split()
        winning_numbers, draws = data.split("|")
        self.winning_numbers = {
            int(number) for number in winning_numbers.split()
        }
        self.draws = {int(number) for number in draws.split()}

    def calculate_win(self):
        hits = self.get_hits()
        if hits == 0:
            return 0
        if hits == 1:
            return 1
        else:
            return 1 * 2 ** (hits - 1)

    def get_hits(self):
        return len(self.draws & self.winning_numbers)


TEST_DATA = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]

data = read_lines(Path(__file__).parent / "input.txt")


def task01(input_data, test=True):
    points = 0
    for row in input_data:
        card = ScratchCard(row)
        points += card.calculate_win()
    if test:
        assert points == 13
    print(points)


def task02(input_data, test=True):
    stack = []
    card_count = 0
    debug_book = {}
    for row in tqdm(input_data):
        try:
            repeater = stack.pop(0)
        except IndexError:
            repeater = 0
        for _ in range(repeater + 1):
            card = ScratchCard(row)
            card_count += 1
            hits = card.get_hits()
            for i in range(hits):
                if len(stack) > i:
                    stack[i] += 1
                else:
                    stack.append(1)
        debug_book[card.card_id] = repeater
    if test:
        assert card_count == 30
    return card_count


task01(TEST_DATA)
print(task01(data, test=False))
task02(TEST_DATA)
print(task02(data, test=False))
