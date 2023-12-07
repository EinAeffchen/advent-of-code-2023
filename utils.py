import requests
from login import cookie
from pathlib import Path


def get_data(day: int):
    p = Path(__file__).parent / "input.txt"
    if not p.is_file():
        data = requests.get(
            f"https://adventofcode.com/2023/day/{day}/input", cookies=cookie
        ).text
        with open("input.txt", "w") as f_out:
            f_out.write(data)
    else:
        with open(p) as f_in:
            data = f_in.read()
    return data.split("\n")
