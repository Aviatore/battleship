import copy
import pprint
from os import system
import random


AI_MODE = "normal" # if 'god_like' while picking a shot AI takes into account the ship length


def go_to_point(row, col):
    return f"\033[{row};{col}H"


def clear():
    system("clear")


def board_init(size):
    """Initilizes a board of custom size."""
    board = []
    for row in range(size):
        board.append(('0 '*size).split(' ')[:-1])
    return board


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
        print(f"{rows[index]} {' '.join(board[index])}")
        
    print("")


def print_board_mod(board, row, col, player):
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
    
    print(f"{go_to_point(__row, __col)}{player['name']}")
    __row += 1
    print(f"{go_to_point(__row, __col)}  {' '.join(cols_str)}")
    __row += 1
    for index in range(col_len):
        print(f"{go_to_point(__row, __col)}{rows[index]} {' '.join(board[index])}")
        __row += 1
        
    print("")


def print_table(ships, row, col):
    COL1_LEN = 7
    COL2_LEN = 10
    __row = row
    __col = col
    print(f"{go_to_point(__row, __col)}amount | ship type  | ship length")
    __row += 1
    print(f"{go_to_point(__row, __col)}-------+------------+------------")
    __row += 1

    for ship in ships.keys():
        print(f"{go_to_point(__row, __col)}{str(ships[ship][1]).center(COL1_LEN)}| {ship.ljust(COL2_LEN)} | {'X'*ships[ship][0]}")
        __row += 1


def print_boards(board1, board2, player1, player2):
    """Prints both boards to the screen."""
    BOARD1_ROW = 1
    BOARD1_COL = 1
    BOARD2_ROW = 1
    BOARD2_COL = 24
    print_board_mod(board1, BOARD1_ROW, BOARD1_COL, player1)
    print_board_mod(board2, BOARD2_ROW, BOARD2_COL, player2)


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
        user_input = input(f"{player['name']}, please give coordinates: ")

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

        if opponent_board[row][col] != '0':
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
        if board[row][col_index_left_shotted_module - 1] == '0' and ai_is_not_sunk_above_below(board, [row, col_index_left_shotted_module - 1]):
            if col_index_left_shotted_module - 1 > 0:
                if board[row][col_index_left_shotted_module - 2] in ['0', 'M', 'H']:
                    coords_for_shot.append([row, col_index_left_shotted_module - 1])
            else:
                coords_for_shot.append([row, col_index_left_shotted_module - 1])
    
    if col_index_right_shotted_module < BOARD_SIZE - 1:
        if board[row][col_index_right_shotted_module + 1] == '0' and ai_is_not_sunk_above_below(board, [row, col_index_left_shotted_module + 1]):
            if col_index_right_shotted_module + 1 < BOARD_SIZE - 1:
                if board[row][col_index_right_shotted_module + 2] in ['0', 'M', 'H']:
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
            if board[row][col - 1] == '0' and ai_is_not_sunk_above_below(board, [row, col - 1]):
                if col - 1 > 0:
                    if board[row][col - 2] in ['M', 'H', '0']:
                        valid_shots.append([row, col - 1])
                else:
                    valid_shots.append([row, col - 1])
        
        if col < BOARD_SIZE - 1:
            if board[row][col + 1] == '0' and ai_is_not_sunk_above_below(board, [row, col + 1]):
                if col + 1 < BOARD_SIZE - 1:
                    if board[row][col + 2] in ['M', 'H', '0']:
                        valid_shots.append([row, col + 1])
                else:
                    valid_shots.append([row, col + 1])
    
    if ai_number_of_free_spaces_above_below(board, [row, col]) >= ship['len']:
        if row > 0:
            if board[row - 1][col] == '0' and ai_is_not_sunk_left_right(board, [row - 1, col]):
                if row - 1 > 0:
                    if board[row - 2][col] in ['M', 'H', '0']:
                        valid_shots.append([row - 1, col])
                else:
                    valid_shots.append([row - 1, col])
        
        if row < BOARD_SIZE - 1:
            if board[row + 1][col] == '0' and ai_is_not_sunk_left_right(board, [row + 1, col]):
                if row + 1 < BOARD_SIZE - 1:
                    if board[row + 2][col] in ['M', 'H', '0']:
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
        if board[row][col - 1] == '0' and ai_is_not_sunk_above_below(board, [row, col - 1]):
            if col - 1 > 0:
                if board[row][col - 2] in ['M', 'H', '0']:
                    valid_shots.append([row, col - 1])
            else:
                valid_shots.append([row, col - 1])
    
    if col < BOARD_SIZE - 1:
        if board[row][col + 1] == '0' and ai_is_not_sunk_above_below(board, [row, col + 1]):
            if col + 1 < BOARD_SIZE - 1:
                if board[row][col + 2] in ['M', 'H', '0']:
                    valid_shots.append([row, col + 1])
            else:
                valid_shots.append([row, col + 1])
    
    if row > 0:
        if board[row - 1][col] == '0' and ai_is_not_sunk_left_right(board, [row - 1, col]):
            if row - 1 > 0:
                if board[row - 2][col] in ['M', 'H', '0']:
                    valid_shots.append([row - 1, col])
            else:
                valid_shots.append([row - 1, col])
    
    if row < BOARD_SIZE - 1:
        if board[row + 1][col] == '0' and ai_is_not_sunk_left_right(board, [row + 1, col]):
            if row + 1 < BOARD_SIZE - 1:
                if board[row + 2][col] in ['M', 'H', '0']:
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
        if board[row][col_index] == '0':
            free_spaces_number += 1
        else:
            break
    
    # Count to the right
    for col_index in range(col + 1, BOARD_SIZE):
        if board[row][col_index] == '0':
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
        if board[row_index][col] == '0':
            free_spaces_number += 1
        else:
            break

    # Count below
    for row_index in range(row - 1, -1, -1):
        if board[row_index][col] == '0':
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
        if board[row_index_up_shotted_module - 1][col] == '0' and ai_is_not_sunk_left_right(board, [row_index_up_shotted_module - 1, col]):
            if row_index_up_shotted_module - 1 > 0:
                if board[row_index_up_shotted_module - 2][col] in ['0', 'M', 'H']:
                    coords_for_shot.append([row_index_up_shotted_module - 1, col])
            else:
                coords_for_shot.append([row_index_up_shotted_module - 1, col])
    
    if row_index_down_shotted_module < BOARD_SIZE - 1:
        if board[row_index_down_shotted_module + 1][col] == '0' and ai_is_not_sunk_left_right(board, [row_index_up_shotted_module + 1, col]):
            if row_index_down_shotted_module + 1 < BOARD_SIZE - 1:
                if board[row_index_down_shotted_module + 2][col] in ['0', 'M', 'H']:
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
        if board[row][col - 1] == 'S':
            return False
    
    if col < SIZE - 1:
        if board[row][col + 1] == 'S':
            return False
    
    return True


