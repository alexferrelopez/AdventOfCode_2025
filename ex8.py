import math


def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, 'r') as file:
        # read and yield the content of the file line by line
        for line in file:
            yield line


class Edge():
    def __init__(self, points, index1, index2):
        self.point1 = index1
        self.point1_ref = points[index1]
        self.point2 = index2
        self.point2_ref = points[index2]
        self.distance = points[index1].calculate_distance(points[index2])


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.adjacencies = []

    def calculate_distance(self, point):
        return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2)

    def add_adjacent(self, adjacency):
        self.adjacencies.append(adjacency)


def is_cyclic(node, visited, parent):
    pass

def dfs(node, visited, points):
    visited[node] = True
    adjacencies = points[node].adjacencies
    processes_nodes = [node]
    for adjacency in adjacencies:
        if not visited[adjacency]:
            new_processed_nodes = dfs(adjacency, visited, points)
            processes_nodes.extend(new_processed_nodes)

    return processes_nodes

def run_ex(file):
    lines = [line.split(",") for line in read_file(file)]
    points = []
    edges = []

    for line in lines:
        points.append(Point(int(line[0]), int(line[1]), int(line[2])))

    count = 0

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            edge = Edge(points, i, j)
            edges.append(edge)
            count += 1

    # get 10 smallest edges
    sorted_edges = sorted(edges, key=lambda x: x.distance)

    visited = [False] * len(points)

    final_edge = None
    for edge in sorted_edges:
        current_nodes = dfs(edge.point1, visited, points)
        if edge.point2 not in current_nodes:
            points[edge.point1].add_adjacent(edge.point2)
            points[edge.point2].add_adjacent(edge.point1)
            visited[edge.point1] = True
            visited[edge.point2] = True
            if len(dfs(edge.point1, [False]*len(points),points)) == len(points):
                final_edge = edge
                break

    result = final_edge.point1_ref.x * final_edge.point2_ref.x

    print(result)

    return result


def files_are_equal(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        return f1.read() == f2.read()


if __name__ == '__main__':
    a = run_ex('ex8_1_input_example')
    if a == 40:
        print("Example test passed")
    run_ex('ex8_1_input')

