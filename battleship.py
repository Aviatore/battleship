import copy
import pprint
from os import system
import random


AI_MODE = "normal" # if 'god_like' while picking a shot AI takes into account the ship length
MARK_MISS = chr(8729)
MARK_HIT = "H"
MARK_SUNK = "S"
MARK_EMPTY = "~"
MARK_HIT_COLOR = "\033[93m"
MARK_SUNK_COLOR = "\033[91m"
MARK_EMPTY_COLOR = "\033[96m"
MARK_MISS_COLOR = "\033[0m"
WHITE = "\033[0m"

def go_to_point(row, col):
    return f"\033[{row};{col}H"


def clear():
    system("clear")


def board_init(size):
    """Initilizes a board of custom size."""
    board = []
    for row in range(size):
        board.append((f"{MARK_EMPTY} "*size).split(' ')[:-1])
    return board


def board_row_color_parser(row):
    __row = copy.deepcopy(row)
    for index in range(len(__row)):
        if __row[index] == MARK_EMPTY:
            __row[index] = f"{MARK_EMPTY_COLOR}{MARK_EMPTY}{WHITE}"
        elif __row[index] == MARK_MISS:
            __row[index] = f"{MARK_MISS_COLOR}{MARK_MISS}{WHITE}"
        elif __row[index] == MARK_HIT:
            __row[index] = f"{MARK_HIT_COLOR}{MARK_HIT}{WHITE}"
        elif __row[index] == MARK_SUNK:
            __row[index] = f"{MARK_SUNK_COLOR}{MARK_SUNK}{WHITE}"
    return __row


def print_board(board):
    """Prints board to the screen during the placement phase."""
    row_len = len(board[0])
    col_len = len(board)
    rows_template = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    cols = []
    
    for col_index in range(col_len):
        cols.append(col_index + 1)
        
    cols_str = list(map(str, cols))
    rows = []
    
    for row_index in range(row_len):
        rows.append(rows_template[row_index])
  
    print(" ", " ".join(cols_str))
    
    for index in range(col_len):
        print(f"{rows[index]} {' '.join(board_row_color_parser(board[index]))}")
        
    print("")


def print_board_mod(board, row, col, player_name=""):
    """Prints board to the screen during the placement phase."""
    __row = row
    __col = col
    row_len = len(board[0])
    col_len = len(board)
    rows_template = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    cols = []
    
    for col_index in range(col_len):
        cols.append(col_index + 1)
        
    cols_str = list(map(str, cols))
    rows = []
    
    for row_index in range(row_len):
        rows.append(rows_template[row_index])
    
    print(f"{go_to_point(__row, __col)}{player_name}")
    __row += 1
    print(f"{go_to_point(__row, __col)}  {' '.join(cols_str)}")
    __row += 1
    for index in range(col_len):
        print(f"{go_to_point(__row, __col)}{rows[index]} {' '.join(board_row_color_parser(board[index]))}")
        __row += 1
        
    print("")


def print_table(ships, row, col, player_name):
    COL1_LEN = 7
    COL2_LEN = 10
    TABLE_WIDTH = len("-------+------------+------------")
    __row = row
    __col = col
    table_title = f"{player_name}'s ship stats"
    print(f"{go_to_point(__row, __col)}{table_title.center(TABLE_WIDTH)}")
    __row += 1
    print(f"{go_to_point(__row, __col)}-------+------------+------------")
    __row += 1
    print(f"{go_to_point(__row, __col)}Amount | Ship type  | Ship length")
    __row += 1
    print(f"{go_to_point(__row, __col)}-------+------------+------------")
    __row += 1

    for ship in ships.keys():
        print(f"{go_to_point(__row, __col)}{str(ships[ship][1]).center(COL1_LEN)}| {ship.ljust(COL2_LEN)} | {'X'*ships[ship][0]}")
        __row += 1


def print_boards(board1, board2, player1, player2):
    """Prints both boards to the screen."""
    BOARD_SIZE = len(board1)
    TABLE_ROWS_NUMBER = 8
    TABLE_LENGTH = len("-------+------------+------------")
    SPACING = 4

    if BOARD_SIZE < TABLE_ROWS_NUMBER:
        BOARD_Y_OFFSET = TABLE_ROWS_NUMBER - BOARD_SIZE + 2
    else:
        BOARD_Y_OFFSET = 3

    BOARD_X_OFFSET = TABLE_LENGTH + SPACING

    BOARD1_ROW = BOARD_Y_OFFSET
    BOARD1_COL = BOARD_X_OFFSET
    BOARD2_ROW = BOARD_Y_OFFSET
    BOARD2_COL = BOARD_X_OFFSET + (BOARD_SIZE * 2) + 2 + SPACING
    print_board_mod(board1, BOARD1_ROW, BOARD1_COL, player1['name'])
    print_board_mod(board2, BOARD2_ROW, BOARD2_COL, player2['name'])