# The function checks if there is a sunk ship above or below
# the specified position
def ai_is_not_sunk_above_below(board, coord):
    SIZE = len(board)

    row, col = coord

    if row > 0:
        if board[row - 1][col] == 'S':
            return False
    
    if row < SIZE - 1:
        if board[row + 1][col] == 'S':
            return False
    
    return True


def ai_is_shot_valid(board, coord):
    row, col = coord

    if board[row][col] == '0':
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
                        opponent_board[cord[0]][cord[1]] = 'S'
                    return
                else:
                    opponent_board[row][col] = 'H'
                    return
    else:
        opponent_board[row][col] = 'M'


def is_all_ships_destroyed(board, ship_stats):
    """Checks if all ships are destroyed.
       The 'board' variable can be used to mark all sunk ships with a color."""
    pass


def battleship_game(board1, board2, ship_stats1, ship_stats2, game_mode, player1, player2):
    """Game logic."""
    loop = True
    if game_mode == 'HUMAN-HUMAN':
        while loop:
            clear()
            print_boards(board1, board2, player1, player2)
            row, col = get_player_target_for_shot(board2, player1)
            shot(board2, ship_stats2, player1, row, col)
            if is_all_ships_destroyed(board2, ship_stats2):
                loop = False
                continue
            
            clear()
            print_boards(board1, board2, player1, player2)
            row, col = get_player_target_for_shot(board1, player2)
            shot(board1, ship_stats1, player2, row, col)
            if is_all_ships_destroyed(board1, ship_stats1):
                loop = False
                continue
    elif game_mode == 'HUMAN-AI':
        while loop:
            clear()
            print_boards(board1, board2, player1, player2)
            row, col = get_player_target_for_shot(board2, player1)
            shot(board2, ship_stats2, player1, row, col)
            if is_all_ships_destroyed(board2, ship_stats2):
                loop = False
                continue
            
            clear()
            print_boards(board1, board2, player1, player2)
            row, col = get_ai_target_for_shot(board1, ship_stats1, player2)
            shot(board1, ship_stats1, player2, row, col)
            if is_all_ships_destroyed(board1, ship_stats1):
                loop = False
                continue

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
        if board[row][col_index] != '0':
            user_input = None
            return "The ship overlaps the other ship!", user_input
        
        # Checks if other ship is above or below
        if col <= col_index <= col + ship_len:
            for i in [-1, 1]:
                if 0 <= row + i <= board_size - 1: # Checks if indexes after modifications are within a valid range
                    if board[row + i][col_index] != '0':
                        user_input = None
                        return "Ships are too close!", user_input
        
        # Checks if other ship is on the right
        if col_index == col + ship_len - 1 and col_index < board_size - 1:
            if board[row][col_index + 1] != '0':
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
        if board[row_index][col] != '0':
            user_input = None
            return "The ship overlaps the other ship!", user_input
        
        # Checks if other ship is on the left or on the right
        if row <= row_index <= row + ship_len:
            for i in [-1, 1]:
                if 0 <= col + i <= board_size - 1: # Checks if indexes after modifications are within a valid range
                    if board[row_index][col + i] != '0':
                        user_input = None
                        return "Ships are too close!", user_input
                
        # Checks if other ship is below
        if row_index == row + ship_len - 1 and row_index < board_size - 1:
            if board[row_index + 1][col] != '0':
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
        user_input = input(f"{player['name']}, please give coordinates: ")
        user_input_list = user_input.split(" ")

        

        if user_input_list[0] == 'quit':
            print("Good bye!")
            exit()
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
        elif SHIP_TYPE not in ['carrier', 'battleship', 'cruiser', 'destroyer']:
            user_input = None
            continue
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
    """Returns True if in any of the adjacent positions are something else than '0'"""
    BOARD_SIZE = len(board)
    row, col = coord
    
    if board[row][col] != '0':
        return True
    if col > 0:
        if board[row][col - 1] != '0':
            return True
    if col < BOARD_SIZE - 1:
        if board[row][col + 1] != '0':
            return True
    if row > 0:
        if board[row - 1][col] != '0':
            return True
    if row < BOARD_SIZE - 1:
        if board[row + 1][col] != '0':
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
            board = board_init(BOARD_SIZE) # Reset the board
            __ships = copy.deepcopy(ships) # Reset the __ships
            ship_stats = {
                'carrier': [],
                'battleship': [],
                'cruiser': [],
                'destroyer': []
            }
            counter = 0
        counter += 1


