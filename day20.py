import networkx as nx


def parse_file(file_path: str) -> list[list[str]]:
    grid = []
    with open(file_path, "r") as file:
        for line in file.readlines():
            grid.append(list(line.strip()))
    return grid


def parse_grid_and_create_graph(
    grid: list[list[str]],
) -> tuple[nx.Graph, tuple[int, int], tuple[int, int]]:
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
    return abs(n1[0] - n2[0]) + abs(n1[1] - n2[1])


def find_cheats_that_save_x(
    graph: nx.Graph, start: tuple[int, int], end: tuple[int, int], x: int = 100
) -> tuple[int, int]:
    unaltered_shortest_path = nx.shortest_path_length(graph, start, end)

    max_savings = 0
    count_greater_than_x = 0
    for node1 in sorted(nx.descendants(graph, start) | {start}):
        for node2 in sorted(nx.descendants(graph, end) | {end}):
            distance_of_cheat = manh_dist(node1, node2)
            if 0 < distance_of_cheat <= 2:
                savings = unaltered_shortest_path - (
                    nx.shortest_path_length(graph, start, node1)
                    + distance_of_cheat
                    + nx.shortest_path_length(graph, node2, end)
                )
                max_savings = max(max_savings, savings)
                if savings >= x:
                    count_greater_than_x += 1

    return count_greater_than_x, max_savings


grid = parse_file("inputs/day20.txt")
graph, start, end = parse_grid_and_create_graph(grid)
print(find_cheats_that_save_x(graph, start, end, 100))
