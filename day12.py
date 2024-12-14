import argparse
import networkx as nx
import sys
from collections.abc import Sequence
from typing import Optional


def get_sumproduct_area_and_perimeter(graph: nx.Graph) -> int:
    """Multiply area and perimeter for each island, and return the sum"""
    total_cost = 0
    for component in nx.connected_components(graph):
        subgraph = graph.subgraph(component)
        area = len(component)
        perimeter = sum([4 - degree for node, degree in subgraph.degree()])
        total_cost += area * perimeter
    return total_cost


def read_file_to_grid(filename: str) -> list[list[str]]:
    """Read the file into a 2D grid"""
    with open(filename, "r") as file:
        grid = [list(line.strip()) for line in file.readlines()]
    return grid


def create_graph_from_grid(grid) -> nx.Graph:
    """Create a graph from the grid"""
    G = nx.Graph()
    rows, cols = len(grid), len(grid[0])

    # Add edges for adjacent matching letters
    for r in range(rows):
        for c in range(cols):
            current_node = (r, c)
            G.add_node(current_node, letter=grid[r][c])

            # Check right
            if c + 1 < cols and grid[r][c] == grid[r][c + 1]:
                G.add_edge(current_node, (r, c + 1))

            # Check down
            if r + 1 < rows and grid[r][c] == grid[r + 1][c]:
                G.add_edge(current_node, (r + 1, c))

            # Check left
            if c - 1 >= 0 and grid[r][c] == grid[r][c - 1]:
                G.add_edge(current_node, (r, c - 1))

            # Check up
            if r - 1 >= 0 and grid[r][c] == grid[r - 1][c]:
                G.add_edge(current_node, (r - 1, c))

    return G


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/12
    """
    args = parse_args(argv)
    grid = read_file_to_grid(args.file)
    graph = create_graph_from_grid(grid)

    total_cost = get_sumproduct_area_and_perimeter(graph)
    print(f"Part 1: {total_cost}")


if __name__ == "__main__":
    main(sys.argv[1:])
