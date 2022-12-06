from typing import Callable, List, Tuple

EXAMPLE = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

Counting_method = Callable[[List[int], List[int]], bool]


def fully_contain(assignment_1: List[int], assignment_2: List[int]) -> bool:
    union_list = list(set(assignment_1) | set(assignment_2))
    return max(len(assignment_1), len(assignment_2)) == len(union_list)


def overlap(assignment_1: List[int], assignment_2: List[int]) -> bool:
    union_list = list(set(assignment_1) | set(assignment_2))
    return len(union_list) < (len(assignment_1) + len(assignment_2))


def get_assignment_pair(assignement_pair: str) -> Tuple[List[int], List[int]]:
    first_assignement_range, second_assignement_range = assignement_pair.split(",")
    return get_list_from_range(first_assignement_range), get_list_from_range(second_assignement_range)


def get_list_from_range(assignement_range: str) -> List[int]:
    lower_bound, upper_bound = assignement_range.split("-")
    return [*range(int(lower_bound), int(upper_bound) + 1)]


def count_assignements_pair(assignements_list: List[str], counting_method: Counting_method) -> int:
    counter = 0
    for assignement_pair in assignements_list:
        assignement_1, assignement_2 = get_assignment_pair(assignement_pair)
        if counting_method(assignement_1, assignement_2):
            counter += 1

    return counter


def test_part_1():
    """In how many assignment pairs does one range fully contain the other."""
    assert count_assignements_pair(EXAMPLE.splitlines(), fully_contain) == 2


def test_part_2():
    """In how many assignment pairs do the ranges overlap."""
    assert count_assignements_pair(EXAMPLE.splitlines(), overlap) == 4


if __name__ == "__main__":
    print("=== DAY 4 ===")
    with open("./day_4.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        print(f"[Part 1] Number of fully contain pair assignements: {count_assignements_pair(lines, fully_contain)}")
        print(f"[Part 2] Number of overlapping pair assignements: {count_assignements_pair(lines, overlap)}")
