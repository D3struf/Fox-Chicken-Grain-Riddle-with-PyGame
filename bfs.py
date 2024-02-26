from collections import deque

def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        print("Queue: ", queue)
        current_node, path = queue.popleft()
        print("Current Node: ", current_node)
        print("Path: ", path)

        if current_node == goal:
            return path

        if current_node not in visited:
            visited.add(current_node)
            print('Visited: ', visited)
            neighbors = graph[current_node]
            print('Neighbors: ', neighbors)

            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    return None

# Example usage:
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'E', 'F'],
    'D': ['B', 'G'],
    'E': ['B', 'C', 'G'],
    'F': ['C'],
    'G': ['D', 'E', 'F']
}

start_node = 'A'
goal_node = 'D'

result_path = bfs(graph, start_node, goal_node)

if result_path:
    print(f"Path from {start_node} to {goal_node}: {result_path}")
else:
    print(f"No path found from {start_node} to {goal_node}")
