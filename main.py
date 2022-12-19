import random
from terminal_utils import set_matrix, set_size, print_matrix, print_log

field_size = set_size()
matrix = set_matrix(field_size)

ap_active_pawns = []
ap_blocked_cells = []
ap_pawns_in_house = int((field_size - 3) / 2)
ap_name = "a"

pp_active_pawns = []
pp_blocked_cells = []
pp_pawns_in_house = int((field_size - 3) / 2)
pp_name = "b"

# ap - active player, pp - passive player
def change_turn():
    global ap_active_pawns, ap_blocked_cells, ap_pawns_in_house, ap_name
    global pp_active_pawns, pp_blocked_cells, pp_pawns_in_house, pp_name

    ap_active_pawns, pp_active_pawns = pp_active_pawns, ap_active_pawns
    ap_blocked_cells, pp_blocked_cells = pp_blocked_cells, ap_blocked_cells
    ap_pawns_in_house, pp_pawns_in_house = pp_pawns_in_house, ap_pawns_in_house
    ap_name, pp_name = pp_name, ap_name

def start_turn():
    while True:
        a_cube = int(random.random() * 6 + 1)
        b_cube = int(random.random() * 6 + 1)

        if a_cube > b_cube:
            return print_field("A moves first")
        elif a_cube < b_cube:
            change_turn()
            return print_field("B moves first")

def print_field(message: str = None):
    field = [list(row) for row in matrix]

    for pawn in ap_active_pawns:
        field[pawn[0]][pawn[1]] = ap_name.upper()

    for pawn in pp_active_pawns:
        field[pawn[0]][pawn[1]] = pp_name.upper()

    print_matrix(field, field_size)

    if message:
        print_log(message)

def set_start_limit():
    global a_blocked_cells, b_blocked_cells

    medium = int((field_size - 1) / 2)

    if ap_name == "a":
        ap_blocked_cells.append((medium + 1, medium))
        pp_blocked_cells.append((medium - 1, medium))
    else:
        ap_blocked_cells.append((medium - 1, medium))
        pp_blocked_cells.append((medium + 1, medium))

def add_pawn():
    global ap_pawns_in_house, ap_active_pawns
    medium = int((field_size - 1) / 2)

    if ap_name == "a":
        ap_active_pawns.append((0, medium + 1))
    elif ap_name == "b":
        ap_active_pawns.append((field_size - 1, medium - 1))

    ap_pawns_in_house -= 1

# Remove by index
def remove_pawn(index: int):
    global ap_active_pawns
    ap_active_pawns.pop(index)

def move_pawn_to_home(index: int):
    global pp_pawns_in_house, pp_active_pawns

    pp_active_pawns.pop(index)
    pp_pawns_in_house += 1

# Move
def move_pawn(moves: int, blocked_cells: list[(int, int)]) -> bool:
    global ap_active_pawns

    medium = int((field_size - 1) / 2)

    for ind, pawn in enumerate(ap_active_pawns):
        new_position = pawn

        for _ in range(moves):
            new_position = get_next_position(new_position)

            if new_position in blocked_cells:
                break
        else:
            if new_position[0] == medium and new_position[1] == medium:
                remove_pawn(ind)
            else:
                ap_active_pawns[ind] = new_position
                set_blocked_cells()
            return True

    return False

def get_next_position(position: (int, int)):
    position = list(position)
    direction = get_direction(position)

    if direction == "right":
        position[1] += 1
    elif direction == "left":
        position[1] -= 1
    elif direction == "up":
        position[0] -= 1
    elif direction == "down":
        position[0] += 1

    return tuple(position)

def get_direction(position: (int, int)):
    medium = int((field_size - 1) / 2)

    # Side direction points
    right_side_point = (
            position[0] == 0 and position[1] == medium - 1 or
            position[0] == medium - 1 and position[1] == 0 or
            position[0] == medium - 1 and position[1] == medium + 1
    )

    left_side_point = (
            position[0] == medium + 1 and position[1] == medium - 1 or
            position[0] == medium + 1 and position[1] == field_size - 1 or
            position[0] == field_size - 1 and position[1] == medium + 1
    )

    up_side_point = (
            position[0] == medium - 1 and position[1] == medium - 1 or
            position[0] == medium + 1 and position[1] == 0 or
            position[0] == field_size - 1 and position[1] == position[1] == medium - 1
    )

    down_side_point = (
            position[0] == 0 and position[1] == medium + 1 or
            position[0] == medium - 1 and position[1] == field_size - 1 or
            position[0] == medium + 1 and position[1] == medium + 1
    )

    right_side_row = (position[0] == 0 or position[0] == medium - 1)
    left_side_row = (position[0] == medium + 1 or position[0] == field_size - 1)
    up_side_column = (position[1] == 0 or position[1] == medium - 1)
    down_side_column = (position[1] == medium + 1 or position[1] == field_size - 1)

    medium_a = (position[1] == medium and position[0] != field_size - 1)
    medium_b = (position[1] == medium and position[0] != 0)

    if ap_name == "a" and medium_a:
        return "down"
    elif ap_name == "b" and medium_b:
        return "up"
    elif right_side_point:
        return "right"
    elif left_side_point:
        return "left"
    elif up_side_point:
        return "up"
    elif down_side_point:
        return "down"
    elif right_side_row:
        return "right"
    elif left_side_row:
        return "left"
    elif up_side_column:
        return "up"
    elif down_side_column:
        return "down"

# Blocked cells
def set_blocked_cells():
    global ap_blocked_cells
    pawns = ap_active_pawns
    ap_blocked_cells = list(set([x for x in pawns if pawns.count(x) > 1]))
    set_start_limit()

def try_to_bit_pawn():
    same_pawn = list(set(ap_active_pawns) & set(pp_active_pawns))

    if same_pawn:
        pawn_ind = pp_active_pawns.index(same_pawn[0])
        print(pawn_ind, same_pawn)
        move_pawn_to_home(pawn_ind)
        print_field(f"Player {ap_name} bit pawn of {pp_name}")

# Move
def make_move(move: int) -> bool:
    did_move = move_pawn(move, ap_blocked_cells)

    if did_move:
        try_to_bit_pawn()

    return did_move

def move():
    for i in range(3):
        move = int(random.random() * 6 + 1)
        print_field(f"{ap_name} got {move} on the cube")

        if move != 6:
            did_move = make_move(move)

            if not did_move:
                print_field(f"No possible moves for {ap_name}")

            break

        six_move()

    change_turn()

def six_move():
    if ap_pawns_in_house:
        add_pawn()
        print_field(f"Player {ap_name} adds new pawn")
        try_to_bit_pawn()
    else:
        make_move(6)

def start():
    add_pawn()
    set_start_limit()
    change_turn()

    add_pawn()
    set_start_limit()
    change_turn()

    start_turn()

start()
while not not (pp_pawns_in_house or pp_active_pawns):
    move()

print_field(f"{pp_name} player won")
