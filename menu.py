from os import system


COLOR_CYAN = "\033[96m"
COLOR_WHITE = "\033[0m"


def print_logo():
    LOGO = """
    ____        __  __  __          __    _     
   / __ )____ _/ /_/ /_/ /__  _____/ /_  (_)___ 
  / __  / __ `/ __/ __/ / _ \/ ___/ __ \/ / __ \\
 / /_/ / /_/ / /_/ /_/ /  __(__  ) / / / / /_/ /
/_____/\__,_/\__/\__/_/\___/____/_/ /_/_/ .___/ 
                                       /_/   """
    print(f"{COLOR_CYAN}{LOGO}{COLOR_WHITE}")


def clear():
    system("clear")
    print_logo()

def menu(board_size=None, game_mode=None, player1=None, player2=None):
    if board_size is None:    
        board_size = 9
    if game_mode is None:
        game_mode = "HUMAN-AI"
    game_mode_dict = {
        "HUMAN-AI": "HUMAN vs. COMPUTER",
        "HUMAN-HUMAN": "HUMAN vs. HUMAN"
    }
    turns_limit = -1
    if turns_limit < 0:
        turns_limit_str = "infinite"
    else:
        turns_limit_str = str(turns_limit)
    
    user_input = None
    while user_input is None:
        clear()
        print(f"1. Battlefield size: {board_size}x{board_size}")
        print(f"2. Game mode: {game_mode_dict[game_mode]}")
        print(f"3. Turns limit: {turns_limit_str}")
        print("4. Next")
        print("\nGive the number of chosen option and press ENTER:")
        user_input = input("> ")
        
        if len(user_input) == 0:
            user_input = None
            continue
        elif user_input == "quit":
            print("Good bye!")
            exit()
        elif len(user_input) > 1:
            user_input = None
            continue
        elif not user_input.isdigit():
            user_input = None
            continue
        elif int(user_input) not in range(1, 5):
            user_input = None
            continue
        elif user_input == "1":
            board_size = battlefield_size()
            user_input = None
            continue
        elif user_input == "2":
            game_mode = gamemode()
            user_input = None
            continue
        elif user_input == "3":
            turns_limit = turnslimit(board_size)
            user_input = None
            continue
        elif user_input == "4":
            board_size, game_mode, ships, player1, player2, turns_limit, goback = next_menu(board_size, game_mode, turns_limit, player1, player2)
            if goback is True:
                user_input = None
                continue
            else:
                return board_size, game_mode, ships, player1, player2, turns_limit
                
            

def battlefield_size():
    user_input = None
    while user_input is None:
        clear()
        print("Please, give a number within a range between 5 and 9:")
        user_input = input("> ")
        
        if len(user_input) == 0:
            user_input = None
            continue
        elif user_input == "quit":
            print("Good bye!")
            exit()
        elif len(user_input) > 1:
            user_input = None
            continue
        elif not user_input.isdigit():
            user_input = None
            continue
        elif int(user_input) not in range(5, 10):
            user_input = None
            continue
        
        return int(user_input)


def gamemode():
    user_input = None
    while user_input is None:
        clear()
        print("1. HUMAN vs. COMPUTER")
        print("2. HUMAN vs. HUMAN")
        print("\nGive the number of chosen option and press ENTER:")
        user_input = input("> ")
        
        if len(user_input) == 0:
            user_input = None
            continue
        elif user_input == "quit":
            print("Good bye!")
            exit()
        elif len(user_input) > 1:
            user_input = None
            continue
        elif not user_input.isdigit():
            user_input = None
            continue
        elif int(user_input) not in range(1, 3):
            user_input = None
            continue
        elif user_input == "1":
            return "HUMAN-AI"
        elif user_input == "2":
            return "HUMAN-HUMAN"
        

