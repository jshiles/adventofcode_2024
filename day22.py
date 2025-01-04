import argparse
import sys
from collections import Counter
from collections.abc import Sequence
from itertools import accumulate, chain, pairwise
from functools import reduce
import operator
from typing import Optional, Generator, Union, Iterable


def compute_next_secret(s: int) -> int:
    """Compute the next secet in the sequence given the input."""
    s = (s ^ (s * 64)) % 16777216
    s = (s ^ (s // 32)) % 16777216
    s = (s ^ (s * 2048)) % 16777216
    return s


def compute_xth_secrect(s: int, x: int) -> int:
    """Compute the xth secrets given the starting secret s"""
    return reduce(lambda acc, _: compute_next_secret(acc), range(x), s)


def compute_x_differences(s: int, x: int) -> tuple[list[int], list[int]]:
    """
    Compute prices and differnces for the first x generated numbers starting
    with secrets.
    """

    def price_differences(prices: Iterable[int]) -> Generator[int, None, None]:
        return (current - previous for previous, current in pairwise(prices))

    digits = accumulate([s] * x, lambda acc, _: compute_next_secret(acc))
    prices = list(map(lambda x: x % 10, digits))
    return prices, list(price_differences(prices))


def find_best_pattern(secrets: list[int]) -> int:
    """
    Find the pattern (4 price differences) that generates the higest sell prices
    across all monkeys. Each monkey will only buy the first occurrance of the
    pattern. Return the combined sell price of pattern.
    """
    best_patterns = {}

    for secret in secrets:
        # determine the local patterns maximiums.
        window = []
        patterns = dict()
        prices, differences = compute_x_differences(secret, 2000)
        for idx, number in enumerate(differences):
            window.append(number)
            if len(window) == 4:
                if patterns.get(tuple(window), None) is None:
                    patterns[tuple(window)] = prices[idx + 1]
                window.pop(0)

        # combine the two key patters into a global.
        for key in patterns.keys():
            best_patterns[key] = best_patterns.get(key, 0) + patterns.get(key, 0)

    return max(best_patterns.values())


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

    prices, differences = compute_x_differences(123, 10)
    assert prices == [3, 0, 6, 5, 4, 4, 6, 4, 4, 2]
    assert list(differences) == [-3, 6, -1, -1, 0, 2, -2, 0, -2]

    args = parse_args(argv)
    with open(args.file, "r") as file:
        numbers = [int(line.strip()) for line in file if line.strip().isdigit()]

        # Part 1
        part1 = sum([compute_xth_secrect(x, 2000) for x in numbers])
        print(f"Part 1: {part1}")

        # Part 2
        print(f"Part 2: {find_best_pattern(numbers)}")


if __name__ == "__main__":
    main(sys.argv[1:])
