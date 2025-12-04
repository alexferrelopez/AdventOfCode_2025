from itertools import count


def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, 'r') as file:
        # read and yield the content of the file line by line
        for line in file:
            yield line.strip()

def get_surround(matrix, target_col, target_row):
    surround = []

    for col in range(-1,2):
        for row in range(-1,2):
            current_col = col + target_col
            current_row = row + target_row
            if len(matrix) > current_col >= 0 and len(matrix[0]) > current_row >= 0:
                val = matrix[col + target_col][row + target_row]
                surround.append(val)

    return surround

def run_ex(file):
    grid = []
    total_sum = 0
    for line in read_file(file):
        line = line.strip()
        a = list(line)
        grid.append(a)
        print(a)

    while True:
        current_sum = 0
        for col, line in enumerate(grid):
            for row, cell in enumerate(line):
                if cell == '@':
                    surround = get_surround(grid, col, row)
                    if surround.count('@') - 1 < 4:
                        current_sum += 1
                        grid[col][row] = '.'
        if current_sum == 0:
            break
        total_sum += current_sum

    print("Sum:", total_sum)
    return total_sum


if __name__ == '__main__':
    a = run_ex('ex4_1_input_example')
    if a == 43:
        print("Example test passed")
        run_ex('ex4_1_input')
