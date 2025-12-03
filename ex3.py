def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, 'r') as file:
        # read and yield the content of the file line by line
        for line in file:
            yield line.strip()


def find_max(arr):
    position = 0
    max_value = arr[position]
    for i, num in enumerate(arr):
        if num > max_value:
            max_value = num
            position = i

    return max_value, position


def find_max_value_in_str(arr, depth=12):
    if depth == 1:
        max_val, pos = find_max(arr)
        return str(max_val)
    else:
        sliced_arr = arr[:-(depth-1)]

        max_val, pos = find_max(sliced_arr)

        new_arr = arr[pos + 1:]
        res = str(max_val) + find_max_value_in_str(new_arr, depth - 1)
        return res


def run_ex(file):
    sum = 0
    for line in read_file(file):
        arr = list(map(int, line))
        res = find_max_value_in_str(arr)
        sum += int(res)

    print("Sum:", sum)
    return sum


if __name__ == '__main__':
    a = run_ex('ex3_1_input_example')
    if a == 3121910778619:
        print("Example test passed")
    run_ex('ex3_1_input')
