from itertools import count


def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, 'r') as file:
        # read and yield the content of the file line by line
        for line in file:
            yield line.strip()

def calculate_new_ranges(ranges, new_range):
    parts = new_range.split("-")
    start = min(int(parts[0]), int(parts[1]))
    end = max(int(parts[0]), int(parts[1]))
    for r in ranges:
        if (r[0] <= start <= r[1]) or (r[0] <= end <= r[1]):
            new_low = min(r[0], start)
            new_high = max(r[1], end)
            ranges.remove(r)
            return calculate_new_ranges(ranges, f"{new_low}-{new_high}")
        elif start < r[0] and end > r[1]:
            ranges.remove(r)
            return calculate_new_ranges(ranges, f"{start}-{end}")

    ranges.append([start, end])

    return ranges

def add_new_range(ranges, new_range):
    parts = new_range.split("-")
    start = int(parts[0])
    end = int(parts[1])
    ranges.append([start, end])
    return ranges

def is_fresh(ranges, id):
    for range in ranges:
        if id >= range[0] and id <= range[1]:
            return True
    return False

def run_ex(file):
    total = 0
    iterator = read_file(file)
    ranges = []
    for line in iterator:
        if line == "":
            break
        ranges = calculate_new_ranges(ranges, line)

    valid_id_counter = 0

    ranges.sort()

    for r in ranges:
        print(f"{str(r[1])} - {r[0]} + 1. {r[1] - r[0] + 1}")
        valid_id_counter += (r[1] - r[0] + 1)

    for line in iterator:
        if is_fresh(ranges, int(line)):
            total += 1

    print("Sum:", total)
    print("Count:", valid_id_counter)
    return total


if __name__ == '__main__':
    a = run_ex('ex5_1_input_example')
    if a == 3:
        print("Example test passed")
        run_ex('ex5_1_input')
