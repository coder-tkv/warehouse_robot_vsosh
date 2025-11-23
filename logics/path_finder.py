from logics.config import *
import heapq


def dijkstra(graph, start, goal):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)

        if node in visited:
            continue

        visited.add(node)
        path = path + [node]

        if node == goal:
            return path, cost

        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))

    return None, None



def get_matrix(tiles):
    def in_bounds(x, y):
        return 0 <= x < list_width and 0 <= y < list_height

    matrix = {}
    for y in range(list_height):
        for x in range(list_width):
            c = y * list_width + x
            to_append = {}
            tile = tiles[y][x]

            neighbors = {
                'right': (x + 1, y, 1),
                'left':  (x - 1, y, -1),
                'down':  (x, y + 1, list_width),
                'up':    (x, y - 1, -list_width),
            }

            if tile == FLOOR:
                for direction, (nx, ny, delta) in neighbors.items():
                    if in_bounds(nx, ny):
                        neighbor = tiles[ny][nx]
                        if neighbor == FLOOR:
                            to_append[c + delta] = 1


            matrix[c] = to_append
    return matrix
