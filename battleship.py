import copy
import pprint


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


def print_boards(board1, board2):
    """Prints both boards to the screen."""
    pass


def get_player_target_for_shot(opponent_board, player):
    """Asks the player for coordinates.
       Checks if the move is valid. Hits that target used coordinates or that target outside the range, are treated as invalid."""
    row = 0
    col = 0
    
    return row, col


def get_ai_target_for_shot(opponent_board, oponent_ship_stats, computer):
    """Pics a valid move"""
    row = 0
    col = 0
    
    return row, col


def shot(opponent_board, oponent_ship_stats, player, row, col):
    """Place the player's shot on the opponent's board.
       The shot mark (M, H, S) depends on the shot status, respectively: miss, hit or sunk"""
    pass


def is_all_ships_destroyed(board, ship_stats):
    """Checks if all ships are destroyed.
       The 'board' variable can be used to mark all sunk ships with a color."""
    pass


def battleship_game(board1, board2, ship_stats1, ship_stats2, game_mode, player1, player2):
    """Game logic."""
    loop = True
    while loop:
        print_boards(board1, board2)
        row, col = get_player_target_for_shot(board2, player1)
        shot(board2, ship_stats2, player1, row, col)
        if is_all_ships_destroyed(board2, ship_stats2):
            loop = False
            continue
        
        print_boards(board1, board2)
        row, col = get_player_target_for_shot(board1, player2)
        shot(board1, ship_stats1, player2, row, col)
        if is_all_ships_destroyed(board1, ship_stats1):
            loop = False
            continue


def place_ship(board, player, ship_stats, ships):
    """Controls the placement phase.
       Asks the player for coordinates, ship type and direction (h - horizontal or v - vertical), e.g. b2 cruiser h.
       """
    board_size = len(board)
    ROW = 0
    COL = 1
    SHIP = 1
    SHIP_LEN = 0
    SHIP_NUM = 1
    DIRECTION = 2
    LEFT, DOWN = [-1, -1]
    RIGHT, UP = [1, 1]
    STAY = 0
    
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
        elif user_input_list[0][ROW].upper() not in rows or user_input_list[0][COL] not in cols_str:
            user_input = None
            continue
        elif user_input_list[SHIP] not in ['carrier', 'battleship', 'cruiser', 'destroyer']:
            user_input = None
            continue
        elif user_input_list[DIRECTION] not in ['h', 'v']:
            user_input = None
            continue
        else:
            row = rows.index(user_input_list[0][ROW].upper())
            col = cols.index(int(user_input_list[0][COL]))
        
        dirs_row = [STAY, UP, DOWN, STAY]
        dirs_col = [LEFT, STAY, STAY, RIGHT]
        dirs = list(zip(dirs_row, dirs_col))
        
        if user_input_list[DIRECTION] == 'h':
            
            for col_index in range(col - 1, col + ships[user_input_list[SHIP]][SHIP_LEN]):
                # Checks if col_index is within a valid range, i.e. between 0 and (board_size - 1)
                if col_index < 0:
                    continue
                elif col_index > board_size - 1:
                    print("Edge")
                    user_input = None
                    break
                
                # Checks if a ship overlaps other ship
                if board[row][col_index] != '0':
                    msg = "Ships are too close!"
                    user_input = None
                    break
                
                # Checks if other ship is above or below
                if col <= col_index <= col + ships[user_input_list[SHIP]][SHIP_LEN]:
                    for i in [-1, 1]:
                        if 0 <= row + i <= board_size - 1: # Checks if indexes after modifications are within a valid range
                            if board[row + i][col_index] != '0':
                                msg = "Ships are too close!"
                                user_input = None
                                break
                    #else:
                        #break
                
                # Checks if other ship is on the right
                if col_index == col + ships[user_input_list[SHIP]][SHIP_LEN] - 1 and col_index < board_size - 1:
                    if board[row][col_index + 1] != '0':
                        msg = "Ships are too close!"
                        user_input = None
                        break
            
            if user_input is not None:
                coords = []
                for i in range(ships[user_input_list[SHIP]][SHIP_LEN]):
                    board[row][col + i] = 'X'
                    coords.append([row, col + i])
                ship_stats[user_input_list[SHIP]]['coord'].append(coords)
                ship_stats[user_input_list[SHIP]]['num'] += 1
        
        elif user_input_list[DIRECTION] == 'v':
            for row_index in range(row - 1, row + ships[user_input_list[SHIP]][SHIP_LEN]):
                # Checks if row_index is within a valid range, i.e. between 0 and (board_size - 1)
                if row_index < 0:
                    continue
                elif row_index > board_size - 1:
                    print("Edge")
                    user_input = None
                    break
                
                # Checks if a ship overlaps other ship
                if board[row_index][col] != '0':
                    msg = "Ships are too close!"
                    user_input = None
                    break
                
                # Checks if other ship is on the left or on the right
                if row <= row_index <= row + ships[user_input_list[SHIP]][SHIP_LEN]:
                    for i in [-1, 1]:
                        if 0 <= col + i <= board_size - 1: # Checks if indexes after modifications are within a valid range
                            if board[row_index][col + i] != '0':
                                msg = "Ships are too close!"
                                user_input = None
                                break
                    #else:
                        #break
                        
                # Checks if other ship is below
                if row_index == row + ships[user_input_list[SHIP]][SHIP_LEN] - 1 and row_index < board_size - 1:
                    if board[row_index + 1][col] != '0':
                        msg = "Ships are too close!"
                        user_input = None
                        break
                    
            if user_input is not None:
                coords = []
                for i in range(ships[user_input_list[SHIP]][SHIP_LEN]):
                    board[row + i][col] = 'X'
                    coords.append([row + i, col])
                ship_stats[user_input_list[SHIP]]['coord'].append(coords)
                ship_stats[user_input_list[SHIP]]['num'] += 1
    
    
    pprint.pprint(ship_stats)


