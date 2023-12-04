from pathlib import Path


def read_lines(input_file: Path):
    with open(input_file, "r") as f_in:
        return f_in.readlines()


data = read_lines(Path(__file__).parent / "input.txt")


def task1(input_data: list):
    row_sum = 0
    for row in input_data:
        numbers = [number for number in row if number.isnumeric()]
        result = int(f"{numbers[0]}{numbers[-1]}")
        row_sum += result
    return row_sum


def task2(input_data):
    numbers = {
        "one": "one1one",
        "two": "two2two",
        "three": "three3three",
        "four": "four4four",
        "five": "five5five",
        "six": "six6six",
        "seven": "seven7seven",
        "eight": "eight8eight",
        "nine": "nine9nine",
    }
    translated_data = list()
    for row in input_data:
        for text, number in numbers.items():
            row = row.replace(text, number)
        translated_data.append(row)
    return task1(translated_data)


print(task1(data))
print(task2(data))
