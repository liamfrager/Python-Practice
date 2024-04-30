from flask import Flask, render_template, redirect
import requests as req

app = Flask(__name__)

houses = {
    'gryffindor': {'name': 'Gryffindor', 'img': 'https://static.wikia.nocookie.net/pottermore/images/1/16/Gryffindor_crest.png', 'qualities': ['courageous', 'brave', 'determined']},
    'ravenclaw': {'name': 'Ravenclaw', 'img': 'https://static.wikia.nocookie.net/pottermore/images/4/4f/Ravenclaw_crest.png', 'qualities': ['wise', 'witty', 'observant']},
    'hufflepuff': {'name': 'Hufflepuff', 'img': 'https://static.wikia.nocookie.net/pottermore/images/5/5e/Hufflepuff_crest.png', 'qualities': ['loyal', 'humble', 'patient']},
    'slytherin': {'name': 'Slytherin', 'img': 'https://static.wikia.nocookie.net/pottermore/images/4/45/Slytherin_Crest.png', 'qualities': ['ambitious', 'cunning', 'proud']},
}


@app.route('/')
def home():
    return render_template('index.html', houses=houses)


@app.route('/<house>')
def house(house):
    URL = 'https://hp-api.onrender.com/api/characters/house/' + house
    res = req.get(URL)
    characters = res.json()
    return render_template('house.html', house=houses[house], characters=characters)


@app.route('/character/<id>')
def character(id):
    URL = 'https://hp-api.onrender.com/api/character/' + id
    res = req.get(URL)
    character = res.json()[0]
    return render_template('character.html', character=character)


if __name__ == '__main__':
    app.run(port=4000, debug=True)
