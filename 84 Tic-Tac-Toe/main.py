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

    def refresh_display(*args):
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
        print(args[0] if args else '')

    def is_winning_move(move):
        rows = ['123', '456', '789', '147', '258', '369', '159', '357']
        for row in rows:
            if move in row:
                spaces = [*row]
                if _[spaces[0]] == _[spaces[1]] and _[spaces[1]] == _[spaces[2]]:
                    return True
        return False

    player = 1
    valid_moves = 9
    refresh_display()
    while True:
        try:
            move = str(
                int(input(f'{'X' if player > 0 else 'O'}, where would you like to go?: ')))
        except:
            refresh_display('Not a valid move. Try again.')
            continue
        if move in board:
            _[move] = 'X' if player > 0 else 'O'
            player *= -1
            valid_moves -= 1
        else:
            refresh_display('Not a valid move. Try again.')
            continue
        if valid_moves == 0 or is_winning_move(move):
            break
        refresh_display()

    refresh_display()
    print(f'Game over! {('X wins!' if player < 0 else 'O wins!')
          if is_winning_move(move) else "It's a draw!"}')
    again = input('Would you like to play again? (Y/N) ').lower()
    if again == 'y':
        new_game()
    else:
        print('Thanks for playing!')


new_game()
