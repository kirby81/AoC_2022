import re
from queue import LifoQueue
from typing import List

EXAMPLE = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""  # noqa W291


class Dock:
    def __init__(self, dock_map: List[str]) -> None:
        nb_stack = int(dock_map[-1].strip()[-1])
        self.stacks: List[LifoQueue[str]] = [LifoQueue() for i in range(nb_stack)]

        for line in reversed(dock_map[: len(dock_map) - 1]):
            for match in re.finditer(r"[A-Z]", line):
                self.store_crate(int(dock_map[-1][match.start(0)]), match.group(0))

    def pickup_crate(self, stack_number: int) -> str:
        return self.stacks[stack_number - 1].get()

    def store_crate(self, stack_number: int, crate: str) -> None:
        self.stacks[stack_number - 1].put(crate)

    def get_top_crates(self) -> str:
        result = ""
        for stack in self.stacks:
            result += stack.get()

        return result


class Crane:
    def execute_command(self, command: str, dock: Dock) -> None:
        raise NotImplementedError


class CrateMover9000(Crane):
    def execute_command(self, command: str, dock: Dock) -> None:
        nb_item, origin_stack, destination_stack = [int(s) for s in re.findall(r"\d+", command)]
        for _ in range(nb_item):
            dock.store_crate(destination_stack, dock.pickup_crate(origin_stack))


class CrateMover9001(Crane):
    def __init__(self) -> None:
        self.queue = LifoQueue()

    def execute_command(self, command: str, dock: Dock) -> None:
        nb_item, origin_stack, destination_stack = [int(s) for s in re.findall(r"\d+", command)]
        for _ in range(nb_item):
            self.queue.put(dock.pickup_crate(origin_stack))

        while not self.queue.empty():
            dock.store_crate(destination_stack, self.queue.get())


def execute_procedure(procedure: List[str], crane: Crane) -> str:
    dock_map = procedure[: procedure.index("")]
    dock = Dock(dock_map)

    for command in procedure[procedure.index("") + 1 :]:
        crane.execute_command(command, dock)

    return dock.get_top_crates()


def test_part_1():
    """What crate ends up on top of each stack with the CrateMover9000."""
    assert execute_procedure(EXAMPLE.splitlines(), CrateMover9000()) == "CMZ"


def test_part_2():
    """What crate ends up on top of each stack with the CrateMover9001."""
    assert execute_procedure(EXAMPLE.splitlines(), CrateMover9001()) == "MCD"


if __name__ == "__main__":
    print("=== DAY 5 ===")
    with open("./day_5.txt") as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
        print(
            f"[Part 1] Crates on top of each stack with a CrateMover9000: {execute_procedure(lines, CrateMover9000())}"
        )
        print(
            f"[Part 2] Crates on top of each stack with a CrateMover9001: {execute_procedure(lines, CrateMover9001())}"
        )
