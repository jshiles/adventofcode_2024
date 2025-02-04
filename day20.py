import argparse
import networkx as nx
import sys
from collections.abc import Sequence
from typing import Optional


def parse_file(file_path: str) -> list[list[str]]:
    """Read the file into an nxm grid"""
    grid = []
    with open(file_path, "r") as file:
        for line in file.readlines():
            grid.append(list(line.strip()))
    return grid


def parse_grid_and_create_graph(
    grid: list[list[str]],
) -> tuple[nx.Graph, tuple[int, int], tuple[int, int]]:
    """
    converts a nxm grid into a network where '.' are the path, 'S' is the start,
    and 'E' is the end.
    :param grid: list[list[str]]
    :returns: nx.Graph (our graph), start and end as tuple[int, int]
    """
    start = end = (0, 0)
    graph = nx.Graph()
    rows, cols = len(grid), len(grid[0])

    # Replace 'S' and 'E' with '.' and record their positions
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
                grid[r][c] = "."
            elif grid[r][c] == "E":
                end = (r, c)
                grid[r][c] = "."

    # Helper function to get neighbors
    def get_neighbors(r, c):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == ".":
                yield (nr, nc)

    # Build the graph
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == ".":
                graph.add_node((r, c))
                for neighbor in get_neighbors(r, c):
                    graph.add_edge((r, c), neighbor)

    return graph, start, end


def manh_dist(n1: tuple[int, int], n2: tuple[int, int]) -> int:
    """computes the manhattan distance bwetween two points."""
    return abs(n1[0] - n2[0]) + abs(n1[1] - n2[1])


def find_cheats_that_save_x(
    graph: nx.Graph,
    start: tuple[int, int],
    end: tuple[int, int],
    x: int = 100,
    dist: int = 2,
) -> int:
    """
    Find the number of 'cheats' that save at least 100 steps.
    :param graph: nx.Graph
    :param start: tuple[int, int] starting node
    :param end: tuple[int, int] ending node
    :param x: int the minimum amount of savings required to be counted
    :returns: tuple[int, int] with number of 'cheats' that save x and max savings.
    """
    unaltered_shortest_path = nx.shortest_path_length(graph, start, end)

    computed = {}
    count_greater_than_x = 0
    for node1 in sorted(nx.descendants(graph, start) | {start}):
        for node2 in sorted(nx.descendants(graph, end) | {end}):
            distance_of_cheat = manh_dist(node1, node2)
            if (
                0 < distance_of_cheat <= dist
                and computed.get(frozenset([node1, node2]), None) is None
            ):
                savings = unaltered_shortest_path - (
                    nx.shortest_path_length(graph, start, node1)
                    + distance_of_cheat
                    + nx.shortest_path_length(graph, node2, end)
                )
                computed[frozenset([node1, node2])] = savings
                if savings >= x:
                    count_greater_than_x += 1

    return count_greater_than_x


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/20
    """
    args = parse_args(argv)
    grid = parse_file(args.file)
    graph, start, end = parse_grid_and_create_graph(grid)
    # effective_cheats = find_cheats_that_save_x(graph, start, end, 100)
    # print(f"Part 1: {effective_cheats}")

    effective_cheats = find_cheats_that_save_x(graph, start, end, 100, 20)
    print(f"Part 2: {effective_cheats}")


if __name__ == "__main__":
    main(sys.argv[1:])
