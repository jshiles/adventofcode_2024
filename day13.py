import argparse
import sys
from collections.abc import Sequence
from collections import deque
from dataclasses import dataclass
from typing import Optional
from heapq import heappush, heappop
from math import sqrt


@dataclass(frozen=True)
class Position:
    x: int
    y: int


@dataclass(frozen=True)
class Move:
    x: int
    y: int
    cost: int


def solve_equation(target: Position, moves: list[Move], offset: int = 0) -> int:
    """
    Solves the 2-equation linear system. In this special case, each move has a
    cost so A and B are multiplied by their cost for a single int return value.
        A = (p_x*b_y - prize_y*b_x) / (a_x*b_y - a_y*b_x)
        B = (a_x*p_y - a_y*p_x) / (a_x*b_y - a_y*b_x)

    :param target: Position containing the location of the prize.
    :param moves: list[Move] containing the A, B button movements with cost.
    :return: int
    """
    # Part 2 adjusts the regular target position
    if offset != 0:
        target = Position(target.x + offset, target.y + offset)

    #
    denom = moves[0].x * moves[1].y - moves[0].y * moves[1].x
    move_0 = int(round((target.x * moves[1].y - target.y * moves[1].x) / denom))
    move_1 = int(round((target.y * moves[0].x - target.x * moves[0].y) / denom))
    end_position = Position(
        move_0 * moves[0].x + move_1 * moves[1].x,
        move_0 * moves[0].y + move_1 * moves[1].y,
    )
    if end_position == target:
        return move_0 * moves[0].cost + move_1 * moves[1].cost

    return 0


def parse_input_and_generate_data(path):
    """
    Parses the input text to extract Button moves and Prize positions.

    :param input_text: String containing Button moves and Prize positions.
    :return: List of tuples (Position, List[Move]).
    """
    with open(path, "r") as file:
        lines = file.read().strip().split("\n")
        games = []

        moves = []
        target = None

        for line in lines:
            if line.startswith("Button"):
                # Extract Button move details
                parts = line.split(":")[1].strip().split(", ")
                x = int(parts[0].split("+")[1])
                y = int(parts[1].split("+")[1])
                cost = 3 if "A" in line else 1  # Assign cost based on button type
                moves.append(Move(x, y, cost))
            elif line.startswith("Prize"):
                # Extract Prize position
                parts = line.split(":")[1].strip().split(", ")
                x = int(parts[0].split("=")[1])
                y = int(parts[1].split("=")[1])
                target = Position(x, y)
                # Append the current set of moves and target position to the result
                games.append((target, moves))
                moves = []  # Reset moves for the next section

    return games


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/13
    """
    args = parse_args(argv)
    data = parse_input_and_generate_data(args.file)

    costs = sum(
        [
            solve_equation(target, moves)
            for target, moves in parse_input_and_generate_data(args.file)
        ]
    )
    print(f"Part 1: {costs}")

    costs = sum(
        [
            solve_equation(target, moves, 10000000000000)
            for target, moves in parse_input_and_generate_data(args.file)
        ]
    )
    print(f"Part 2: {costs}")


if __name__ == "__main__":
    main(sys.argv[1:])
