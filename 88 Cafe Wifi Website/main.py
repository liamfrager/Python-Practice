from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('pages/home.html')


@app.route('/cafes')
def cafes():
    return render_template('pages/cafes.html')


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    return render_template('pages/add.html')


if __name__ == '__main__':
    app.run(port=4000, debug=True)
