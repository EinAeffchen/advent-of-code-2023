from pathlib import Path
from tqdm import tqdm


def read_lines(input_file: Path):
    with open(input_file, "r") as f_in:
        return f_in.read()


def parse_input(input_data: list[str]) -> dict:
    input_data = input_data.split("\n")
    seeds = input_data[0]
    title = ""
    maps = dict()
    maps["seeds"] = [int(seed) for seed in seeds.split(": ")[1].split()]
    for row in input_data[2:]:
        if row == "":
            continue
        first_element = row.split()[0]
        if not first_element.isnumeric():
            title = first_element
            maps[title] = list()
        else:
            maps[title].append([int(number) for number in row.split()])
    return maps


data = read_lines(Path(__file__).parent / "input.txt")

TEST_DATA = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def convert_map(row: list[int], seed: int) -> int:
    value = None
    continue_marker = False
    if seed >= row[1] and seed <= row[1] + row[2]:
        value = row[0] - row[1] + seed
        continue_marker = True
    return value or seed, continue_marker


def convert_range(row: list[int], seeds: list[int]) -> int:
    # row: destination source range
    # seeds: start_value, range
    # map:          45678
    # var1:        345
    # var2:          567
    # var3:            789
    # -> return missed, mappend_seeds
    # missed seeds have to be mapped against leftover rows
    seeds_min = seeds[0]
    seeds_max = seeds[0] + seeds[1]
    destination = row[0]
    target_min = row[1]
    target_max = row[1] + row[2]
    if seeds_max < target_min:  # seeds all lower than range
        return seeds, []
    elif seeds_min > target_max:
        return seeds, []
    # full match
    elif seeds_min >= target_min and seeds_max <= target_max:
        seeds[0] = destination - target_min + seeds[0]
        return [], seeds
    # left partial intersection
    #   678910
    #   45678
    # 23456
    elif seeds_min <= target_min and seeds_max <= target_max:
        leftover_range = target_min - seeds_min
        unmapped_seeds = [seeds_min, leftover_range]
        mapped_seeds = [destination, seeds[1] - leftover_range]
        return unmapped_seeds, mapped_seeds
    # right partial intersection
    #   678910
    #   45678
    #      78910
    elif seeds_min >= target_min and seeds_max >= target_max:
        leftover_range = seeds_max - target_max
        unmapped_seeds = [target_max, leftover_range]
        mapped_seeds = [
            destination - target_min + seeds_min,
            seeds[1] - leftover_range,
        ]
        return unmapped_seeds, mapped_seeds
    else:
        print("WHAT?!")


# destination, source, range
def convert_to_location(maps: dict, seed: int):
    order = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]
    for map in order:
        for row in maps[map]:
            seed, continue_marker = convert_map(row, seed)
            if continue_marker:
                break
    return seed


def convert_to_location_by_range(maps: dict, mapping_dict: dict):
    order = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]
    for map in order:
        unmapped_seeds = mapping_dict.pop(map)
        for unmapped in unmapped_seeds:
            for i, row in enumerate(maps[map]):
                final = i == len(maps[map]) - 1
                unmapped, mapped_seeds = convert_range(row, unmapped)
                if mapped_seeds:
                    try:
                        mapping_dict[order[order.index(map) + 1]] = (
                            mapping_dict.get(order[order.index(map) + 1], [])
                            + [mapped_seeds]
                        )
                    except IndexError:
                        mapping_dict["final"] = mapped_seeds
                if not unmapped:
                    break
            if final and unmapped:
                try:
                    mapping_dict[order[order.index(map) + 1]] = (
                        mapping_dict.get(order[order.index(map) + 1], [])
                        + [unmapped]
                    )
                except IndexError:
                    mapping_dict["final"] = unmapped
    return mapping_dict


def task01(input_data: str, test=True):
    maps = parse_input(input_data)
    locations = []
    for seed in maps["seeds"]:
        locations.append(convert_to_location(maps, seed))
    if test:
        assert min(locations) == 35
    return min(locations)


def task02(input_data: str, test=True):
    maps = parse_input(input_data)
    seeds = [maps["seeds"][i : i + 2] for i in range(0, len(maps["seeds"]), 2)]
    locations = convert_to_location_by_range(maps, {"seed-to-soil": seeds})
    if test:
        assert min(locations["final"]) == 46
    return min(locations)


task01(TEST_DATA)
print(task01(data, test=False))
task02(TEST_DATA)
# print(task02(data, test=False))
