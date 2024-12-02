import argparse
import sys
from collections.abc import Generator, Sequence
from typing import Optional


def walk_in_pairs(lst: list[int]) -> Generator[tuple[int, int]]:
    for i in range(len(lst) - 1):
        yield (lst[i], lst[i + 1])


def violation(x: int, y: int, ascending: bool) -> bool:
    return not (
        (ascending and x < y and y - x <= 3 and y - x >= 1)
        or (not ascending and x > y and x - y <= 3 and x - y >= 1)
    )


def is_safe(lst: list[int]) -> bool:
    """ """
    if len(lst) > 1:
        ascending = True if lst[0] < lst[1] else False
        for x, y in walk_in_pairs(lst):
            if violation(x, y, ascending):
                return False
    return True


def is_safe_dampner(lst: list[int]) -> bool:
    """ """
    if is_safe(lst):
        return True

    for i in range(len(lst)):
        test_list = lst[:i] + lst[i + 1 :]  # Remove the i-th number
        if is_safe(test_list):
            return True

    return False


def read_integer_rows(file_path: str) -> list[list[int]]:
    rows: list[list[int]] = []
    with open(file_path, "r") as file:
        for line in file:
            elements = line.strip().split()
            int_row = [int(el) for el in elements]
            rows.append(int_row)
    return rows


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/2
    """
    args = parse_args(argv)
    lists: list[list[int]] = read_integer_rows(args.file)

    num_safe: int = sum([1 if is_safe(lst) else 0 for lst in lists])
    print(f"Part 1 -> Num Safe: {num_safe}")

    num_safe2: int = sum([1 if is_safe_dampner(lst) else 0 for lst in lists])
    print(f"Part 2 -> Num Safe: {num_safe2}")


if __name__ == "__main__":
    main(sys.argv[1:])
