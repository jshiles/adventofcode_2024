import argparse
import sys
from collections.abc import Sequence
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


class LoopDetected(Exception):
    """Custom exception for detecting a loop."""
    def __init__(self, message="A loop was detected"):
        super().__init__(message)


@dataclass(frozen=True)
class Location:
    x: int
    y: int

    def next_space(self, d: Direction):
        return Location(self.x+d.value[0], self.y+d.value[1])


def turn_right(d: Direction) -> Direction:
    """Turn 90 degrees"""
    turn_map = {
        Direction.NORTH: Direction.EAST,
        Direction.EAST: Direction.SOUTH,
        Direction.SOUTH: Direction.WEST,
        Direction.WEST: Direction.NORTH
    }
    return turn_map[d]


def guards_walking_path(grid:list[list[str]], sp: Location) -> set[tuple[Location, Direction]]:
    """
    Return a list of set of spaces and direction the the guard is walking.
    Raises a LoopDetected error when the cycle will never end.
    """

    rows, cols = len(grid), len(grid[0])

    def still_on_board(sp: Location) -> bool:
        return True if 0 <= sp.x < rows and 0 <= sp.y < cols else False

    path: set = set()
    current_direction = Direction.NORTH

    path.add((sp, current_direction))
    current_location = sp
    next_space = current_location.next_space(current_direction)

    while still_on_board(next_space):
        if not grid[next_space.y][next_space.x] == '#':
            current_location = next_space
            next_space = current_location.next_space(current_direction)
            if (current_location, current_direction) in path:
                raise LoopDetected("Loop detected in the walk!")
            path.add((current_location, current_direction))
        else:
            current_direction = turn_right(current_direction)
            next_space = current_location.next_space(current_direction)

    return path


def detect_loops(grid:list[list[str]], sp: Location) -> int:
    """
    Insert obsticals are a systematic set of locations based on our knowledge
    of where the guard will walk. If that raises a loop, then we count and we
    return the final count.
    """
    rows, cols = len(grid), len(grid[0])

    steps = guards_walking_path(grid, sp)
    unique_spaces = {t[0] for t in steps}

    obsticals_creating_loop: list[Location] = []
    for obsticle_loc in unique_spaces:
        x = obsticle_loc.x
        y = obsticle_loc.y
        if grid[y][x] == '#' or (sp.x == x and sp.y == y):
            continue
        try:
            new_grid = deepcopy(grid)
            new_grid[y][x] = '#'
            guards_walking_path(new_grid, sp)
        except LoopDetected as e:
            obsticals_creating_loop.append(Location(x, y))
            # print(f"Handled exception ({x},{y}): {e}")

    return len(obsticals_creating_loop)


def process_grid(file_path: str) -> tuple[list[list[str]], Location]:
    """
    Read the grid from the file into a list of lists, and find the starting
    point. Return them as tuple.
    """
    grid = []
    position = Location(0,0)

    with open(file_path, 'r') as file:
        for row_idx, line in enumerate(file):
            row = list(line.strip())
            for col_idx, char in enumerate(row):
                if char == "^":
                    position = Location(col_idx, row_idx)
                    row[col_idx] = "."
            grid.append(row)

    return grid, position


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/6
    """
    args = parse_args(argv)
    grid, starting_position = process_grid(args.file)

    steps = guards_walking_path(grid, starting_position)
    unique_spaces = {t[0] for t in steps}
    print(f"Part 1: {len(unique_spaces)}")

    loops = detect_loops(grid, starting_position)
    print(f"Part 2: {loops}")


if __name__ == "__main__":
    main(sys.argv[1:])
