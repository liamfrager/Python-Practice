from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
def home():
    houses = {
        'gryffindor': {'name': 'Gryffindor', 'img': 'https://static.wikia.nocookie.net/pottermore/images/1/16/Gryffindor_crest.png', 'qualities': ['courageous', 'brave', 'determined'], 'colors': ['firebrick', 'gold']},
        'ravenclaw': {'name': 'Ravenclaw', 'img': 'https://static.wikia.nocookie.net/pottermore/images/4/4f/Ravenclaw_crest.png', 'qualities': ['wise', 'witty', 'observant'], 'colors': ['deepskyblue', 'sienna']},
        'hufflepuff': {'name': 'Hufflepuff', 'img': 'https://static.wikia.nocookie.net/pottermore/images/5/5e/Hufflepuff_crest.png', 'qualities': ['loyal', 'humble', 'patient'], 'colors': ['gold', 'black']},
        'slytherin': {'name': 'Slytherin', 'img': 'https://static.wikia.nocookie.net/pottermore/images/4/45/Slytherin_Crest.png', 'qualities': ['ambitious', 'cunning', 'proud'], 'colors': ['forestgreen', 'silver']},
    }
    return render_template('index.html', houses=houses)


@app.route('/<house>')
def house(house):
    return render_template('house.html', house=house)


if __name__ == '__main__':
    app.run(port=4000, debug=True)
