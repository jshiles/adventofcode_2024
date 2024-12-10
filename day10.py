import argparse
import sys
from collections.abc import Sequence
from typing import Optional
from enum import Enum
from dataclasses import dataclass
from collections import deque


@dataclass(frozen=True)
class Location:
    row: int
    col: int


def find_path(grid: list[list[int]], sp: Location, ep: Location) -> list[Location]:
    """
    BFS of the grid from this sp to this ep. Not efficient because it walks the grid
    for each pair rather than just each starting point.
    """
    rows, cols = len(grid), len(grid[0])

    start = (sp.row, sp.col)
    end = (ep.row, ep.col)

    # Directions for movement (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(*start, [])])
    visited = set()

    while queue:
        row, col, path = queue.popleft()

        # If we reach the target
        if (row, col) == end:
            return path + [Location(row, col)]

        # Mark the current cell as visited
        visited.add(Location(row, col))

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and Location(nr, nc) not in visited
                and (grid[nr][nc] - grid[row][col]) == 1
            ):
                queue.append((nr, nc, path + [Location(row, col)]))

    return []


def parse_input(path: str) -> list[list[int]]:
    nested_list = []
    with open(path, "r") as file:
        for line in file:
            numbers = list(line.strip())
            nested_list.append([int(num) for num in numbers])
    return nested_list


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/8
    """
    args = parse_args(argv)
    topological_map = parse_input(args.file)

    starting_points = [
        Location(row_idx, col_idx)
        for row_idx, row in enumerate(topological_map)
        for col_idx, val in enumerate(row)
        if val == 0
    ]
    ending_points = [
        Location(row_idx, col_idx)
        for row_idx, row in enumerate(topological_map)
        for col_idx, val in enumerate(row)
        if val == 9
    ]

    count = 0
    for sp in starting_points:
        for ep in ending_points:
            if len(find_path(topological_map, sp, ep)) > 0:
                count += 1
    print(f"Part 1: {count}")


if __name__ == "__main__":
    main(sys.argv[1:])
