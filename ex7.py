from copy import deepcopy


def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, 'r') as file:
        # read and yield the content of the file line by line
        for line in file:
            yield line


def surround_splitter(lines, row, col, side):
    if col > 0 and side == "left":
        lines[row][col - 1] = "|"
    elif col < len(lines[0]) - 1 and side == "right":
        lines[row][col + 1] = "|"

    return lines

def simulate_timeline_2(lines, row, start_col):
    col_freq = {start_col: 1}
    count = 1

    for i in range(row, len(lines)):
        this_round = deepcopy(col_freq)
        col_freq = {}
        for j, freq in this_round.items():
            if lines[i][j] == "^":
                col_freq[j-1] = col_freq.get(j-1, 0) + freq
                col_freq[j+1] = col_freq.get(j+1, 0) + freq

                count += freq

            elif lines[i][j] == ".":
                col_freq[j] = col_freq.get(j, 0) + freq

    return count


def simulate_timeline(lines, row, start_col):
    to_explore = [start_col]
    count = 1

    for i in range(row, len(lines)):
        this_round = to_explore.copy()
        to_explore = []

        for j in this_round:
            if lines[i][j] == "^":
                to_explore.append(j - 1)
                to_explore.append(j + 1)

                # test_count += v
                count += 1
                pass

            elif lines[i - 1][j] == ".":
                to_explore.append(j)


    return count


def run_ex(file):
    lines = [[c for c in line] for line in read_file(file)]

    start_index = lines[0].index('S')

    lines[1][start_index] = "|"
    # paths = simulate_timeline(lines, 2, start_index)

    paths2 = simulate_timeline_2(lines, 2, start_index)

    print(paths2)

    return paths2


def files_are_equal(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        return f1.read() == f2.read()


if __name__ == '__main__':
    a = run_ex('ex7_1_input_example')
    if a == 40:
        print("Example test passed")
        run_ex('ex7_1_input')