def get_player_target_for_shot(opponent_board, player):
    """Asks the player for coordinates.
       Checks if the move is valid. Hits that target used coordinates or that target outside the range, are treated as invalid."""
    BOARD_SIZE = len(opponent_board)
    
    cols = []

    for col_index in range(BOARD_SIZE):
        cols.append(col_index + 1)

    cols_str = list(map(str, cols))
    
    rows_template = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    rows = []

    for row_index in range(BOARD_SIZE):
        rows.append(rows_template[row_index])

    user_input = None
    msg = ""

    while user_input is None:
        print(msg)
        msg = ""
        print(f"{player['name']}, give coordinates for the shot: ")
        user_input = input("> ")

        ROW = user_input[0] # The row letter
        COL = user_input[1] # The col number

        if user_input[0] == 'quit':
            print("Good bye!")
            exit()
        elif len(user_input) != 2:
            user_input = None
            continue
        elif ROW.upper() not in rows or COL not in cols_str:
            user_input = None
            continue
        else:
            row = rows.index(ROW.upper())
            col = cols.index(int(COL))

        if opponent_board[row][col] != MARK_EMPTY:
            msg = "You have already made a shot to this coordinates."
            user_input = None
            continue
    return row, col


def ai_is_ship_placed_horizontally(coords):
    ROW = 0

    if len(coords) > 1:
        if coords[0][ROW] == coords[1][ROW]:
            return True
        else:
            return False
    else:
        return True


def ai_horizontally_pick_coord(board, coords):
    BOARD_SIZE = len(board)
    ROW = 0
    COL = 1
    row = coords[0][ROW]

    col_index_left_shotted_module = min( map(lambda x : x[1], coords) )
    col_index_right_shotted_module = max( map(lambda x : x[1], coords) )

    coords_for_shot = []
    
    if col_index_left_shotted_module > 0:
        if board[row][col_index_left_shotted_module - 1] == MARK_EMPTY and ai_is_not_sunk_above_below(board, [row, col_index_left_shotted_module - 1]):
            if col_index_left_shotted_module - 1 > 0:
                if board[row][col_index_left_shotted_module - 2] in [MARK_EMPTY, MARK_MISS, MARK_HIT]:
                    coords_for_shot.append([row, col_index_left_shotted_module - 1])
            else:
                coords_for_shot.append([row, col_index_left_shotted_module - 1])
    
    if col_index_right_shotted_module < BOARD_SIZE - 1:
        if board[row][col_index_right_shotted_module + 1] == MARK_EMPTY and ai_is_not_sunk_above_below(board, [row, col_index_left_shotted_module + 1]):
            if col_index_right_shotted_module + 1 < BOARD_SIZE - 1:
                if board[row][col_index_right_shotted_module + 2] in [MARK_EMPTY, MARK_MISS, MARK_HIT]:
                    coords_for_shot.append([row, col_index_right_shotted_module + 1])
            else:
                coords_for_shot.append([row, col_index_right_shotted_module + 1])
    
    random_index = random.randrange(len(coords_for_shot))
    row = coords_for_shot[random_index][ROW]
    col = coords_for_shot[random_index][COL]
    return row, col   


def ai_pick_coord_from_single_hit(board, ship):
    BOARD_SIZE = len(board)
    ROW = 0
    COL = 1
    row, col = ship['shot'][0]

    valid_shots = []

    if ai_number_of_free_spaces_left_right(board, [row, col]) >= ship['len']:
        if col > 0:
            if board[row][col - 1] == MARK_EMPTY and ai_is_not_sunk_above_below(board, [row, col - 1]):
                if col - 1 > 0:
                    if board[row][col - 2] in [MARK_EMPTY, MARK_MISS, MARK_HIT]:
                        valid_shots.append([row, col - 1])
                else:
                    valid_shots.append([row, col - 1])
        
        if col < BOARD_SIZE - 1:
            if board[row][col + 1] == MARK_EMPTY and ai_is_not_sunk_above_below(board, [row, col + 1]):
                if col + 1 < BOARD_SIZE - 1:
                    if board[row][col + 2] in [MARK_EMPTY, MARK_MISS, MARK_HIT]:
                        valid_shots.append([row, col + 1])
                else:
                    valid_shots.append([row, col + 1])
    
    if ai_number_of_free_spaces_above_below(board, [row, col]) >= ship['len']:
        if row > 0:
            if board[row - 1][col] == MARK_EMPTY and ai_is_not_sunk_left_right(board, [row - 1, col]):
                if row - 1 > 0:
                    if board[row - 2][col] in [MARK_EMPTY, MARK_MISS, MARK_HIT]:
                        valid_shots.append([row - 1, col])
                else:
                    valid_shots.append([row - 1, col])
        
        if row < BOARD_SIZE - 1:
            if board[row + 1][col] == MARK_EMPTY and ai_is_not_sunk_left_right(board, [row + 1, col]):
                if row + 1 < BOARD_SIZE - 1:
                    if board[row + 2][col] in [MARK_EMPTY, MARK_MISS, MARK_HIT]:
                        valid_shots.append([row + 1, col])
                else:
                    valid_shots.append([row + 1, col])
    
    random_index = random.randrange(len(valid_shots))
    row = valid_shots[random_index][ROW]
    col = valid_shots[random_index][COL]
    return row, col


