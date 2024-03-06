import pandas

# TODO 1. Create a dictionary in this format:
# nato_dict = {key: value for (index, row) in student_data_frame.iterrows()}
nato_data = pandas.read_csv('nato_phonetic_alphabet.csv')
nato_dict = {row.letter: row.code for (index, row) in nato_data.iterrows()}

# TODO 2. Create a list of the phonetic code words from a word that the user inputs.


def generate_phonetic():
    word = input("Type a word: ").upper()
    if word == "":
        return
    else:
        try:
            output = [nato_dict[letter] for letter in word]
        except KeyError:
            print("Sorry! Please only letters in the alphabet.")
        else:
            print(output)
    generate_phonetic()


generate_phonetic()
print("Good bye!")
