import argparse
import sys
from collections.abc import Sequence
from typing import Optional
from dataclasses import dataclass
import networkx as nx


@dataclass
class Point:
    x: int
    y: int


def create_grid_graph(maxx: int, maxy: int) -> nx.Graph:
    # Initialize an empty graph
    G = nx.Graph()

    # Add nodes and edges
    for x in range(maxx):
        for y in range(maxy):
            G.add_node((x, y))

            # Add edges to neighbors
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if 0 <= neighbor[0] < maxx and 0 <= neighbor[1] < maxy:
                    G.add_edge((x, y), neighbor)

    return G


def remove_blocked_nodes(graph: nx.Graph, blocked_points: list[Point]) -> None:
    # Convert blocked points to a set of tuples
    blocked_set = {(point.x, point.y) for point in blocked_points}
    graph.remove_nodes_from(blocked_set)


def parse_input(file_path: str) -> list[Point]:
    blocked_points: list[Point] = []

    with open(file_path, "r") as file:
        for line in file:
            x, y = line.strip().split(",")
            blocked_points.append(Point(int(x), int(y)))

    return blocked_points


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="input file", required=True, type=str)
    parser.add_argument("--maxx", type=int, default=71)
    parser.add_argument("--maxy", type=int, default=71)
    parser.add_argument("--bytes_fallen", type=int, default=1024)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    https://adventofcode.com/2024/day/18
    """
    args = parse_args(argv)
    graph = create_grid_graph(args.maxx, args.maxy)
    blocked_points = parse_input(args.file)

    remove_blocked_nodes(graph, blocked_points[: args.bytes_fallen])
    path_len = nx.shortest_path_length(graph, (0, 0), (args.maxx - 1, args.maxy - 1))
    print(f"Part 1: {path_len}")

    # remove one at a time, until we raise a no path exception.
    for point in blocked_points[args.bytes_fallen :]:
        remove_blocked_nodes(graph, [point])
        try:
            _ = nx.shortest_path_length(graph, (0, 0), (args.maxx - 1, args.maxy - 1))
        except nx.NetworkXNoPath:
            print(f"Part 2: {point}")
            break


if __name__ == "__main__":
    main(sys.argv[1:])
