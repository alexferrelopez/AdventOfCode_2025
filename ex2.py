def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, 'r') as file:
        # read and yield the content of the file line by line
        for line in file:
            yield line.strip()


def divide_string(s, n):
    if len(s) % n != 0:
        return False, []

    part_length = len(s) // n

    parts = [s[i:i + part_length] for i in range(0, len(s), part_length)]

    return True, parts


def run_ex(file):
    sum = 0
    for line in read_file(file):
        id_ranges = line.split(",")
        for id_range in id_ranges:
            start, end = map(int, id_range.split("-"))
            for i in range(start, end + 1):
                value = str(i)
                for j in range(2, len(value)+1):
                    is_divisible, divisions = divide_string(value, j)
                    if is_divisible:
                        unique_parts = set(divisions)
                        if len(unique_parts) == 1:
                            sum += i
                            break

    print("Sum:", sum)


if __name__ == '__main__':
    # run_ex('ex2_1_input_example')
    run_ex('ex2_1_input')
