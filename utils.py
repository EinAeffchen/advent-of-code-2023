import requests
from login import cookie
from pathlib import Path
from datetime import datetime


def get_data(day: int):
    p = Path(__file__).parent / "input.txt"
    if p.is_file():
        creation_date = datetime.fromtimestamp(p.stat().st_mtime)
        if creation_date.day == day:
            with open(p) as f_in:
                data = f_in.read()
            return [row for row in data.split("\n") if row]
    data = requests.get(
        f"https://adventofcode.com/2023/day/{day}/input", cookies=cookie
    ).text
    with open("input.txt", "w") as f_out:
        f_out.write(data)
    return [row for row in data.split("\n") if row]
