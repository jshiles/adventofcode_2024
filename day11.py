import argparse
import sys
from collections.abc import Sequence
from typing import Optional
from functools import lru_cache


def stones_after_x_blinks(stones: list[int], x: int) -> int:
    @lru_cache(maxsize=None)
    def _recurse_blinks(stone: int, blinks_remaining: int) -> int:
        if blinks_remaining == 0:
            return 1

        if stone == 0:
            # If the stone is engraved with the number 0, it is replaced by
            # a stone engraved with the number 1.
            return _recurse_blinks(1, blinks_remaining - 1)
        elif len(str(stone)) % 2 == 0:
            # If the stone is engraved with a number that has an even
            # number of digits, it is replaced by two stones. The left half
            # of the digits are engraved on the new left stone, and the
            # right half of the digits are engraved on the new right stone.
            # (The new numbers don't keep extra leading zeroes: 1000 would
            # become stones 10 and 0.)
            num_str = str(stone)
            left = int(num_str[: len(num_str) // 2])
            right = int(num_str[len(num_str) // 2 :])
            return _recurse_blinks(left, blinks_remaining - 1) + _recurse_blinks(
                right, blinks_remaining - 1
            )
        else:
            # If none of the other rules apply, the stone is replaced by a
            # new stone; the old stone's number multiplied by 2024 is
            # engraved on the new stone.
            return _recurse_blinks(stone * 2024, blinks_remaining - 1)

    return sum([_recurse_blinks(stone, x) for stone in stones])


def parse_input(path: str) -> list[int]:
    with open(path, "r") as file:
        numbers = list(map(int, file.read().split()))
    return numbers


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/8
    """
    args = parse_args(argv)
    nums = parse_input(args.file)
    print(f"Part 1: {stones_after_x_blinks(nums, 25)}")
    print(f"Part 2: {stones_after_x_blinks(nums, 75)}")


if __name__ == "__main__":
    main(sys.argv[1:])
