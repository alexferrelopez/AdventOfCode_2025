def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, 'r') as file:
        # read and yield the content of the file line by line
        for line in file:
            yield line


def build_button_sequences(buttons: list, current_sequence: list, index, unique_sequences) -> set:
    if len(current_sequence) > 0:
        unique_sequences.add(",".join([str(i) for i in current_sequence]))

    for i in range(index, len(buttons)):
        sequence_copy = current_sequence.copy()
        sequence_copy.append(i)
        build_button_sequences(buttons, sequence_copy, i + 1, unique_sequences)

    return unique_sequences


def run_ex(file):
    lines = [line.split(" ") for line in read_file(file)]

    expected_combinations = [[a == "#" for a in line.pop(0)[1:-1]] for line in lines]

    joltage_requirements = [line.pop() for line in lines]

    for line in lines:
        for i, button in enumerate(line):
            line[i] = button[1:-1].split(",")

    total_min_presses = 0
    for i, buttons in enumerate(lines):
        min_presses = len(buttons)
        sequences = build_button_sequences(buttons, [], 0, set())
        expected_combination = expected_combinations[i]

        for seq in sequences:
            light_pattern = [False for _ in range(len(expected_combination))]
            buttons_pressed = [buttons[int(button_index)] for button_index in seq.split(",")]
            flattened_buttons = [item for sublist in buttons_pressed for item in sublist]

            for index in range(len(expected_combination)):
                index_count = flattened_buttons.count(str(index))
                if index_count % 2 == 1:
                    light_pattern[index] = True

            presses = len(seq.split(","))
            if light_pattern == expected_combination and presses < min_presses:
                min_presses = presses

        total_min_presses += min_presses

    print(total_min_presses)

    return total_min_presses


if __name__ == '__main__':
    a = run_ex('ex10_1_input_example')
    if a == 24:
        print("Example test passed")

    run_ex('ex10_1_input')
