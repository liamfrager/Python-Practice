from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import sqlite3

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=DeclarativeBase)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)


class Book(db.Model):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    author: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)


with app.app_context():
    db.create_all()

# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# cursor.execute(
#     "CREATE TABLE books ( \
#         id INTEGER PRIMARY KEY, \
#         title varchar(250) NOT NULL UNIQUE, \
#         author varchar(250) NOT NULL, \
#         rating FLOAT NOT NULL \
#     )"
# )
# cursor.execute(
#     f"INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')"
# )
# db.commit()


@app.route('/')
def home():
    return render_template('index.html', books=all_books)


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template('add.html')
    elif request.method == "POST":
        data = dict(request.form)
        return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True, port=4000)
