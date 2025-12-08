from itertools import count


def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, 'r') as file:
        # read and yield the content of the file line by line
        for line in file:
            yield line

def reparse_column_values(lines, col):
    initial_values = [lines[row][col] for row in range(len(lines)-1)]
    result = []

    for i in range(len(initial_values[0])):
        val = ""
        for j in range(len(initial_values)):
            val += initial_values[j][i]
        result.append(val)

    return result

def split_lines(lines):
    last_line = lines.pop()
    result = [[] for _ in range(len(lines))]
    last_index = 0
    for i, char in enumerate(last_line):
        if (char == "*" or char == "+") and i > 0:
            example = last_line[last_index:i]
            for j in range(len(lines)):
                result[j].append(lines[j][last_index:i-1])
            print(example)
            last_index = i

    for j in range(len(lines)):
        result[j].append(lines[j][last_index:-1])

    last_line = last_line.split()
    result.append([a.strip() for a in last_line])

    return result

def run_ex(file):
    total = 0
    lines = [line for line in read_file(file)]

    lines = split_lines(lines)

    for col in range(len(lines[0])):
        values = reparse_column_values(lines, col)
        if lines[-1][col] == "*":
            partial_result = 1

            for value in values:
                partial_result *= int(value)
            total += partial_result

        else:
            partial_result = 0
            for value in values:
                partial_result += int(value)
            total += partial_result

    print("Sum:", total)
    return total


if __name__ == '__main__':
    a = run_ex('ex6_1_input_example')
    if a == 3263827:
        print("Example test passed")
        run_ex('ex6_1_input')
