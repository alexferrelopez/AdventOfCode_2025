from math import floor


def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, 'r') as file:
        # read and yield the content of the file line by line
        for line in file:
            yield line.strip()


def run_ex(file):
    gauge = 50
    i = 0

    for line in read_file(file):
        value = int(line[1:])
        is_right = line.startswith('R')
        prev_gauge = gauge

        if is_right:
            gauge = (gauge + value)
        else:
            gauge = (gauge - value)

        a = (prev_gauge * gauge)
        print(line + ":", prev_gauge, "->", gauge, ",", gauge % 100)
        if a < 0 or gauge == 0:
            i += 1
            print("\tCrossed zero:", prev_gauge, gauge)

        wrap_count = floor(abs(gauge) / 100)

        gauge = gauge % 100

        i += wrap_count
        if wrap_count > 0:
            print("\tWrapped:", wrap_count, "from", prev_gauge, "to", gauge)

    print(i, gauge)


if __name__ == '__main__':
    run_ex('ex1_1_input_example')
    run_ex('ex1_1_input')
