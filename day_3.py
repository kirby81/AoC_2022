from more_itertools import chunked, divide
from typing import List

EXEMPLE = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


def get_item_priority(char: str) -> int:
    if char >= "a":
        return ord(char) - ord("a") + 1  # [a-z] -> [1-26]
    return ord(char) - ord("A") + 27  # [A-Z] -> [27-52]


def get_common_item(rucksack: str) -> str:
    compartment_1, compartment_2 = divide(2, rucksack)
    return list(set(compartment_1).intersection(compartment_2))[0]


def get_common_item_priority(rucksack: str) -> int:
    item = get_common_item(rucksack)
    return get_item_priority(item)


def sum_common_items_priorities(rucksacks: List[str]) -> int:
    return sum([get_common_item_priority(rucksack) for rucksack in rucksacks])


def sum_group_badges_priorities(rucksacks: List[str]) -> int:
    sum_badges_prority = 0
    for chunk in chunked(rucksacks, 3):
        sum_badges_prority += get_item_priority(set(chunk[0]).intersection(*chunk).pop())
    return sum_badges_prority


def test_part_1():
    """What is the sum of the priorities of common items."""
    assert sum_common_items_priorities(EXEMPLE.splitlines()) == 157


def test_part_2():
    """What is the sum of the priorities of group's badges."""
    assert sum_group_badges_priorities(EXEMPLE.splitlines()) == 70


if __name__ == "__main__":
    print("=== DAY 3 ===")
    with open("./day_3.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        print(f"[Part 1] Sum of the priorities of common items: {sum_common_items_priorities(lines)}")
        print(f"[Part 2] Sum of group's badges priorities: {sum_group_badges_priorities(lines)}")
