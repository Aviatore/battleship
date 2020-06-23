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
        ship_stats[ship_type]['coord'].append(coords)
        ship_stats[ship_type]['num'] += 1
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
        ship_stats[ship_type]['coord'].append(coords)
        ship_stats[ship_type]['num'] += 1
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

        ROW = user_input_list[0][0] # The row letter
        COL = user_input_list[0][1] # The col number
        SHIP_TYPE = user_input_list[1] # The name of the ship
        SHIP_LEN = ships[SHIP_TYPE][0] # The length of the ship
        SHIP_AMOUNT = ships[SHIP_TYPE][1] # The number of ships to be placed on the board
        DIRECTION = user_input_list[2] # The direction code: 'h' - horizontally or 'v' - vertically

        if user_input_list[0] == 'quit':
            print("Good bye!")
            exit()
        elif len(user_input_list) != 3:
            user_input = None
            continue
        elif ROW.upper() not in rows or COL not in cols_str:
            user_input = None
            continue
        elif SHIP_TYPE not in ['carrier', 'battleship', 'cruiser', 'destroyer']:
            user_input = None
            continue
        elif DIRECTION not in ['h', 'v']:
            user_input = None
            continue
        elif SHIP_AMOUNT == 0:
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
    
    
    pprint.pprint(ship_stats)
    pprint.pprint(ships)


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
        'carrier': [5, 1],
        'battleship': [4, 2],
        'cruiser': [3, 3],
        'destroyer': [2, 4]
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
