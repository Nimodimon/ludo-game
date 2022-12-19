import time

def print_log(message: str):
    print(message)
    time.sleep(1.5)

def print_matrix(matrix, field_size):
    numbers_list = [str(i % 10) for i in range(field_size)]

    horizontal_numbers = " " + get_spaced_row([""] + numbers_list)
    rows = [get_spaced_row([numbers_list[ind]] + row) for ind, row in enumerate(matrix)]

    print("\n".join([horizontal_numbers] + rows))

def set_matrix(field_size: int):
    half = int((field_size - 1) / 2)

    matrix = [symmetry_row(" " * (half - 1) + "*", "*")]

    for i in range(half - 2):
        matrix.append(symmetry_row(" " * (half - 1) + "*", "D"))

    matrix.append(symmetry_row("*" * half, "D"))

    matrix.append(symmetry_row("*" + "D" * (half - 1), "X"))

    matrix.extend([list(i) for i in matrix][-2::-1])

    return matrix

def get_spaced_row(row) -> str:
    return (" " * 2).join(row)

def symmetry_row(string_val: str, medium_char: str):
    return list(string_val + medium_char + string_val[::-1])

def set_size() -> int:
    while True:
        size = input("Enter field size: ")
        correct_size, err = size_is_correct(size)

        if correct_size:
            return int(size)

        if err == "not_int":
            print("Field size must be int!")
            time.sleep(1)
        elif err == "too_many":
            print("Sorry, it`s too many for me")
            time.sleep(1)
        elif err == "val_props":
            print("Field size must be uncountable and more than 5")
            time.sleep(2)

def size_is_correct(size: str) -> (bool, str):
    if not size.isdigit():
        return False, "not_int"

    elif int(size) > 21:
        return False, "too_many"

    elif int(size) < 5 or int(size) % 2 == 0:
        return False, "val_props"

    return True, ""