def ai_pick_coord_from_single_hit_normal_mode(board, coord):
    BOARD_SIZE = len(board)
    ROW = 0
    COL = 1
    row, col = coord

    valid_shots = []

    if col > 0:
        if board[row][col - 1] == MARK_EMPTY and ai_is_not_sunk_above_below(board, [row, col - 1]):
            if col - 1 > 0:
                if board[row][col - 2] in [MARK_EMPTY, MARK_MISS, MARK_HIT]:
                    valid_shots.append([row, col - 1])
            else:
                valid_shots.append([row, col - 1])
    
    if col < BOARD_SIZE - 1:
        if board[row][col + 1] == MARK_EMPTY and ai_is_not_sunk_above_below(board, [row, col + 1]):
            if col + 1 < BOARD_SIZE - 1:
                if board[row][col + 2] in [MARK_EMPTY, MARK_MISS, MARK_HIT]:
                    valid_shots.append([row, col + 1])
            else:
                valid_shots.append([row, col + 1])
    
    if row > 0:
        if board[row - 1][col] == MARK_EMPTY and ai_is_not_sunk_left_right(board, [row - 1, col]):
            if row - 1 > 0:
                if board[row - 2][col] in [MARK_EMPTY, MARK_MISS, MARK_HIT]:
                    valid_shots.append([row - 1, col])
            else:
                valid_shots.append([row - 1, col])
    
    if row < BOARD_SIZE - 1:
        if board[row + 1][col] == MARK_EMPTY and ai_is_not_sunk_left_right(board, [row + 1, col]):
            if row + 1 < BOARD_SIZE - 1:
                if board[row + 2][col] in [MARK_EMPTY, MARK_MISS, MARK_HIT]:
                    valid_shots.append([row + 1, col])
            else:
                valid_shots.append([row + 1, col])
    
    random_index = random.randrange(len(valid_shots))
    row = valid_shots[random_index][ROW]
    col = valid_shots[random_index][COL]
    return row, col


def ai_number_of_free_spaces_left_right(board, coord):
    """Counts free positions on the board on the left and on the right
       from the position specified by 'coord'"""
    BOARD_SIZE = len(board)
    row, col = coord

    free_spaces_number = 0
    
    # Count to the left
    for col_index in range(col - 1, -1, -1):
        if board[row][col_index] == MARK_EMPTY:
            free_spaces_number += 1
        else:
            break
    
    # Count to the right
    for col_index in range(col + 1, BOARD_SIZE):
        if board[row][col_index] == MARK_EMPTY:
            free_spaces_number += 1
        else:
            break
    
    return free_spaces_number
            

def ai_number_of_free_spaces_above_below(board, coord):
    """Counts free positions on the board above and below
       of the position specified by 'coord'"""
    BOARD_SIZE = len(board)
    row, col = coord

    free_spaces_number = 0
    
    # Count above
    for row_index in range(row + 1, BOARD_SIZE):
        if board[row_index][col] == MARK_EMPTY:
            free_spaces_number += 1
        else:
            break

    # Count below
    for row_index in range(row - 1, -1, -1):
        if board[row_index][col] == MARK_EMPTY:
            free_spaces_number += 1
        else:
            break

    return free_spaces_number


def ai_vertically_pick_coord(board, coords):
    BOARD_SIZE = len(board)
    ROW = 0
    COL = 1
    col = coords[0][COL]

    row_index_up_shotted_module = min( map(lambda x : x[0], coords) )
    row_index_down_shotted_module = max( map(lambda x : x[0], coords) )

    coords_for_shot = []

    if row_index_up_shotted_module > 0:
        if board[row_index_up_shotted_module - 1][col] == MARK_EMPTY and ai_is_not_sunk_left_right(board, [row_index_up_shotted_module - 1, col]):
            if row_index_up_shotted_module - 1 > 0:
                if board[row_index_up_shotted_module - 2][col] in [MARK_EMPTY, MARK_MISS, MARK_HIT]:
                    coords_for_shot.append([row_index_up_shotted_module - 1, col])
            else:
                coords_for_shot.append([row_index_up_shotted_module - 1, col])
    
    if row_index_down_shotted_module < BOARD_SIZE - 1:
        if board[row_index_down_shotted_module + 1][col] == MARK_EMPTY and ai_is_not_sunk_left_right(board, [row_index_up_shotted_module + 1, col]):
            if row_index_down_shotted_module + 1 < BOARD_SIZE - 1:
                if board[row_index_down_shotted_module + 2][col] in [MARK_EMPTY, MARK_MISS, MARK_HIT]:
                    coords_for_shot.append([row_index_down_shotted_module + 1, col])
            else:
                coords_for_shot.append([row_index_down_shotted_module + 1, col])

    random_index = random.randrange(len(coords_for_shot))
    row = coords_for_shot[random_index][ROW]
    col = coords_for_shot[random_index][COL]
    return row, col
    

def ai_get_coords_of_available_shots(board):
    SIZE = len(board)
    
    valid_shots = []
    for row_index in range(SIZE):
        for col_index in range(SIZE):
            if ai_is_shot_valid(board, [row_index, col_index]):
                valid_shots.append([row_index, col_index])
    
    return valid_shots


# The function checks if there is a sunk ship on the left or on the right-hand side
# from the specified position
def ai_is_not_sunk_left_right(board, coord):
    SIZE = len(board)

    row, col = coord

    if col > 0:
        if board[row][col - 1] == MARK_SUNK:
            return False
    
    if col < SIZE - 1:
        if board[row][col + 1] == MARK_SUNK:
            return False
    
    return True


# The function checks if there is a sunk ship above or below
# the specified position
def ai_is_not_sunk_above_below(board, coord):
    SIZE = len(board)

    row, col = coord

    if row > 0:
        if board[row - 1][col] == MARK_SUNK:
            return False
    
    if row < SIZE - 1:
        if board[row + 1][col] == MARK_SUNK:
            return False
    
    return True


