import argparse
import sys
from collections.abc import Sequence
from typing import Optional
from functools import partial
from itertools import product


def all_possible(input: list[int], combine: bool = False) -> list[int]:
    """
    Computes all possible outcomes using three operators: "+", "*", and optionally
    "||" in a left to right computation. Returns those possibilities in a list.
    """
    combine_fn = lambda x, y: x * 10 ** len(str(y)) + y
    prev_vals = [input[0]]
    for x in input[1:]:
        new_prev_vals = []
        for y in prev_vals:
            new_prev_vals.append(x + y)
            new_prev_vals.append(x * y)
            if combine:
                new_prev_vals.append(combine_fn(y, x))
        prev_vals = new_prev_vals
    return prev_vals


def is_possible(target: int, input: list[int]) -> bool:
    """
    compute all possible outcomes with "+" and "*" operators from left to
    right. Returns True if target is in the possible outcomes.
    """
    return target in all_possible(input)


def is_possible_concatenation(target: int, input: list[int]) -> bool:
    """
    compute all possible outcomes with "+", "*", and "||" operators from left
    to right. Returns True if target is in the possible outcomes.
    """
    return target in all_possible(input) or target in all_possible(input, True)


def process_input(file_path: str) -> list[tuple[int, list[int]]]:
    """
    Read the grid from the file into a list of lists, and find the starting
    point. Return them as tuple.
    """
    data_list = []

    with open(file_path, "r") as file:
        for line in file:
            target, numbers = line.split(":")
            target = int(target.strip())
            number_list = list(map(int, numbers.strip().split()))
            data_list.append((target, number_list))

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
    calibration_result = sum(
        [target for target, nums in equations if is_possible(target, nums)]
    )
    print(f"Part 1: {calibration_result}")

    calibration_result = sum(
        [
            target
            for target, nums in equations
            if is_possible_concatenation(target, nums)
        ]
    )
    print(f"Part 2: {calibration_result}")


if __name__ == "__main__":
    main(sys.argv[1:])