def check_all_ships_are_placed(ships):
    """Checks the remaining number of ships to be placed.
       If the number is non-zero, the function returns True.
       If there are no ships left, it returns False."""
    pass


def place_ship_loop(board, player, ship_stats, ships):
    __ships = copy.deepcopy(ships)
    
    while check_all_ships_are_placed(__ships):
        print_board(board)
        place_ship(board, player, ship_stats, __ships)


def main():
    board_size = 9
    board1 = board_init(board_size)
    board2 = board_init(board_size)
    
    # Declaration of ship types. The lists contain two values:
    # - first, corresponds to the ship's size
    # - second, corresponds to the number of ship units that can be placed on board
    ships = {
        'carrier': [5, 2],
        'battleship': [4, 3],
        'cruiser': [3, 3],
        'destroyer': [2, 3]
    }
    
    player1 = {
        'name': 'WW',
        'color': None
    }
    player2 = {
        'name': 'WW',
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
        'carrier': {
            'coord': [],
            'num': 0
            },
        'battleship': {
            'coord': [],
            'num': 0
            },
        'cruiser': {
            'coord': [],
            'num': 0
            },
        'destroyer': {
            'coord': [],
            'num': 0
            },
    }
    
    ship_stats2 = {
        'carrier': {
            'coord': [],
            'num': 0
            },
        'battleship': {
            'coord': [],
            'num': 0
            },
        'cruiser': {
            'coord': [],
            'num': 0
            },
        'destroyer': {
            'coord': [],
            'num': 0
            },
    }

    while True:
        print_board(board1)
        place_ship(board1, player1, ship_stats1, ships)
    exit()

    

    # Player1 places his ships
    place_ship_loop(board1, player1, ship_stats1, ships)
    
    # Player2 places his ships
    place_ship_loop(board2, player2, ship_stats2, ships)

    game_mode = "HUMAN-HUMAN"
    
    # Reset player's boards
    board1 = board_init(board_size)
    board2 = board_init(board_size)
    
    battleship_game(board1, board2, ship_stats1, ship_stats2, game_mode, player1, player2)
    

main()
