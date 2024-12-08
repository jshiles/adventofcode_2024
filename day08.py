import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import combinations, chain
from math import sqrt
from typing import Optional


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Antenna:
    point: Point
    frequency: str


def find_antinodes(
    locations: list[Antenna], max_x: int, max_y: int, resonnance: bool = False
) -> set[Point]:
    """
    Find all antinodes locations, according the definition from list of Antenna locs.
    Return locations as a set[Point]
    """

    def compute_antinode(l1: Antenna, l2: Antenna) -> None:
        if l1.frequency == l2.frequency:
            newx = l2.point.x + (l2.point.x - l1.point.x)
            newy = l2.point.y + (l2.point.y - l1.point.y)
            count = 0
            while (
                newx >= 0
                and newx < max_x
                and newy >= 0
                and newy < max_y
                and (resonnance or count == 0)
            ):
                antinode_locations.add(Point(newx, newy))
                newx = newx + (l2.point.x - l1.point.x)
                newy = newy + (l2.point.y - l1.point.y)
                count += 1
            if resonnance:
                antinode_locations.add(l2.point)

    antinode_locations = set()
    for loc1, loc2 in combinations(locations, 2):
        compute_antinode(loc1, loc2)
        compute_antinode(loc2, loc1)

    return antinode_locations


def process_input(file_path: str) -> tuple[list[Antenna], int, int]:
    """Returns the list of Antennas and max cols and rows"""
    locations = []
    max_length = 0  # To track the maximum line length
    num_rows = 0  # To count the number of rows

    with open(file_path, "r") as file:
        for y, line in enumerate(file):  # y is the row index
            stripped_line = line.strip()
            max_length = max(max_length, len(stripped_line))  # Update max_length
            for x, char in enumerate(stripped_line):  # x is the column index
                if char != ".":  # Skip '.' characters
                    locations.append(Antenna(Point(x=x, y=y), frequency=char))
            num_rows += 1  # Increment row count

    return locations, max_length, num_rows


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/8
    """
    args = parse_args(argv)
    locations, max_x, max_y = process_input(args.file)

    num_antinodes = len(find_antinodes(locations, max_x, max_y))
    print(f"Part 1: {num_antinodes}")

    num_antinodes = len(find_antinodes(locations, max_x, max_y, True))
    print(f"Part 2: {num_antinodes}")


if __name__ == "__main__":
    main(sys.argv[1:])
