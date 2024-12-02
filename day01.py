import argparse
import numpy as np
from collections import Counter
import sys
from collections.abc import Sequence
from typing import Optional


def sum_differences(left_l, right_l) -> int:
    """Return sum of abs diff of left_l and right_l"""
    return np.abs(np.sort(left_l) - np.sort(right_l)).sum()


def similarity(left_l, right_l) -> int:
    """Return sum of left_l times frequency in right_l"""
    frequency: Counter[int] = Counter(right_l.tolist())
    return np.array([num * frequency.get(num, 0) for num in left_l]).sum()


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        "-f",
        help="input file",
        required=True,
        type=str
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/1
    """
    args = parse_args(argv)
    data = np.loadtxt(args.file, dtype=int)
    left_l = data[:, 0]
    right_l = data[:, 1]
    print(f"Part 1: {sum_differences(left_l, right_l)}")
    print(f"Part 2: {similarity(left_l, right_l)}")


if __name__ == "__main__":
    main(sys.argv[1:])