def ai_is_shot_valid(board, coord):
    row, col = coord

    if board[row][col] == MARK_EMPTY:
        if ai_is_not_sunk_left_right(board, [row, col]) and ai_is_not_sunk_above_below(board, [row, col]):
            return True
        else:
            return False
    else:
        return False


def get_ai_target_for_shot(opponent_board, oponent_ship_stats, computer):
    """Pics a valid move"""
    row = col = None

    if AI_MODE == "god_like":
        for ship_type in oponent_ship_stats.keys():
            for ship in oponent_ship_stats[ship_type]:
                if len(ship['shot']) == 1:
                    row, col = ai_pick_coord_from_single_hit(opponent_board, ship)
                elif 1 < len(ship['shot']) < ship['len']:
                    if ai_is_ship_placed_horizontally(ship['shot']):
                        row, col = ai_horizontally_pick_coord(opponent_board, ship['shot'])
                    
                    if row is None:
                        row, col = ai_vertically_pick_coord(opponent_board, ship['shot'])
    else:
        for ship_type in oponent_ship_stats.keys():
            for ship in oponent_ship_stats[ship_type]:
                if len(ship['shot']) == 1:
                    row, col = ai_pick_coord_from_single_hit_normal_mode(opponent_board, ship['shot'][0])
                elif 1 < len(ship['shot']) < ship['len']:
                    if ai_is_ship_placed_horizontally(ship['shot']):
                        row, col = ai_horizontally_pick_coord(opponent_board, ship['shot'])
                    
                    if row is None:
                        row, col = ai_vertically_pick_coord(opponent_board, ship['shot'])
    
    if row is None or col is None:
        valid_shots = ai_get_coords_of_available_shots(opponent_board)

        valid_shots_random_index = random.randrange(len(valid_shots))
        row, col = valid_shots[valid_shots_random_index]

    return row, col


def shot(opponent_board, oponent_ship_stats, player, row, col):
    """Place the player's shot on the opponent's board.
       The shot mark (M, H, S) depends on the shot status, respectively: miss, hit or sunk"""
    
    for ship_type in oponent_ship_stats.keys():
        for ship in oponent_ship_stats[ship_type]:
            if [row, col] in ship['coord']:
                ship['shot'].append([row, col])
                if ship['len'] == len(ship['shot']):
                    for cord in ship['shot']:
                        opponent_board[cord[0]][cord[1]] = f"{MARK_SUNK_COLOR}{MARK_SUNK}{WHITE}"
                    return MARK_SUNK
                else:
                    opponent_board[row][col] = f"{MARK_HIT_COLOR}{MARK_HIT}{WHITE}"
                    return MARK_HIT
    else:
        opponent_board[row][col] = f"{MARK_MISS_COLOR}{MARK_MISS}{WHITE}"
        return MARK_MISS


def is_all_ships_destroyed(board, ship_stats):
    """Checks if all ships are destroyed.
       The 'board' variable can be used to mark all sunk ships with a color."""
    for ship_type in ship_stats:
        for ship in ship_stats[ship_type]:
            if len(ship['shot']) != ship['len']:
                return False
    return True


def coordinates_index_to_string(row, col):
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    cols = []
    for col_index in range(len(rows)):
        cols.append(col_index + 1)
    cols_str = list(map(str, cols))
    
    output = rows[row] + cols_str[col]
    return output    


def shot_msg(shot_result, player_name, row, col):
    if shot_result == MARK_HIT:
        return f"{player_name} has hit a ship at {coordinates_index_to_string(row, col)}!"
    elif shot_result == MARK_MISS:
        return f"{player_name} has missed at {coordinates_index_to_string(row, col)}!"
    elif shot_result == MARK_SUNK:
        return f"{player_name} has sunk a ship by a shot at {coordinates_index_to_string(row, col)}!"


def update_ships(ship_stats):
    ships = {
        'carrier': [5, 0],
        'battleship': [4, 0],
        'cruiser': [3, 0],
        'destroyer': [2, 0]
    }

    for ship_type in ship_stats:
        count = len(ship_stats[ship_type])
        for ship in ship_stats[ship_type]:
            if len(ship['shot']) == ship['len']:
                count -= 1
        ships[ship_type][1] = count
    
    return ships


def save_cursor_position():
    print("\033[s", end="")

def restore_cursor_position():
    print("\033[u\033[0K", end="")


def print_summary_message(board_size, game_mode, player_name=None):
    print("")
    if player_name is None:
        print("No more turns, it's a draw!")
    else:
        print(f"{player_name} won the game!")
    
    print("")
    print("If you want to play another game, write 'y'.")
    print("If you want to go back to main menu, write 'm'.")
    print("If you want to quit the game, write 'quit' or 'q'.")
    print("")
    save_cursor_position()
    user_input = None
    while user_input is None:
        restore_cursor_position()
        user_input = input("> ")
        if user_input not in ['y', 'm', 'q', 'quit']:
            user_input = None
        elif user_input == 'y':
            main(board_size, game_mode)
        elif user_input == 'm':
            pass
        elif user_input in ['quit', 'q']:
            print("Good bye!")
            exit()


