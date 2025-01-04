import argparse
import sys
from collections.abc import Sequence
from typing import Optional
from itertools import combinations


def find_triplets_containing_t_node(graph: dict) -> list[tuple[str, str, str]]:
    """Find all triplets that have one node that starts with 't'"""
    triplets = set()
    for node in graph:
        neighbors = graph[node]
        # Check all combinations of two neighbors
        for n1, n2 in combinations(neighbors, 2):
            if n1 in graph[n2]:  # Check if n1 and n2 are connected
                triplet = tuple(sorted([node, n1, n2]))
                triplets.add(triplet)

    return [
        triplet for triplet in triplets if any(node.startswith("t") for node in triplet)
    ]


def find_largest_neighborhood(graph: dict) -> list[str]:
    """Find the largest neighborhood and return nodes as a list."""

    def connected_nodes(node, required):
        key = tuple(sorted(required))
        if key in neighborhoods:
            return

        neighborhoods.add(key)
        for neighbor in graph:
            if neighbor in required or not all(neighbor in graph[n] for n in required):
                continue
            connected_nodes(neighbor, {*required, neighbor})

    neighborhoods = set()
    for node in graph:
        connected_nodes(node, {node})

    return sorted(max(neighborhoods, key=len))


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """https://adventofcode.com/2024/day/23"""

    args = parse_args(argv)
    edges = []
    with open(args.file, "r") as file:
        edges = [edge.strip() for edge in file.readlines()]

    # Parse edges into an adjacency list
    graph = {}
    for edge in edges:
        node1, node2 = edge.split("-")
        graph.setdefault(node1, set()).add(node2)
        graph.setdefault(node2, set()).add(node1)

    print(f"Part 1: {len(find_triplets_containing_t_node(graph))}")

    lg_neighborhood = find_largest_neighborhood(graph)
    print(f"Part 2: {','.join(lg_neighborhood)}")


if __name__ == "__main__":
    main(sys.argv[1:])