def place_ship_loop(board, player, ship_stats, ships):
    __ships = copy.deepcopy(ships)
    
    while check_all_ships_are_placed(__ships):
        clear()
        print_board(board)
        print_table(__ships, 5, 24)
        place_ship(board, player, ship_stats, __ships)


def main():
    board_size = 9
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
    # The 'coord' key contains a list of coordinates of every ship of its kind, e.g. [ [ [1,1],[1,2] ], [ [3,3],[3,4] ] ]
    # [
    #     [
    #         [1,1], [1,2] # First 'destroyer'
    #     ],
    #     [
    #         [3,3], [3,4] # Second 'destroyer'
    #     ],
    # ]
    # The 'num' key contains the number of ships of its kind. Whenever a ship is sunk, the number is decreased by one.
    # The function 'is_all_ships_destroyed(board, ship_stats)' checks this value to check if all ships were destroyed.
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
    
    # ship_stats1_tmp = {
    #     'carrier': {
    #         'coord': [],
    #         'num': 0
    #         },
    #     'battleship': {
    #         'coord': [],
    #         'num': 0
    #         },
    #     'cruiser': {
    #         'coord': [],
    #         'num': 0
    #         },
    #     'destroyer': {
    #         'coord': [],
    #         'num': 0
    #         },
    # }
    
    # ship_stats2_tmp = {
    #     'carrier': {
    #         'coord': [],
    #         'num': 0
    #         },
    #     'battleship': {
    #         'coord': [],
    #         'num': 0
    #         },
    #     'cruiser': {
    #         'coord': [],
    #         'num': 0
    #         },
    #     'destroyer': {
    #         'coord': [],
    #         'num': 0
    #         },
    # }

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
    # place_ship_loop(board1, player1, ship_stats1, ships)
    
    ai_place_ship(board1, ship_stats1, ships)
    print_board(board1)
    # pprint.pprint(ship_stats1)
    input("Player1 board, press any key to continue ...")
    # Player2 places his ships
    # place_ship_loop(board2, player2, ship_stats2, ships)

    ai_place_ship(board2, ship_stats2, ships)
    print_board(board2)
    # pprint.pprint(ship_stats2)
    input("Computer board, press any key to continue ...")

    game_mode = "HUMAN-AI"
    
    # Reset player's boards
    board1 = board_init(board_size)
    board2 = board_init(board_size)
    
    battleship_game(board1, board2, ship_stats1, ship_stats2, game_mode, player1, player2)
    

main()
