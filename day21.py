import argparse
import networkx as nx
import re
import sys
from collections.abc import Sequence
from functools import cache
from itertools import product, combinations, chain
from typing import Optional


def grid_to_graph(grid: list[list[str]]) -> nx.Graph:
    """create a networkx graph from a grid"""
    G = nx.Graph()
    rows = len(grid)
    cols = len(grid[0])

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != "X":  # Skip "X"
                G.add_node((i, j), value=grid[i][j])
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] != "X":
                        G.add_edge((i, j), (ni, nj))

    return G


def get_node_by_value(graph, target_value):
    """Look up an node in the Graph by the readable value."""
    for node, data in graph.nodes(data=True):
        if data.get("value") == target_value:
            return node
    return None


def direction_symbol(p1: tuple[int, int], p2: tuple[int, int]) -> str:
    """
    Translates a sequency of (x, y) steps into numpad values. Returns that sequence
    as a string.
    """
    r1, c1 = p1  # Row and column of p1
    r2, c2 = p2  # Row and column of p2
    if r1 == r2 and c2 < c1:  # Same row, left
        return "<"
    elif r1 == r2 and c2 > c1:  # Same row, right
        return ">"
    elif c1 == c2 and r2 < r1:  # Same column, above
        return "^"
    elif c1 == c2 and r2 > r1:  # Same column, below
        return "v"
    else:
        raise ValueError("Not directly adjacent or invalid input")


def create_numpad_graph() -> nx.Graph:
    grid = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["X", "0", "A"]]
    return grid_to_graph(grid)


def create_arrows_graph() -> nx.Graph:
    grid = [["X", "^", "A"], ["<", "v", ">"]]
    return grid_to_graph(grid)


def shortest_pad_paths_from_a_b(a: str, b: str, padtype: str = "arrows") -> list[str]:
    """
    Returns the short paths from a to b in steps. pattype determins the graph we use.
    """
    graph = ARROWS_G if padtype == "arrows" else NUMPAD_G
    start_node = get_node_by_value(graph, a)
    end_node = get_node_by_value(graph, b)
    paths = []
    for path in nx.all_shortest_paths(graph, start_node, end_node):
        paths.append([direction_symbol(s, e) for s, e in zip(path, path[1:])])
    return ["".join(p) + "A" for p in paths]


def shortest_paths(code: str, padtype: str) -> list[str]:
    """
    Finds the shortest paths for a code. padtype determines which graph we are
    using. Returns all shortest paths.
    """
    parts = []
    curr = "A"
    for next in code:
        possible = shortest_pad_paths_from_a_b(curr, next, padtype)
        parts.append(possible)
        curr = next
    return ["".join(x) for x in product(*parts)]


def compute_shortest_seq_lenth(seq: str, depth: int = 2) -> int:
    """Function used in part 1 to find the shortest sequence of a sub sequence"""
    if depth == 1:
        return min([len(p) for p in shortest_paths(seq, "arrows")])

    next_robot = [
        compute_shortest_seq_lenth(p, depth - 1) for p in shortest_paths(seq, "arrows")
    ]
    return min([p for p in next_robot])


@cache
def compute_lengths(a: str, b: str, depth: int = 2) -> int:
    """
    Depth first search of optimal path from A to B in the directional arrow pad.
    Returns the shortest path for all robots.
    """
    if depth == 1:
        return min([len(p) for p in shortest_pad_paths_from_a_b(a, b)])

    optimal = sys.maxsize
    for robot_path in shortest_pad_paths_from_a_b(a, b):
        paths = [
            ((a, b), compute_lengths(a, b, depth - 1))
            for a, b in zip("A" + robot_path, robot_path)
        ]
        length = sum([p[1] for p in paths])
        optimal = min(optimal, length)

    return optimal


def solve(codes: list[str], n: int) -> int:
    """
    Finds the optimal path for 1 numpad robot + n-1 directional arrow + one
    more directional pad for the user. It does this for each code and returns
    the optimal steps times the numeric value of the code.
    """

    total = 0
    # Part 1
    # for code in codes:
    #     optimal = min([compute_shortest_seq_lenth(p, n) for p in shortest_paths(code, "numpad")])
    #     value = int("".join(re.findall(r"\d", code)))
    #     total += optimal * value

    # Part 2
    # Modified to walk pairwise (depth-first), caching these results which cuts
    # out a lot of computation.
    for code in codes:
        optimal = sys.maxsize
        for numpad_path in shortest_paths(code, "numpad"):
            paths = [
                ((a, b), compute_lengths(a, b, n))
                for a, b in zip("A" + numpad_path, numpad_path)
            ]
            length = sum([p[1] for p in paths])
            optimal = min(optimal, length)

        value = int("".join(re.findall(r"\d", code)))
        total += optimal * value

    return total


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/21
    """
    args = parse_args(argv)
    with open(args.file, "r") as file:
        codes = [line.strip() for line in file.readlines()]

    # optimal_slow = (
    #     min([compute_shortest_seq_lenth(p, 2) for p in shortest_paths("029A", "numpad")])
    #     * 29
    # )
    # optimal_fast = solve(["029A"], 2)
    # assert optimal_slow == optimal_fast

    print(f"Part 1: {solve(codes, 2)}")
    print(f"Part 2: {solve(codes, 25)}")


if __name__ == "__main__":
    NUMPAD_G = create_numpad_graph()
    ARROWS_G = create_arrows_graph()
    main(sys.argv[1:])
