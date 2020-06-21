import copy


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
       Checks if the move is valid. Hits that target used coordinates or that taget outside range, are trated as invalid."""
    row = 0
    col = 0
    
    return row, col


def get_ai_target_for_shot(opponent_board, oponent_ship_stats, computer):
    """Pics a valid move"""
    row = 0
    col = 0
    
    return row, col


def shot(opponent_board, oponent_ship_stats, player, row, col):
    """Place player's shot on oponent's board.
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
    pass


def check_all_ships_are_placed(ships):
    """Checks the remaining number of ships to be placed.
       If the number is non-zero, the function returns True.
       If there is no ships left, it returns False."""
    pass


def place_ship_loop(board, player, ship_stats, ships):
    __ships = copy.deepcopy(ships)
    
    while check_all_ships_are_placed(ships):
        print_board(board)
        place_ship(board, player, ship_stats, ships)


def main():
    board_size = 9
    board1 = board_init(board_size)
    board2 = board_init(board_size)
    
    print_board(board1)
    exit()
    
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

    # Player1 places his ships
    place_ship_loop(board1, player1, ship_stats1, ships)
    
    # Player2 places his ships
    place_ship_loop(board2, player2, ship_stats2, ships)

    game_mode = "HUMAN-HUMAN"
    
    battleship_game(board1, board2, ship_stats1, ship_stats2, game_mode, player1, player2)
    

main()
