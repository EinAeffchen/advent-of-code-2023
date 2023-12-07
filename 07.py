from dataclasses import dataclass
from collections import Counter
from utils import get_data

TEST_DATA = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483",
]


def parse_input(input_data: list[str]):
    hands: list[dict] = []
    for row in input_data:
        hand, bid = row.split()
        data = {"hand": hand, "bid": bid}
        hands.append(data)
    return hands


@dataclass
class Card:
    symbol: str

    def __post_init__(self):
        order = "23456789TJQKA"
        self.order = [symbol for symbol in order]

    def __lt__(self, other: "Card"):
        return self.order.index(self.symbol) < self.order.index(other.symbol)


@dataclass
class Hand:
    cards: list[Card]
    bid: int

    def __post_init__(self):
        self.ranking = self.rank()

    def rank(self):
        counts = self.n_of_kind().values()
        if 5 in counts:
            return 7
        elif 4 in counts:
            return 6
        elif 3 in counts and 2 in counts:
            return 5
        elif 3 in counts:
            return 4
        elif 2 in counts:
            return 3
        elif 1 in counts:
            return 2
        else:
            return 0

    def __lt__(self, other):
        if self.ranking == other.ranking:
            for i in range(len(self.cards)):
                if self.cards[i] != other.cards[i]:
                    return self.cards[i] < other.cards[i]
        else:
            return self.ranking < other.ranking

    def _hand_to_string(self):
        return "".join([card.symbol for card in self.cards])

    def n_of_kind(self):
        return Counter(self._hand_to_string())


def calculate_winnings(hands: list[Hand]):
    # return sum([(i + 1) * hand.bid for i, hand in enumerate(hands)])
    summe = 0
    for i, hand in enumerate(hands):
        summe += (i + 1) * hand.bid
    return summe


def task01(input_data: list[str], test=True):
    hands = list()
    for row in input_data:
        if row != "":
            raw_cards, bid = row.split()
            hand = Hand([Card(symbol) for symbol in raw_cards], int(bid))
            hands.append(hand)
    hands.sort()
    winnings = calculate_winnings(hands)
    if test:
        assert winnings == 6440
    return winnings


task01(TEST_DATA)
print(task01(get_data(7), test=False))
# task02(TEST_DATA)
# print(task02(data, test=False))
