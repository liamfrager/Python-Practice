from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        name = request.form["username"]
        pw = request.form["password"]
        return f"<h1>Name: {name}, Password: {pw}</h1>"


if __name__ == "__main__":
    app.run(debug=True, port=4000)
