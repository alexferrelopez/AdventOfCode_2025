from itertools import permutations, product

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds



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


def run_ex_1(file):
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


def is_valid_remaining(remaining_contribution, joltage):
    if remaining_contribution < 0 or (joltage == remaining_contribution and joltage > 0):
        return False
    else:
        return True


def is_valid_contribution(contribution, joltage):
    if contribution > joltage or (contribution == 0 and joltage > 0):
        return False
    else:
        return True


def calculate_remaining_contributions(buttons, joltage_requirement):
    remaining_contributions = [0 for _ in range(len(joltage_requirement))]
    # contributions = [0 for _ in range(len(joltage_requirement))]
    flattened_buttons = flatten_two_dim_list(buttons)
    # skip_sequence = False
    for index in range(len(joltage_requirement)):
        index_count = flattened_buttons.count(str(index))
        remaining_contributions[index] = joltage_requirement[index] - index_count
        # contributions[index] = index_count

    return remaining_contributions


def is_valid_button_sequence(buttons, joltage_requirement):
    flattened_buttons = flatten_two_dim_list(buttons)
    is_valid = True

    for index in range(len(joltage_requirement)):
        index_count = flattened_buttons.count(str(index))
        value = joltage_requirement[index] - index_count
        is_valid &= is_valid_remaining(value, joltage_requirement[index])

        if not is_valid:
            break

    return is_valid


def flatten_two_dim_list(two_dim_list: list[list[str]]):
    return [item for sublist in two_dim_list for item in sublist]


def calculate_contributions(button, length):
    contributions = [0 for _ in range(length)]
    for index in range(length):
        index_count = button.count(str(index))
        contributions[index] = index_count

    return contributions


def all_sorted_tie_permutations(rows, key):
    rows_sorted = sorted(rows, key=key, reverse=True)

    # group consecutive ties
    groups = []
    cur = [rows_sorted[0]]
    cur_k = key(rows_sorted[0])

    for r in rows_sorted[1:]:
        k = key(r)
        if k == cur_k:
            cur.append(r)
        else:
            groups.append(cur)
            cur = [r]
            cur_k = k
    groups.append(cur)

    # permutations within each tie group, then cartesian product across groups
    per_group = [permutations(g) for g in groups]
    for choice in product(*per_group):
        yield [row for group_perm in choice for row in group_perm]

def build_linear_system(results, var_equation_indices, *, count_duplicates=True, dtype=float):

    m = len(results)
    n = len(var_equation_indices)

    A = np.zeros((m, n), dtype=dtype)
    b = np.array(results, dtype=dtype)

    for var_j, eq_list in enumerate(var_equation_indices):
        for eq_i in eq_list:
            eq_i = int(eq_i)
            if not (0 <= eq_i < m):
                raise IndexError(f"Equation index {eq_i} out of range [0, {m-1}]")
            if count_duplicates:
                A[eq_i, var_j] += 1
            else:
                A[eq_i, var_j] = 1

    return A, b

def solve_min_sum_nonnegative_integers(A, b):
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)

    m, n = A.shape

    # Objective: min sum(x)
    c = np.ones(n, dtype=float)

    # Equality constraints: A x = b
    constraints = LinearConstraint(A, lb=b, ub=b)

    # Bounds: x >= 0
    bounds = Bounds(lb=np.zeros(n), ub=np.full(n, np.inf))

    # Integrality: 1 => integer for each variable
    integrality = np.ones(n, dtype=int)

    res = milp(
        c=c,
        constraints=constraints,
        integrality=integrality,
        bounds=bounds,
    )

    if not res.success:
        raise ValueError(f"ILP failed: {res.message}")

    # Round defensively (solvers can return near-integers as floats)
    x = np.rint(res.x).astype(int)
    return x

def method_2_solver(joltage_requirements, lines):
    total_min_presses = 0
    count = 0
    for buttons, joltage_requirement in zip(lines, joltage_requirements):

        A, b = build_linear_system(joltage_requirement, buttons)
        x = solve_min_sum_nonnegative_integers(A, b)

        total_min_presses += np.sum(x)

    return count, total_min_presses


def run_ex_2(file):
    lines = [line.split(" ") for line in read_file(file)]

    [line.pop(0) for line in lines]

    joltage_requirements = [[int(counter) for counter in line.pop().strip()[1:-1].split(",")] for line in lines]

    lines = [[button[1:-1].split(",") for button in line] for line in lines]

    # count, total_min_presses = method_1_solver(joltage_requirements, lines)
    count, total_min_presses = method_2_solver(joltage_requirements, lines)

    print("Invalid button sequences: " + str(count) + "/" + str(len(lines)))
    print(total_min_presses)

    return total_min_presses


def method_1_solver(joltage_requirements: list[list[int]], lines: list[list[list[str]]]):
    total_min_presses = 0
    count = 0
    for buttons, joltage_requirement in zip(lines, joltage_requirements):
        is_solvable, total_min_presses = bruteforce_search(buttons, joltage_requirement)
        if not is_solvable:
            count += 1
    return count, total_min_presses


def bruteforce_search(buttons: list[list[str]], joltage_requirement: list[int]):
    min_presses = float('inf')
    results = {}
    sequences = build_button_sequences(buttons, [], 0, set())

    for seq_i, seq in enumerate(sequences):
        buttons_pressed = [buttons[int(button_index)] for button_index in seq.split(",")]

        prov_jolt_requirement = joltage_requirement.copy()

        buttons_pressed.sort(key=lambda x: min([joltage_requirement[int(index)] for index in x]) / len(x))

        presses = 0
        record = {}
        while len(buttons_pressed) > 0:
            button_pressed = buttons_pressed.pop(0)

            remaining_contributions = calculate_remaining_contributions(buttons_pressed,
                                                                        prov_jolt_requirement)

            buttons_pressed.sort(key=lambda x: min([remaining_contributions[int(index)] for index in x]) / len(x))

            min_quotient = min([remaining_contributions[int(index)] for index in button_pressed])

            for index in button_pressed:
                prov_jolt_requirement[int(index)] -= min_quotient
                record[",".join(button_pressed)] = min_quotient

            presses += min_quotient

            if all(l == 0 for l in prov_jolt_requirement):
                if presses < min_presses:
                    min_presses = presses
                    results[presses] = {seq_i: record}
            elif any(l < 0 for l in prov_jolt_requirement):
                break

    if min_presses != float('inf'):
        print(f"Found valid button sequence with {min_presses} presses")
        return True, min_presses
    else:
        print("No valid button sequence found")
        return False, min_presses


if __name__ == '__main__':
    '''
    a = run_ex_1('ex10_1_input_example')
    if a == 7:
        print("Example test passed")

    run_ex_1('ex10_1_input')
    '''

    a = run_ex_2('ex10_1_input_example')
    if a == 33:
        print("Example test passed")

    run_ex_2('ex10_1_input')
