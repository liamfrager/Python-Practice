from flask import Flask, render_template
import datetime as dt
import requests as req

app = Flask(__name__)


@app.route('/')
def home():
    this_year = dt.datetime.now().year
    return render_template("index.html", this_year=this_year)


@app.route('/guess/<name>')
def guess(name):
    res = req.get(f"https://api.genderize.io/?name={name}")
    gender = res.json()["gender"]
    res = req.get(f"https://api.agify.io/?name={name}")
    age = res.json()["age"]
    return render_template("guess.html", name=name.title(), gender=gender, age=age)


if __name__ == "__main__":
    app.run(debug=True)
