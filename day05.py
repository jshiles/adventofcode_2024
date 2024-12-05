import argparse
import sys
from collections.abc import Sequence
from typing import Optional


def validate(print_run: list[int], rules: dict[int, list[int]]) -> bool:
    """Validate the the printing logic is correct according the rules"""
    already_printed: dict = {}
    for page in print_run:
        ok = all([bool(already_printed.get(x, 1)) for x in rules.get(page, [])])
        if not ok:
            return False
        already_printed[page] = 0
    return True


def find_middle_num(print_run: list[int]) -> int:
    """Return the middle number of the array as an int"""
    middle_index = len(print_run) // 2
    if len(print_run) % 2 == 0:
        return (print_run[middle_index - 1] + print_run[middle_index]) // 2
    else:
        return print_run[middle_index]


def parse_input(file_path: str) -> tuple[dict[int, list[int]], list[list[int]]]:
    """Read in our grid from a file"""
    with open(file_path, "r") as file:
        content = file.read()
        part1, part2 = content.split("\n\n", 1)

    dict_data: dict[int, list[int]] = {}
    for line in part1.strip().split("\n"):
        key, value = line.split("|")
        key = int(key.strip())
        value = value.strip()
        if key not in dict_data:
            dict_data[key] = []
        dict_data[key].append(int(value))

    list_of_lists: list[list[int]] = [
        [int(num.strip()) for num in line.split(",")]
        for line in part2.strip().split("\n")
    ]

    return dict_data, list_of_lists


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/4
    """
    args = parse_args(argv)
    rules, print_order = parse_input(args.file)
    total = sum([find_middle_num(print_run) for print_run in print_order if validate(print_run, rules)])
    print(f"Part 1: {total}")


if __name__ == "__main__":
    main(sys.argv[1:])
