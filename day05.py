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


def insert_before(run: list[int], x: int, before: int) -> list[int]:
    """We insert all x's prior to 'before' and return the modified list"""
    y_index = run.index(before)
    x_values = [num for i, num in enumerate(run) if num == x and i > y_index]
    others = [num for i, num in enumerate(run) if num != x or i < y_index]
    new_y_index = others.index(before)
    result = others[:new_y_index] + x_values + others[new_y_index:]
    return result


def validate_and_fix(print_run: list[int], rules: dict[int, list[int]]) -> list[int]:
    """
    If the solution is not valid, we will recrusively shift the violations
    until we reach a valid print_run and then return that.
    """
    if validate(print_run, rules):
        return print_run

    inncorrect_run = print_run
    already_printed: dict = {}
    for page in inncorrect_run:
        violations = [x for x in rules.get(page, []) if already_printed.get(x, 0)]
        if len(violations):
            return validate_and_fix(
                insert_before(inncorrect_run, page, violations[0]), rules
            )
        already_printed[page] = 1

    return inncorrect_run


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
    total = sum([find_middle_num(pr) for pr in print_order if validate(pr, rules)])
    print(f"Part 1: {total}")
    total = sum(
        [
            find_middle_num(validate_and_fix(pr, rules))
            for pr in print_order
            if not validate(pr, rules)
        ]
    )
    print(f"Part 2: {total}")


if __name__ == "__main__":
    main(sys.argv[1:])
