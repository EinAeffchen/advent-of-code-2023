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
        order = "J23456789TQKA"
        self.order = [symbol for symbol in order]

    def __lt__(self, other: "Card"):
        return self.order.index(self.symbol) < self.order.index(other.symbol)


@dataclass
class Hand:
    cards: list[Card]
    bid: int
    task2: bool = False

    def __post_init__(self):
        self.ranking = self._rank()

    def _count_joker(self):
        return len([True for card in self.cards if card.symbol == "J"])

    def _rank(self):
        counts = list(self._n_of_kind().values())
        if not counts:
            counts = [0]
        if self.task2:
            for _ in range(self._count_joker()):
                highest_number = max(counts)
                if highest_number != 5:
                    counts[counts.index(highest_number)] += 1
        if 5 in counts:
            value = 7
        elif 4 in counts:
            value = 6
        elif 3 in counts and 2 in counts:
            value = 5
        elif 3 in counts:
            value = 4
        elif Counter(counts)[2] == 2:
            value = 3
        elif 2 in counts:
            value = 2
        elif 1 in counts:
            value = 1
        else:
            value = 0
        return value

    def __lt__(self, other):
        if self.ranking == other.ranking:
            for i in range(len(self.cards)):
                if self.cards[i] != other.cards[i]:
                    return self.cards[i] < other.cards[i]
        else:
            return self.ranking < other.ranking

    def _hand_to_string(self):
        return "".join([card.symbol for card in self.cards])

    def _n_of_kind(self):
        count_string = self._hand_to_string()
        if self.task2:
            count_string = count_string.replace("J", "")
        return Counter(count_string)


def calculate_winnings(hands: list[Hand]):
    return sum([(i + 1) * hand.bid for i, hand in enumerate(hands)])


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


def task02(input_data: list[str], test=True):
    hands = list()
    for row in input_data:
        if row != "":
            raw_cards, bid = row.split()
            hand = Hand(
                [Card(symbol) for symbol in raw_cards], int(bid), task2=True
            )
            hands.append(hand)
    hands.sort()
    winnings = calculate_winnings(hands)
    if test:
        assert winnings == 5905
    return winnings


task01(TEST_DATA)
print(task01(get_data(7), test=False))
task02(TEST_DATA)
print(task02(get_data(7), test=False))
