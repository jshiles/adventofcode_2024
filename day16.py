import argparse
import heapq
import sys
from collections.abc import Sequence
from typing import Optional
from collections import defaultdict


def find_all_paths(
    grid: list[list[str]], start: tuple[int, int], end: tuple[int, int], start_dir: str
) -> list:
    """
    Finds all possible paths and their costs from start to end inside of grid,
    with starting direction start_dir. Returns a list of dict with "cost" and
    "path", where path is a list of touched points.
    """

    directions = {"north": (-1, 0), "south": (1, 0), "east": (0, 1), "west": (0, -1)}

    def calculate_turn_cost(current_dir: str, new_dir: str) -> int:
        """Given current direction, return the cheapest cost to face new direction."""
        direction_order = ["north", "east", "south", "west"]
        current_index = direction_order.index(current_dir)
        new_index = direction_order.index(new_dir)
        diff = (new_index - current_index) % 4
        return min(diff, 4 - diff) * 1000

    def traverse() -> list:
        """
        'Walk' from start to end and record all possible paths.
        """
        pq = []  # Priority queue for BFS
        heapq.heappush(pq, (0, start[0], start[1], start_dir, [start]))

        # Instead of using visited as a pruning mechanism, we'll use it to prevent
        # infinite loops
        visited = defaultdict(lambda: float("inf"))
        all_paths = []

        while pq:
            cost, x, y, current_dir, path = heapq.heappop(pq)

            # If we reach the end, add this path to our solutions
            if (x, y) == end:
                all_paths.append(
                    {"cost": cost, "path": path + [end], "final_direction": current_dir}
                )
                continue

            # Only skip if we've seen this exact state with a better cost
            # We're more lenient here to allow multiple paths
            if visited[(x, y, current_dir)] <= cost - 2000:  # Allow some suboptimal paths
                continue

            visited[(x, y, current_dir)] = min(visited[(x, y, current_dir)], cost)

            for direction, (dx, dy) in directions.items():
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < len(grid)
                    and 0 <= ny < len(grid[0])
                    and grid[nx][ny] == "."
                    and (nx, ny) not in path
                ):  # Prevent cycles
                    turn_cost = calculate_turn_cost(current_dir, direction)
                    new_cost = cost + turn_cost + 1

                    heapq.heappush(pq, (new_cost, nx, ny, direction, path + [(nx, ny)]))

        return all_paths if all_paths else []

    return traverse()


def read_grid_from_file(
    file_path: str,
) -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
    """
    Read puzzel input and return the grid, and starting and ending locations
    """
    with open(file_path, "r") as file:
        grid = [list(line.strip()) for line in file.readlines()]
        s = e = (0, 0)
        for r_idx, row in enumerate(grid):
            for c_idx, v in enumerate(row):
                if v == "S":
                    s = (r_idx, c_idx)
                    grid[r_idx][c_idx] = "."
                elif v == "E":
                    e = (r_idx, c_idx)
                    grid[r_idx][c_idx] = "."

        return grid, s, e

    return [], (0, 0), (0, 0)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/16
    """
    args = parse_args(argv)
    grid, start, end = read_grid_from_file(args.file)
    paths = find_all_paths(grid, start, end, "east")
    min_cost = min(
        [p.get("cost", None) for p in paths if p.get("cost", None) is not None]
    )
    print(f"Part 1: {min_cost}")

    points = set()
    for d in paths:
        if d.get("cost", 0) == min_cost:
            points.update(d.get("path", []))
    print(f"Part 2: {len(points)}")


if __name__ == "__main__":
    main(sys.argv[1:])
