import argparse
import sys
from collections.abc import Sequence
from typing import Optional


def process_grids(grids: list[list[str]]) -> tuple[list[list[int]], list[list[int]]]:
    def transpose_horizontal(matrix):
        return matrix[::-1]

    def compute_grid(grid):
        """Computes the result of the grid."""
        result = []
        for col in range(len(grid[0])):
            for row_index, row in enumerate(grid):
                if row[col] == ".":
                    result.append(row_index - 1)
                    break
            else:
                result.append(len(grid))
        return result

    locks = []
    keys = []

    for grid in grids:
        if all(char == "#" for char in grid[0]):
            result = compute_grid(grid)
            locks.append(result)
        else:
            row_height = len(grid) - 1
            result = compute_grid(transpose_horizontal(grid))
            keys.append(result)

    return locks, keys


def does_not_overlap(B, A, pins: int = 6) -> bool:
    """ """
    if len(A) != len(B):
        return False
    return all(pins - a > b for a, b in zip(A, B))


def parse_file(filename: str) -> list[list[str]]:
    grids = []
    with open(filename, "r") as file:
        new_grid = []
        for line in file.readlines():
            if line.strip() == "":
                grids.append(new_grid)
                new_grid = []
            else:
                new_grid.append(line.strip())

        if len(new_grid) > 0:
            grids.append(new_grid)

    return grids


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """https://adventofcode.com/2024/day/25"""

    args = parse_args(argv)
    grids = parse_file(args.file)
    locks, keys = process_grids(grids)
    fitting_pairs = 0
    for lock in locks:
        fitting_pairs += sum([1 for key in keys if does_not_overlap(key, lock)])
    print(f"Part 1: {fitting_pairs}")


if __name__ == "__main__":
    main(sys.argv[1:])
