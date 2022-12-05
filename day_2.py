from enum import IntEnum
from typing import List, Self

EXEMPLE = """\
A Y
B X
C Z
"""


class Outcome(IntEnum):
    LOSE = 0
    DRAW = 1
    WIN = 2


class Shape(IntEnum):
    ROCK = 0
    SCISSORS = 1
    PAPER = 2

    @property
    def score(self) -> int:
        SCORES = {"ROCK": 1, "PAPER": 2, "SCISSORS": 3}

        return SCORES[self.name]

    def get_fight_outcome(self, opponent: Self) -> Outcome:
        if opponent == self:
            return Outcome.DRAW
        if (opponent - self) % 3 == 1:
            return Outcome.WIN
        return Outcome.LOSE

    def get_shape_from_outcome(self, outcome: Outcome) -> Self:
        match outcome:
            case Outcome.WIN:
                return Shape((self - 1) % 3)
            case Outcome.DRAW:
                return Shape(self)
            case Outcome.LOSE:
                return Shape((self + 1) % 3)


OPPONENT_SHAPE = {"A": Shape.ROCK, "B": Shape.PAPER, "C": Shape.SCISSORS}

MY_SHAPE = {"X": Shape.ROCK, "Y": Shape.PAPER, "Z": Shape.SCISSORS}

FIGHT_OUTCOME = {"X": Outcome.LOSE, "Y": Outcome.DRAW, "Z": Outcome.WIN}


def compute_score_v1(rounds: List[str]) -> int:
    score = 0
    for round in rounds:
        opponent, me = round.split()
        outcome = MY_SHAPE[me].get_fight_outcome(OPPONENT_SHAPE[opponent])
        score += 3 * outcome + MY_SHAPE[me].score

    return score


def compute_score_v2(rounds: List[str]) -> int:
    score = 0
    for round in rounds:
        opponent, outcome = round.split()
        my_shape = OPPONENT_SHAPE[opponent].get_shape_from_outcome(FIGHT_OUTCOME[outcome])
        score += 3 * FIGHT_OUTCOME[outcome] + my_shape.score

    return score


def test_part_1():
    """Score  according to the v1 strategy guide"""
    assert compute_score_v1(EXEMPLE.splitlines()) == 15


def test_part_2():
    """Score  according to the v2 strategy guide"""
    assert compute_score_v2(EXEMPLE.splitlines()) == 12


if __name__ == "__main__":
    print("=== DAY 2 ===")
    with open("./day_2.txt") as f:
        lines = f.readlines()
        print(f"[Part 1] Total score v1 strategy guide: {compute_score_v1(lines)}")
        print(f"[Part 2] Total score v2 strategy guide: {compute_score_v2(lines)}")
