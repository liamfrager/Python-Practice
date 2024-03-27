from art import logo
from dictionary import dictionary
from os import system, name

# define our clear function


def clear_console():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def get_input():
    # INPUT
    print(logo)
    input_ = input(
        'What would you like to say in Morse Code?: ').lower().strip()
    output = ""
    for char in input_:
        if char == " ":
            output += "\n"
        else:
            output += dictionary[char] + "  "

    input_ = input_.split()
    output = output.split('\n')

    # OUTPUT
    clear_console()
    print(logo)
    print('\nHere is your message in Morse Code:\n')
    for i in range(len(output)):
        print(input_[i].upper())
        print(f'   {output[i]}')

    again = input(
        '\nWould you like to translate another phrase? (Y/N) ').lower()
    if again == 'y':
        clear_console()
        get_input()
    else:
        print('Good bye!')


get_input()
