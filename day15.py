import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from types import new_class
from typing import Optional
from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @classmethod
    def from_char(cls, char):
        mapping = {
            "^": cls.UP,
            "v": cls.DOWN,
            "<": cls.LEFT,
            ">": cls.RIGHT,
        }
        return mapping.get(char, None)


@dataclass
class OccupiedPosition:
    row: int
    col: int
    obj: str

    def distance(self) -> int:
        return 100 * self.row + self.col


def move_robot(puzzle_path: str) -> int:
    """
    Simulate the robots movement from the puzzle input and return the sum of
    the gps coordinates, according the logic.
    :param puzzle_path: str, file path of the input logic
    :returns: int
    """

    def move_once(idx: int, move: str) -> Optional[dict[int, tuple[int, int]]]:
        if objects[idx].obj == "#":
            return None  # cannot move walls.

        dir = Direction.from_char(move)
        if dir is None:
            raise ValueError(f"{move} is not understood")
        d_row, d_col = dir.value
        new_row, new_col = objects[idx].row + d_row, objects[idx].col + d_col

        required_moves = {}
        for blocking_idx, blocking_obj in enumerate(objects):
            if new_row == blocking_obj.row and new_col == blocking_obj.col:
                # In part 2, we have to deal with double wide boxes, which may create
                # adjancent boxes to care about when moving up or down.
                adjacent_obj_idx = None
                if blocking_obj.obj == "[" and dir in [Direction.UP, Direction.DOWN]:
                    adjacent_obj_idx = [
                        idx
                        for idx, x in enumerate(objects)
                        if x.row == blocking_obj.row
                        and x.col == blocking_obj.col + 1
                        and x.obj == "]"
                    ][0]
                elif blocking_obj.obj == "]" and dir in [Direction.UP, Direction.DOWN]:
                    adjacent_obj_idx = [
                        idx
                        for idx, x in enumerate(objects)
                        if x.row == blocking_obj.row
                        and x.col == blocking_obj.col - 1
                        and x.obj == "["
                    ][0]

                # If we have an adjacent box, let's try to recursively move it and
                # return the list of moves.
                if adjacent_obj_idx is not None:
                    child_moves_adj = move_once(adjacent_obj_idx, move)
                    if child_moves_adj is None:
                        return None
                    else:
                        required_moves = required_moves | child_moves_adj

                # Let's try to recursively move child boxes and return the list of
                # moves.
                child_moves = move_once(blocking_idx, move)
                if child_moves is None:
                    return None
                else:
                    required_moves = required_moves | child_moves

        # Assuming we have not failed yet, let's add the current space to the
        # list of moves.
        required_moves[idx] = (new_row, new_col)
        return required_moves

    # Read puzzle input
    objects = find_positions(puzzle_path)
    moves = find_moves(puzzle_path)

    for m_count, m in enumerate(moves):
        robot = [idx for idx, obj in enumerate(objects) if obj.obj == "@"][0]
        required_moves = move_once(robot, m)

        # if None, then moves in this direction are not possible, so just move on.
        if required_moves is not None:
            for idx, move in required_moves.items():
                objects[idx].row = move[0]
                objects[idx].col = move[1]

    # After all moves, return the GPS coordinates of the boxes.
    sum_gps = sum([b.distance() for b in objects if b.obj in ["[", "O"]])
    return sum_gps


def find_positions(file_path: str) -> list[OccupiedPosition]:
    """Finds all positions of a given symbol in the list of lines."""
    positions = []
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char in ["@", "#", "O", "[", "]"]:
                    positions.append(OccupiedPosition(row, col, char))
    return positions


def find_moves(file_path: str) -> list[str]:
    """Finds all moves of a given symbol in the list of lines."""
    moves = []
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char in ["^", "v", "<", ">"]:
                    moves.append(char)
    return moves


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/15
    """
    args = parse_args(argv)

    sum_gps = move_robot(args.file)
    print(f"{sum_gps}")


if __name__ == "__main__":
    main(sys.argv[1:])