def battleship_game(board1, board2, ship_stats1, ship_stats2, game_mode, player1, player2, turns_limit):
    """Game logic."""
    BOARD_SIZE = len(board1)
    SPACING = 4
    TABLE_WIDTH = len("-------+------------+------------")
    TABLE_ROWS_NUMBER = 8
    CONTENT_WIDTH = (TABLE_WIDTH * 2) + (SPACING * 3) + (((BOARD_SIZE * 2) + 2) * 2)

    TABLE_Y_OFFSET = BOARD_SIZE + 2 - TABLE_ROWS_NUMBER + 1 + 2
    if TABLE_Y_OFFSET < 2:
        TABLE_Y_OFFSET = 2

    TABLE1_X_OFFSET = 1
    TABLE2_X_OFFSET = (BOARD_SIZE * 2) - 1 + 2 + SPACING + TABLE_WIDTH + SPACING + (BOARD_SIZE * 2) - 1 + 2 + SPACING

    loop = True
    if game_mode == 'HUMAN-HUMAN':
        msg1 = ""
        msg2 = ""
        while turns_limit > 0:
            clear()
            turns_msg = f"Turns left: {turns_limit}"

            print(turns_msg.center(CONTENT_WIDTH))

            ships = update_ships(ship_stats1)
            print_table(ships, TABLE_Y_OFFSET, TABLE1_X_OFFSET, player1['name'])
            print_boards(board1, board2, player1, player2)
            ships = update_ships(ship_stats2)
            print_table(ships, TABLE_Y_OFFSET, TABLE2_X_OFFSET, player2['name'])
            if msg2 != "":
                print("")
                print(msg2)
                msg2 = ""

            row, col = get_player_target_for_shot(board2, player1)

            shot_result = shot(board2, ship_stats2, player1, row, col)
            msg1 = shot_msg(shot_result, player1['name'], row, col)

            if is_all_ships_destroyed(board2, ship_stats2):
                loop = False
                clear()
                ships = update_ships(ship_stats1)
                print_table(ships, TABLE_Y_OFFSET, TABLE1_X_OFFSET, player1['name'])
                print_boards(board1, board2, player1, player2)
                ships = update_ships(ship_stats2)
                print_table(ships, TABLE_Y_OFFSET, TABLE2_X_OFFSET, player2['name'])
                print_summary_message(BOARD_SIZE, game_mode, player1['name'])
                continue
            
            clear()
            turns_msg = f"Turns left: {turns_limit}"

            print(turns_msg.center(CONTENT_WIDTH))

            ships = update_ships(ship_stats1)
            print_table(ships, TABLE_Y_OFFSET, TABLE1_X_OFFSET, player1['name'])
            print_boards(board1, board2, player1, player2)
            ships = update_ships(ship_stats2)
            print_table(ships, TABLE_Y_OFFSET, TABLE2_X_OFFSET, player2['name'])
            if msg1 != "":
                print("")
                print(msg1)
                msg1 = ""
            row, col = get_player_target_for_shot(board1, player2)

            shot_result = shot(board1, ship_stats1, player2, row, col)
            msg2 = shot_msg(shot_result, player2['name'], row, col)

            if is_all_ships_destroyed(board1, ship_stats1):
                loop = False
                clear()
                ships = update_ships(ship_stats1)
                print_table(ships, TABLE_Y_OFFSET, TABLE1_X_OFFSET, player1['name'])
                print_boards(board1, board2, player1, player2)
                ships = update_ships(ship_stats2)
                print_table(ships, TABLE_Y_OFFSET, TABLE2_X_OFFSET, player2['name'])
                print_summary_message(BOARD_SIZE, game_mode, player2['name'])
                continue
            
            turns_limit -= 1
        
        print("No more turns, it's a draw!")

    elif game_mode == 'HUMAN-AI':
        msg1 = ""
        msg2 = ""
        while turns_limit > 0:
            clear()
            turns_msg = f"Turns left: {turns_limit}"

            print(turns_msg.center(CONTENT_WIDTH))

            ships = update_ships(ship_stats1)
            print_table(ships, TABLE_Y_OFFSET, TABLE1_X_OFFSET, player1['name'])
            print_boards(board1, board2, player1, player2)
            ships = update_ships(ship_stats2)
            print_table(ships, TABLE_Y_OFFSET, TABLE2_X_OFFSET, player2['name'])

            print("")
            print(msg1)
            print(msg2)
            msg1 = ""
            msg2 = ""

            row, col = get_player_target_for_shot(board2, player1)

            shot_result = shot(board2, ship_stats2, player1, row, col)
            msg1 = shot_msg(shot_result, player1['name'], row, col)

            if is_all_ships_destroyed(board2, ship_stats2):
                loop = False
                clear()
                ships = update_ships(ship_stats1)
                print_table(ships, TABLE_Y_OFFSET, TABLE1_X_OFFSET, player1['name'])
                print_boards(board1, board2, player1, player2)
                ships = update_ships(ship_stats2)
                print_table(ships, TABLE_Y_OFFSET, TABLE2_X_OFFSET, player2['name'])
                print_summary_message(BOARD_SIZE, game_mode, player1['name'])
                continue
            
            clear()
            ships = update_ships(ship_stats1)
            print_table(ships, TABLE_Y_OFFSET, TABLE1_X_OFFSET, player1['name'])
            print_boards(board1, board2, player1, player2)
            ships = update_ships(ship_stats2)
            print_table(ships, TABLE_Y_OFFSET, TABLE2_X_OFFSET, player2['name'])
            
            row, col = get_ai_target_for_shot(board1, ship_stats1, player2)

            shot_result = shot(board1, ship_stats1, player2, row, col)
            msg2 = shot_msg(shot_result, player2['name'], row, col)

            if is_all_ships_destroyed(board1, ship_stats1):
                loop = False
                print_summary_message(BOARD_SIZE, game_mode, player2['name'])
                continue

            turns_limit -= 1
        
        clear()
        ships = update_ships(ship_stats1)
        print_table(ships, TABLE_Y_OFFSET, TABLE1_X_OFFSET, player1['name'])
        print_boards(board1, board2, player1, player2)
        ships = update_ships(ship_stats2)
        print_table(ships, TABLE_Y_OFFSET, TABLE2_X_OFFSET, player2['name'])
        print_summary_message(BOARD_SIZE, game_mode)

