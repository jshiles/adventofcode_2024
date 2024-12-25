import argparse
import sys
from collections.abc import Sequence
from typing import Optional
from functools import lru_cache


@lru_cache
def is_possible(pattern: str, remaining_towels: frozenset[str]) -> bool:
    """Determine if pattern is possible at least one way."""
    if pattern in remaining_towels:
        return True

    success = False
    for towel in remaining_towels:
        if len(towel) <= len(pattern) and pattern.startswith(towel):
            success |= is_possible(pattern[len(towel) :], remaining_towels)
    return success


@lru_cache
def is_possible_xways(pattern: str, remaining_towels: frozenset[str]) -> int:
    """Count all possible ways to make the pattern"""
    if len(pattern) == 0:
        return 1

    success = 0
    for towel in remaining_towels:
        if len(towel) <= len(pattern) and pattern.startswith(towel):
            success += is_possible_xways(pattern[len(towel) :], remaining_towels)
    return success


def parse_input(file_path: str) -> tuple[frozenset[str], list[str]]:
    towels = []
    patterns = []

    with open(file_path, "r") as file:
        lines = file.readlines()

    if lines:
        towels = [item.strip() for item in lines[0].split(",")]
        patterns = [line.strip() for line in lines[1:] if line.strip()]

    return frozenset(towels), patterns


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/19
    """
    args = parse_args(argv)

    towels, desired_patterns = parse_input(args.file)
    sum_possible = sum(
        [1 for pattern in desired_patterns if is_possible(pattern, towels)]
    )
    print(f"Part 1: {sum_possible}")

    towels, desired_patterns = parse_input(args.file)
    sum_possible = sum(
        [is_possible_xways(pattern, towels) for pattern in desired_patterns]
    )
    print(f"Part 2: {sum_possible}")


if __name__ == "__main__":
    main(sys.argv[1:])
