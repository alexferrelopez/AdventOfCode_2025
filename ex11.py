from fileinput import lineno
from itertools import permutations, product

def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, 'r') as file:
        # read and yield the content of the file line by line
        for line in file:
            yield line

def dfs(graph, start, goal, unique_paths: set, path):
    queue = graph[start]

    for node in queue:
        if node == goal:
            unique_paths.add(",".join(path + [node]))
            continue

        dfs(graph, node, goal, unique_paths, path + [node])

    return unique_paths


def run_ex_1(file):
    lines = [[device[:3] for device in line.split(" ")] for line in read_file(file)]

    graph = {}

    for line in lines:
        graph[line[0]] = line[1:]

    unique_paths = dfs(graph, "svr", "out", set(), ["you"])

    filtered_paths = [path for path in unique_paths if "fft" in path and "dac" in path]

    print(filtered_paths)

    return len(filtered_paths)




if __name__ == '__main__':

    a = run_ex_1('ex11_1_input_example')
    if a == 7:
        print("Example test passed")

    run_ex_1('ex11_1_input')
    '''

    a = run_ex_2('ex10_1_input_example')
    if a == 33:
        print("Example test passed")

    run_ex_2('ex10_1_input')
    '''