def place_ship_horizontally(user_input, board, ships, ship_stats, ship_type, ship_len, col, row):
    board_size = len(board)

    for col_index in range(col - 1, col + ship_len):
        # Checks if col_index is within a valid range, i.e. between 0 and (board_size - 1)
        if col_index < 0:
            continue
        elif col_index > board_size - 1:
            user_input = None
            return "The coordinates are outside the board.", user_input
        
        # Checks if a ship overlaps other ship
        if board[row][col_index] != MARK_EMPTY:
            user_input = None
            return "The ship overlaps the other ship!", user_input
        
        # Checks if other ship is above or below
        if col <= col_index <= col + ship_len:
            for i in [-1, 1]:
                if 0 <= row + i <= board_size - 1: # Checks if indexes after modifications are within a valid range
                    if board[row + i][col_index] != MARK_EMPTY:
                        user_input = None
                        return "Ships are too close!", user_input
        
        # Checks if other ship is on the right
        if col_index == col + ship_len - 1 and col_index < board_size - 1:
            if board[row][col_index + 1] != MARK_EMPTY:
                user_input = None
                return "Ships are too close!", user_input

    if user_input is not None:
        coords = []
        for i in range(ship_len):
            board[row][col + i] = 'X'
            coords.append([row, col + i])
        
        ship = {
            'coord': coords,
            'shot': [],
            'len': ship_len
        }
        ship_stats[ship_type].append(ship)

        # ship_stats[ship_type]['coord'].append(coords)
        # ship_stats[ship_type]['num'] += 1
        ships[ship_type][1] -= 1
        return "", ""


def place_ship_vertically(user_input, board, ships, ship_stats, ship_type, ship_len, col, row):
    board_size = len(board)

    for row_index in range(row - 1, row + ship_len):
        # Checks if row_index is within a valid range, i.e. between 0 and (board_size - 1)
        if row_index < 0:
            continue
        elif row_index > board_size - 1:
            user_input = None
            return "The coordinates are outside the board.", user_input
        
        # Checks if a ship overlaps other ship
        if board[row_index][col] != MARK_EMPTY:
            user_input = None
            return "The ship overlaps the other ship!", user_input
        
        # Checks if other ship is on the left or on the right
        if row <= row_index <= row + ship_len:
            for i in [-1, 1]:
                if 0 <= col + i <= board_size - 1: # Checks if indexes after modifications are within a valid range
                    if board[row_index][col + i] != MARK_EMPTY:
                        user_input = None
                        return "Ships are too close!", user_input
                
        # Checks if other ship is below
        if row_index == row + ship_len - 1 and row_index < board_size - 1:
            if board[row_index + 1][col] != MARK_EMPTY:
                user_input = None
                return "Ships are too close!", user_input
            
    if user_input is not None:
        coords = []
        for i in range(ship_len):
            board[row + i][col] = 'X'
            coords.append([row + i, col])

        ship = {
            'coord': coords,
            'shot': [],
            'len': ship_len
        }
        ship_stats[ship_type].append(ship)
        # ship_stats[ship_type]['coord'].append(coords)
        # ship_stats[ship_type]['num'] += 1
        ships[ship_type][1] -= 1
        return "", ""


def is_ship_type_correct(ships, ship_name):
    for ship_type in ships:
        if not ship_type.find(ship_name) and ships[ship_type][1] > 0:
            return ship_type
    return None          


