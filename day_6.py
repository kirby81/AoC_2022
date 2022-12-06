from io import StringIO
from typing import IO, List

EXAMPLE = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
]


def find_marker_subroutine(stream: IO[str], marker_size: int) -> int:
    start_marker: List[str] = list(reversed([stream.read(1) for _ in range(marker_size)]))
    while len(start_marker) > len(set(start_marker)):
        start_marker.pop()
        start_marker.insert(0, stream.read(1))
    return stream.tell()


def test_part_1():
    """How many characters need to be processed before the first start-of-packet marker is detected."""
    for stream, packet_marker_index, _ in EXAMPLE:
        assert find_marker_subroutine(StringIO(stream), 4) == packet_marker_index


def test_part_2():
    """How many characters need to be processed before the first start-of-message marker is detected."""
    for stream, _, message_marker_index in EXAMPLE:
        assert find_marker_subroutine(StringIO(stream), 14) == message_marker_index


if __name__ == "__main__":
    print("=== DAY 6 ===")
    with open("./day_6.txt") as f:
        print(f"[Part 1] Start-of-packet marker index: {find_marker_subroutine(f, 4)}")
        print(f"[Part 2] Start-of-message marker index: {find_marker_subroutine(f, 14)}")
