from flask import Flask, render_template, make_response, redirect, url_for, request
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
    return render_template('index.html')


@app.route('/choose')
def choose_house():
    char = request.args.get('character')
    response = make_response(render_template(
        'choose_house.html', houses=houses))
    response.set_cookie('selecting_char', char)
    return response


@app.route('/choose/<house>')
def choose_character(house):
    URL = 'https://hp-api.onrender.com/api/characters/house/' + house
    res = req.get(URL)
    characters = res.json()
    return render_template('choose_character.html', house=houses[house], characters=characters)


@app.route('/select/<id>')
def select(id):
    URL = 'https://hp-api.onrender.com/api/character/' + id
    res = req.get(URL)
    character = res.json()[0]
    print(character)
    response = make_response(redirect(url_for('home')))
    if request.cookies.get('selecting_char') == '1':
        response.set_cookie('char_1_name', character['name'])
        response.set_cookie('char_1_house', character['house'].lower())
    else:
        response.set_cookie('char_2_name', character['name'])
        response.set_cookie('char_2_house', character['house'].lower())
    response.delete_cookie('selecting_char')
    return response


@app.route('/clear')
def clear():
    response = make_response(redirect(url_for('home')))
    cookies = ['char_1_name', 'char_1_house', 'char_2_name', 'char_2_house']
    for cookie in cookies:
        response.delete_cookie(cookie)
    return response


if __name__ == '__main__':
    app.run(port=4000, debug=True)
