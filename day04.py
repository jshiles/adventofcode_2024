import argparse
import sys
from collections.abc import Sequence
from typing import Generator, Optional, Any

def directions() -> Generator[tuple[int, int], Any, None]:
    """return all directions"""
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if not (x == 0 and y == 0):
                yield (x, y)


def count_word_occurrences(grid, word) -> int:
    """
    Search grid for the number of occurrences of word. Diagonal, Hoirzonatal,
    Vertical, and reverse are allowed.
    """
    rows, cols = len(grid), len(grid[0])
    word_len = len(word)

    def is_valid(x, y):
        """Check if the coordinates are within grid boundaries."""
        return 0 <= x < rows and 0 <= y < cols

    def search_from(x, y, index, dx, dy):
        """Recursively search for the word in the given direction."""
        if index == word_len:
            return 1
        nx, ny = x + dx, y + dy
        if not is_valid(nx, ny) or grid[nx][ny] != word[index]:
            return 0
        return search_from(nx, ny, index + 1, dx, dy)

    def search(x, y):
        """Search for the word starting at grid[x][y] in all directions."""
        count = 0
        if grid[x][y] == word[0]:
            for dx, dy in directions():
                count += search_from(x, y, 1, dx, dy)
        return count

    total_count = 0
    for x in range(rows):
        for y in range(cols):
            total_count += search(x, y)

    return total_count


def read_grid(file_path: str) -> list[list[str]]:
    """Read in our grid from a file"""
    with open(file_path, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/3
    """
    args = parse_args(argv)
    grid = read_grid(args.file)
    word = "XMAS"
    print(f"Part 1: {count_word_occurrences(grid, word)}")


if __name__ == "__main__":
    main(sys.argv[1:])