def place_ship(board, player, ship_stats, ships):
    """Controls the placement phase.
       Asks the player for coordinates, ship type and direction (h - horizontal or v - vertical), e.g. b2 cruiser h.
       """
    BOARD_SIZE = len(board)
    
    rows_template = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    cols = []

    for col_index in range(BOARD_SIZE):
        cols.append(col_index + 1)

    cols_str = list(map(str, cols))
    rows = []

    for row_index in range(BOARD_SIZE):
        rows.append(rows_template[row_index])

    user_input = None
    msg = ""

    while user_input is None:
        print(msg)
        msg = ""
        print("If you want to place your ships automatically, write 'auto' and press ENTER.")
        print(f"{player['name']}, give coordinates, type and direction of your ship: ")
        user_input = input("> ")
        user_input_list = user_input.split(" ")

        if user_input_list[0] == 'quit':
            print("Good bye!")
            exit()
        elif user_input_list[0] == 'auto':
            auto_ship_placement(board, ship_stats, ships)
            continue
        elif len(user_input_list) != 3:
            user_input = None
            continue

        ROW = user_input_list[0][0] # The row letter
        COL = user_input_list[0][1] # The col number
        SHIP_TYPE = user_input_list[1] # The name of the ship
        DIRECTION = user_input_list[2] # The direction code: 'h' - horizontally or 'v' - vertically

        if ROW.upper() not in rows or COL not in cols_str:
            user_input = None
            continue

        SHIP_TYPE = is_ship_type_correct(ships, SHIP_TYPE)
        if SHIP_TYPE is None:
            user_input = None
            continue
        # elif SHIP_TYPE not in ['carrier', 'battleship', 'cruiser', 'destroyer']:
        #     user_input = None
        #     continue
        elif DIRECTION not in ['h', 'v']:
            user_input = None
            continue

        SHIP_LEN = ships[SHIP_TYPE][0] # The length of the ship
        SHIP_AMOUNT = ships[SHIP_TYPE][1] # The number of ships to be placed on the board
        
        if SHIP_AMOUNT == 0:
            msg = f"You have no {SHIP_TYPE} left."
            user_input = None
            continue
        else:
            row = rows.index(ROW.upper())
            col = cols.index(int(COL))
        
        if DIRECTION == 'h':
            msg, user_input = place_ship_horizontally(user_input, board, ships, ship_stats, SHIP_TYPE, SHIP_LEN, col, row)
        
        elif DIRECTION == 'v':
            msg, user_input = place_ship_vertically(user_input, board, ships, ship_stats, SHIP_TYPE, SHIP_LEN, col, row)
    
    # DEBUG: Print the content of dictionaries:
    # pprint.pprint(ship_stats)
    # pprint.pprint(ships)


def auto_ship_placement(board, ship_stats, ships):
    BOARD_SIZE = len(board)
    __ships = copy.deepcopy(ships)
    loop = True

    while loop:
        user_input = None
        clear()
        ai_place_ship(board, ship_stats, __ships)
        print("")
        print_board(board)
        while user_input is None:
            user_input = input("Place ships again? ([y]/n): ")
            if user_input.upper() in ['Y', 'N', ""]:
                if user_input.upper() in ['Y', ""]:
                    for row in range(BOARD_SIZE):
                        for col in range(BOARD_SIZE):
                            board[row][col] = f"{MARK_EMPTY}"
                    for ship_type in ship_stats:
                        ship_stats[ship_type] = []
                    for ship_type in __ships:
                        ships[ship_type][1] = __ships[ship_type][1]
                else:
                    # Edit the reference of 'ships'
                    for ship_type in __ships:
                        ships[ship_type][1] = 0
                    return
            else:
                user_input = None
    
    


def check_all_ships_are_placed(ships):
    """Checks the remaining number of ships to be placed.
       If the number is non-zero, the function returns True.
       If there are no ships left, it returns False."""
    for ship_type in ships:
        if ships[ship_type][1] > 0:
            return True
    else:
        return False


def ai_get_ship_to_be_placed(ships):
    """Analysis the 'ships' dictionary and returns the ship type that needs to be placed"""
    for ship_type in ships:
        if ships[ship_type][1] > 0:
            return ship_type
    else:
        return False


def get_random_direction():
    directions = ['h', 'v']
    random_index = random.randrange(2)
    return directions[random_index]


def ai_check_nearby_free_places(board, coord):
    """Returns True if in any of the adjacent positions are something else than '~'"""
    BOARD_SIZE = len(board)
    row, col = coord
    
    if board[row][col] != MARK_EMPTY:
        return True
    if col > 0:
        if board[row][col - 1] != MARK_EMPTY:
            return True
    if col < BOARD_SIZE - 1:
        if board[row][col + 1] != MARK_EMPTY:
            return True
    if row > 0:
        if board[row - 1][col] != MARK_EMPTY:
            return True
    if row < BOARD_SIZE - 1:
        if board[row + 1][col] != MARK_EMPTY:
            return True
    
    return False


def ai_place_ship(board, ship_stats, ships):
    SHIP_LEN = 0
    SHIP_NUM = 1
    BOARD_SIZE = len(board)

    __ships = copy.deepcopy(ships)
    
    counter = 0
    ship_type = ai_get_ship_to_be_placed(__ships)
    while ship_type:
        direction = get_random_direction()
        if direction == 'h':
            row_random = random.randrange(BOARD_SIZE)
            col_random = random.randrange(BOARD_SIZE - __ships[ship_type][SHIP_LEN] + 1)

            for i in range(__ships[ship_type][SHIP_LEN]):
                if ai_check_nearby_free_places(board, [row_random, col_random + i]):
                    break
            else:
                coords = []
                for i in range(__ships[ship_type][SHIP_LEN]):
                    board[row_random][col_random + i] = 'X'
                    coords.append([row_random, col_random + i])

                ship = {
                    'coord': coords,
                    'shot': [],
                    'len': __ships[ship_type][SHIP_LEN]
                }
                ship_stats[ship_type].append(ship)
                __ships[ship_type][SHIP_NUM] -= 1

        elif direction == 'v':
            col_random = random.randrange(BOARD_SIZE)
            row_random = random.randrange(BOARD_SIZE - __ships[ship_type][SHIP_LEN] + 1)

            for i in range(__ships[ship_type][SHIP_LEN]):
                if ai_check_nearby_free_places(board, [row_random + i, col_random]):
                    break
            else:
                coords = []
                for i in range(__ships[ship_type][SHIP_LEN]):
                    board[row_random + i][col_random] = 'X'
                    coords.append([row_random + i, col_random])

                ship = {
                    'coord': coords,
                    'shot': [],
                    'len': __ships[ship_type][SHIP_LEN]
                }
                ship_stats[ship_type].append(ship)
                __ships[ship_type][SHIP_NUM] -= 1
        
        ship_type = ai_get_ship_to_be_placed(__ships)
        
        # Preventing from infinite loop. Some ships distribution may make it impossible to place all ships.
        if counter > 100:
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    board[row][col] = f"{MARK_EMPTY}" # Reset the board
            for ship_type in ship_stats:
                ship_stats[ship_type] = [] # Reset the ship_stats

            __ships = copy.deepcopy(ships) # Reset the __ships
            counter = 0
        counter += 1
    
    


