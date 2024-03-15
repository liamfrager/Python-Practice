from flask import Flask

app = Flask(__name__)


def bold(func):
    def wrap():
        return f"<b>{func()}</b>"
    return wrap


def italic(func):
    def wrap():
        return f"<em>{func()}</em>"
    return wrap


def underline(func):
    def wrap():
        return f"<u>{func()}</u>"
    return wrap


@app.route('/')
@bold
@italic
def hello_world():
    return 'Hello, World!'


@app.route('/test')
def test():
    return 'Test'


if __name__ == "__main__":
    app.run(debug=True)
