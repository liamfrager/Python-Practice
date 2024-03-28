from os import name, system

logo = 'Tic-Tac-Toe'
board = ''


def new_game():
    _ = {
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
    }

    def refresh_display():
        # for windows
        if name == 'nt':
            __ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            __ = system('clear')

        print(logo)
        global board
        board = f'''
                {_['1']} | {_['2']} | {_['3']}
                {_['4']} | {_['5']} | {_['6']}
                {_['7']} | {_['8']} | {_['9']}
                '''
        print(board)

    def is_winning_move(move):
        print(move)
        ####################### CHECK IF MOVE WINS ##############################
        return False

    player = 1
    valid_moves = 9
    while True:
        refresh_display()
        try:
            move = int(
                input(f'{'X' if player > 0 else 'O'}, where would you like to go?: '))
        except:
            print('Not a valid move. Try again.')
            continue
        if str(move) in board:
            _[str(move)] = 'X' if player > 0 else 'O'
            player *= -1
            valid_moves -= 1
        else:
            print('Not a valid move. Try again.')
        if valid_moves == 0:
            break
        elif is_winning_move(move):
            break

    refresh_display()
    print(f'Game over!')
    again = input('Would you like to play again? (Y/N) ').lower()
    if again == 'y':
        new_game()
    else:
        print('Thanks for playing!')


new_game()
