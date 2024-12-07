import argparse
import sys
from collections.abc import Sequence
from typing import Optional


def is_possible(target: int, input: list[int]) -> bool:
    """
    compute all possible outcomes with + x operators from left to right.
    """
    prev_vals = [input[0]]
    for x in input[1:]:
        new_prev_vals = []
        for y in prev_vals:
            new_prev_vals.append(x + y)
            new_prev_vals.append(x * y)
        prev_vals = new_prev_vals
    return target in prev_vals


def process_input(file_path: str) -> list[tuple[int, list[int]]]:
    """
    Read the grid from the file into a list of lists, and find the starting
    point. Return them as tuple.
    """
    data_list = []

    with open(file_path, 'r') as file:
        for line in file:
            target, numbers = line.split(':')  # Split the target and the series
            target = int(target.strip())  # Convert target to an integer
            number_list = list(map(int, numbers.strip().split()))  # Convert numbers to a list of integers
            data_list.append((target, number_list))  # Append as a tuple

    return data_list


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/6
    """
    args = parse_args(argv)
    equations = process_input(args.file)
    calibration_result = sum([target for target, nums in equations if is_possible(target, nums)])
    print(f"Part 1: {calibration_result}")


if __name__ == "__main__":
    main(sys.argv[1:])