def place_ship_loop(board, player, ship_stats, ships):
    __ships = copy.deepcopy(ships)
    BOARD_SIZE = len(board)
    TABLE_ROWS_NUMBER = 8
    TABLE_Y_OFFSET = BOARD_SIZE + 2 - TABLE_ROWS_NUMBER + 1
    if TABLE_Y_OFFSET < 2:
        TABLE_Y_OFFSET = 2
    TABLE_X_OFFSET = (BOARD_SIZE * 2) - 1 + 2 + 4

    if BOARD_SIZE < TABLE_ROWS_NUMBER:
        BOARD_Y_OFFSET = TABLE_ROWS_NUMBER - BOARD_SIZE - 0
    else:
        BOARD_Y_OFFSET = 1
    BOARD_X_OFFSET = 1

    while check_all_ships_are_placed(__ships):
        clear()
        print_board_mod(board, BOARD_Y_OFFSET, BOARD_X_OFFSET)
        # print_board(board)
        print_table(__ships, TABLE_Y_OFFSET, TABLE_X_OFFSET, player['name'])
        place_ship(board, player, ship_stats, __ships)
    
    clear()
    print_board_mod(board, BOARD_Y_OFFSET, BOARD_X_OFFSET)
    print_table(__ships, TABLE_Y_OFFSET, TABLE_X_OFFSET, player['name'])
    print("")
    input("All your ships are on positions. Press ENTER to continue ...")


def main(board_size=9, game_mode="HUMAN-AI"):
    # board_size = 7
    board1 = board_init(board_size)
    board2 = board_init(board_size)
    
    # Declaration of ship types. The lists contain two values:
    # - first, corresponds to the ship's size
    # - second, corresponds to the number of ship units that can be placed on board
    ships = {
        'carrier': [5, 1],
        'battleship': [4, 2],
        'cruiser': [3, 3],
        'destroyer': [2, 4]
    }

    # ships = {
    #     'carrier': [5, 1],
    #     'battleship': [4, 0],
    #     'cruiser': [3, 2],
    #     'destroyer': [2, 0]
    # }
    
    player1 = {
        'name': 'Ryland Hailey',
        'color': None
    }
    player2 = {
        'name': 'Ulric Alden',
        'color': None
    }
    
    # Declaration of dictionary that contains data about player's ships.
    # Each key corresponds to the ship type and contains a list of dictionaries 
    # with a ship data.
    # The structure of the example ship dictionary:
    # ship = {
    #         'coord': [[1,1],[1,2],[1,3]],
    #         'shot': [[1,2]],
    #         'len': 3
    #     }
    # The 'coord' key contains a nested list with coordinates of every ship module.
    # The 'shot' key contains a nested list with coordinates of shot modules.
    # The 'len' key contains a number of ship modules.
    ship_stats1 = {
        'carrier': [],
        'battleship': [],
        'cruiser': [],
        'destroyer': []
    }

    ship_stats2 = {
        'carrier': [],
        'battleship': [],
        'cruiser': [],
        'destroyer': []
    }
    
    turns_limit = 10

    # while True:
    #     clear()
    #     print_board(board1)
    #     print_table(ships, 5, 24)
    #     place_ship(board1, player1, ship_stats1, ships)
    # exit()

    # DEBUG: Computer places his ship
    # while True:
    #     ai_place_ship(board2, ship_stats2, ships)
    #     print_board(board2)
    #     input("Press any key to continue ...")
    #     board2 = board_init(board_size)
    #     ship_stats2 = {
    #         'carrier': [],
    #         'battleship': [],
    #         'cruiser': [],
    #         'destroyer': []
    #     }

    # Player1 places his ships
    place_ship_loop(board1, player1, ship_stats1, ships)
    
    # ai_place_ship(board1, ship_stats1, ships)
    # print_board(board1)
    # pprint.pprint(ship_stats1)
    # input("Player1 board, press any key to continue ...")
    # Player2 places his ships
    # place_ship_loop(board2, player2, ship_stats2, ships)

    ai_place_ship(board2, ship_stats2, ships)
    print_board(board2)
    input("Computer board, press any key to continue ...")

    # game_mode = "HUMAN-AI"
    
    # Reset player's boards
    board1 = board_init(board_size)
    board2 = board_init(board_size)
    
    battleship_game(board1, board2, ship_stats1, ship_stats2, game_mode, player1, player2, turns_limit)
    

main()
