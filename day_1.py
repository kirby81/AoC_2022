from io import StringIO
from typing import IO, List

EXAMPLE = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


def count_next_elf_calories(stream: IO[str]) -> int:
    nb_calorie = 0
    line = stream.readline()
    if line == "":
        raise EOFError
    while line != "\n" and line != "":
        nb_calorie += int(line)
        line = stream.readline()

    return nb_calorie


def get_most_calories(stream: IO[str]) -> int:
    most_calories = 0
    while True:
        try:
            nb_calories = count_next_elf_calories(stream)
        except EOFError:
            break
        if nb_calories > most_calories:
            most_calories = nb_calories

    return most_calories


def get_top3_calories(stream: IO[str]) -> int:
    elfs_calories: List[int] = []
    while True:
        try:
            elfs_calories.append(count_next_elf_calories(stream))
        except EOFError:
            break

    return sum(sorted(elfs_calories, reverse=True)[:3])


def test_part_1():
    """Find the Elf carrying the most Calories."""
    assert get_most_calories(StringIO(EXAMPLE)) == 24000


def test_part_2():
    """Find the top three Elves carrying the most Calories."""
    assert get_top3_calories(StringIO(EXAMPLE)) == 45000


if __name__ == "__main__":
    print("=== DAY 1 ===")
    with open("./day_1.txt") as f:
        print(f"[Part 1] Total calories of the Elf carrying the most: {get_most_calories(f)} calories")
        f.seek(0)
        print(f"[Part 2] Total calories of the top 3 Elfs carrying the most: {get_top3_calories(f)} calories")