def turnslimit(board_size):
    board_size_to_limits = {
        9: 30,
        8: 27,
        7: 23,
        6: 18,
        5: 13
    }
    user_input = None
    while user_input is None:
        clear()
        print(f"Please, give a number higher than {board_size_to_limits[board_size]}, or '0' for infinite:")
        user_input = input("> ")
        
        if len(user_input) == 0:
            user_input = None
            continue
        elif user_input == "quit":
            print("Good bye!")
            exit()
        elif not user_input.isdigit():
            user_input = None
            continue
        elif user_input == "0":
            return -1
        elif int(user_input) < board_size_to_limits[board_size]:
            user_input = None
            continue
        
        return int(user_input)


def next_menu(board_size, game_mode, turns_limit, player1=None, player2=None):
    CARRIER = 0
    BATTLESHIP = 1
    CRUISER = 2
    DESTROYER = 3
    board_size_to_limits = {
        9: [1,2,3,4],
        8: [1,2,2,4],
        7: [1,1,2,3],
        6: [0,1,2,3],
        5: [0,1,1,2]
    }
    ships = {
        'carrier': [5, board_size_to_limits[board_size][CARRIER]],
        'battleship': [4, board_size_to_limits[board_size][BATTLESHIP]],
        'cruiser': [3, board_size_to_limits[board_size][CRUISER]],
        'destroyer': [2, board_size_to_limits[board_size][DESTROYER]]
    }
    
    user_input = None
    
    if game_mode == "HUMAN-AI":
        if player1 is None:
            player1 = {
                'name': 'Player',
                'color': None
            }
            
        player2 = {
            'name': 'Computer',
            'color': None
        }
        while user_input is None:
            clear()
            print(f"1. Player's name: {player1['name']}")
            print("2. Back to main menu")
            print("3. Go to battlefield")
            print("\nGive the number of chosen option and press ENTER:")
            user_input = input("> ")
            
            if len(user_input) == 0:
                user_input = None
                continue
            elif user_input == "quit":
                print("Good bye!")
                exit()
            elif len(user_input) > 1:
                user_input = None
                continue
            elif not user_input.isdigit():
                user_input = None
                continue
            elif int(user_input) not in range(1, 4):
                user_input = None
                continue
            elif user_input == "1":
                player1['name'] = get_player_name()
                user_input = None
                continue
            elif user_input == "2":
                return board_size, game_mode, ships, player1, player2, turns_limit, True
            elif user_input == "3":
                return board_size, game_mode, ships, player1, player2, turns_limit, False
    elif game_mode == "HUMAN-HUMAN":
        if player1 is None:
            player1 = {
                'name': 'Player1',
                'color': None
            }
            player2 = {
                'name': 'Player2',
                'color': None
            }
        while user_input is None:
            clear()
            print(f"1. Player1's name: {player1['name']}")
            print(f"2. Player2's name: {player2['name']}")
            print("3. Back to main menu")
            print("4. Go to battlefield")
            print("\nGive the number of chosen option and press ENTER:")
            user_input = input("> ")
            
            if len(user_input) == 0:
                user_input = None
                continue
            elif user_input == "quit":
                print("Good bye!")
                exit()
            elif len(user_input) > 1:
                user_input = None
                continue
            elif not user_input.isdigit():
                user_input = None
                continue
            elif int(user_input) not in range(1, 5):
                user_input = None
                continue
            elif user_input == "1":
                player1['name'] = get_player_name()
                user_input = None
                continue
            elif user_input == "2":
                player2['name'] = get_player_name()
                user_input = None
                continue
            elif user_input == "3":
                return board_size, game_mode, ships, player1, player2, turns_limit, True
            elif user_input == "4":
                return board_size, game_mode, ships, player1, player2, turns_limit, False


def get_player_name():
    user_input = None
    while user_input is None:
        clear()
        print("Please, give a player's name: ")
        user_input = input("> ")
        
        if len(user_input) == 0:
            user_input = None
            continue
        elif user_input == "quit":
            print("Good bye!")
            exit()
        
        return user_input