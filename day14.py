import argparse
import sys
from collections.abc import Sequence
from typing import Optional
from dataclasses import dataclass
from functools import reduce
from operator import mul


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


def parse_robots_from_file(filename: str) -> list[Robot]:
    """
    Parse positions from a file with format 'p=x,y v=vx,vy'.

    :param filename: Path to the input file
    :param max_x: Maximum x coordinate for the grid
    :param max_y: Maximum y coordinate for the grid
    :return: List of Position objects
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

    # Part 1:
    #   python day14.py -f inputs/day14.txt -x 101 -y 103
    seconds = 100
    quadrants = {1: 0, 2: 0, 3: 0, 4: 0}
    [obj.move(args.maxx, args.maxy) for _ in range(seconds) for obj in robots]
    for obj in robots:
        quad = obj.p.get_quadrant(args.maxx, args.maxy)
        if quad is not None:
            quadrants[quad] += 1
    print(f"Part 1: {reduce(mul, [v for k, v in quadrants.items()])}")


if __name__ == "__main__":
    main(sys.argv[1:])
