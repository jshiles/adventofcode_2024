import argparse
import sys
from collections.abc import Sequence
from typing import Optional
from dataclasses import dataclass
from functools import reduce
from operator import mul

from numpy.lib.function_base import average


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def get_quadrant(self, max_x: int, max_y: int) -> int | None:
        """
        Determine the quadrant of the position.

        Quadrant layout:
        1 | 2
        --+--
        3 | 4

        Returns:
        - 1 for upper right quadrant
        - 2 for upper left quadrant
        - 3 for lower left quadrant
        - 4 for lower right quadrant
        - None if on a border or middle row/column

        :return: Quadrant number or None
        """
        # Calculate quadrant midpoints
        mid_x = max_x // 2
        mid_y = max_y // 2

        # Check if on a border or middle row/column
        if (self.x == mid_x) or (self.y == mid_y):
            return None

        # Determine quadrant
        if self.x < mid_x:
            return 1 if self.y < mid_y else 3
        else:
            return 2 if self.y < mid_y else 4


@dataclass
class Robot:
    p: Position
    dx: int
    dy: int

    def move(self, max_x: int, max_y: int) -> None:
        """
        Move the position by adding velocity, with wrapping around the grid.
        :param max_x: boundary in x direction
        :param max_y: boundary in y direction
        """
        new_x = (self.p.x + self.dx) % max_x
        new_y = (self.p.y + self.dy) % max_y
        self.p = Position(new_x, new_y)


def print_robots(robots: list[Robot], max_x: int, max_y: int) -> None:
    """
    Print a grid representing occupied positions.

    Args:
    :param positions: List of Robots and their position objects with x and y attributes
    :param max_rows: Total number of rows in the grid
    :param max_cols: Total number of columns in the grid
    """
    # Create a 2D grid filled with '.'
    grid = [["." for _ in range(max_x)] for _ in range(max_y)]

    # Mark occupied positions with 'R'
    for robot in robots:
        # Check if position is within grid bounds
        if 0 <= robot.p.x < max_x and 0 <= robot.p.y < max_y:
            grid[robot.p.y][robot.p.x] = "R"

    # Print the grid
    for row in grid:
        print("".join(row))


def count_adjacent_positions(robots: list[Robot]):
    """
    Count the number of adjacent positions for each position in the list.
    Adjacent positions include: up, down, left, right, and diagonals.

    :param positions: List of Robots and their position objects with x and y attributes
    :return: dict mapping each position to its number of adjacent positions
    """
    # Create a set of position tuples for fast lookup
    positions = [robot.p for robot in robots]
    position_set = {(pos.x, pos.y) for pos in positions}

    # Directions for adjacent positions (including diagonals)
    directions = [
        (0, 1),  # up
        (0, -1),  # down
        (1, 0),  # right
        (-1, 0),  # left
        (1, 1),  # up-right diagonal
        (1, -1),  # down-right diagonal
        (-1, 1),  # up-left diagonal
        (-1, -1),  # down-left diagonal
    ]

    # Dictionary to store adjacent position counts
    adjacent_counts = {}

    for pos in positions:
        # Count adjacent positions
        adjacent_count = sum(
            1 for dx, dy in directions if (pos.x + dx, pos.y + dy) in position_set
        )

        adjacent_counts[(pos.x, pos.y)] = adjacent_count

    return adjacent_counts


def mean_adjacency(robots: list[Robot]) -> float:
    """
    Computes the average adjanct robots to each robot.

    :param positions: List of Robots and their position objects with x and y attributes
    :return: float
    """
    adjacent_positions = count_adjacent_positions(robots)
    return sum(adjacent_positions.values()) / len(adjacent_positions)


def parse_robots_from_file(filename: str) -> list[Robot]:
    """
    Parse positions from a file with format 'p=x,y v=vx,vy'.

    :param filename: Path to the input file
    :return: List of Robot objects
    """
    robots = []

    with open(filename, "r") as file:
        for line in file:
            # Remove whitespace and split the line
            line = line.strip()

            # Split position and velocity parts
            p_part, v_part = line.split(" ")

            # Extract x and y from position
            _, pos_coords = p_part.split("=")
            x, y = map(int, pos_coords.split(","))

            # Optional: Extract velocity (if you want to use it later)
            _, vel_coords = v_part.split("=")
            vx, vy = map(int, vel_coords.split(","))

            # Create Position object
            position = Robot(Position(x, y), vx, vy)
            robots.append(position)

    return robots


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    parser.add_argument(
        "--maxx", "-x", help="width of grid", required=True, type=int, default=11
    )
    parser.add_argument(
        "--maxy", "-y", help="height of grid", required=True, type=int, default=7
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/14
    """
    args = parse_args(argv)
    robots = parse_robots_from_file(args.file)

    # Part 1: python day14.py -f inputs/day14.txt -x 101 -y 103
    seconds = 100
    quadrants = {1: 0, 2: 0, 3: 0, 4: 0}
    [obj.move(args.maxx, args.maxy) for _ in range(seconds) for obj in robots]
    for obj in robots:
        quad = obj.p.get_quadrant(args.maxx, args.maxy)
        if quad is not None:
            quadrants[quad] += 1
    print(f"Part 1: {reduce(mul, [v for k, v in quadrants.items()])}")

    # Part 2: Print out possible versions when we have a suffienctly high
    # amount of adjacent robots.
    seconds = 100000
    for i in range(seconds):
        [obj.move(args.maxx, args.maxy) for obj in robots]
        mean_adjacent = mean_adjacency(robots)
        if mean_adjacent > 1.5:
            print(i + 1)
            # print_robots(robots, args.maxx, args.maxy)
            break


if __name__ == "__main__":
    main(sys.argv[1:])
