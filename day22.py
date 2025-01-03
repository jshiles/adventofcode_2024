import argparse
import sys
from collections.abc import Sequence
from itertools import accumulate
from functools import reduce
from typing import Optional


def compute_next_secret(s: int) -> int:
    s = (s ^ (s * 64)) % 16777216
    s = (s ^ (s // 32)) % 16777216
    s = (s ^ (s * 2048)) % 16777216
    return s


def compute_xth_secrect(s: int, x: int) -> int:
    return reduce(lambda acc, _: compute_next_secret(acc), range(x), s)


def compute_x_prices(s: int, x: int) -> int:
    def add_last_digit(acc, num):
        return acc + (num % 10)

    digits = accumulate([s] * x, lambda acc, _: compute_next_secret(acc))
    return reduce(add_last_digit, digits, 0)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """https://adventofcode.com/2024/day/22"""

    assert compute_xth_secrect(1, 2000) == 8685429
    assert compute_xth_secrect(10, 2000) == 4700978
    assert compute_xth_secrect(100, 2000) == 15273692
    assert compute_xth_secrect(2024, 2000) == 8667524

    assert compute_x_prices(123, 10) == 38

    args = parse_args(argv)
    with open(args.file, "r") as file:
        numbers = [int(line.strip()) for line in file if line.strip().isdigit()]

        # Part 1
        # part1 = sum([compute_xth_secrect(x, 2000) for x in numbers])
        # print(f"Part 1: {part1}")


if __name__ == "__main__":
    main(sys.argv[1:])
