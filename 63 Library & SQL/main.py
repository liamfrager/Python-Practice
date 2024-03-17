from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import sqlite3

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
db.init_app(app)


class Book(db.Model):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


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


def get_all_books():
    try:
        with app.app_context():
            result = db.session.execute(db.select(Book).order_by(Book.title))
            return result.scalars().all()
    except:
        return None


def get_book_with_id(id):
    try:
        with app.app_context():
            result = db.session.execute(db.select(Book).where(Book.id == id))
            return result.scalar()
    except:
        return None


def delete_book_with_id(id):
    try:
        result = db.session.execute(db.select(Book).where(Book.id == id))
        book = result.scalar()
        db.session.delete(book)
        db.session.commit()
        return True
    except:
        return False


@app.route('/')
def home():
    get_all_books()
    return render_template('index.html', books=get_all_books())


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template('add.html')
    elif request.method == "POST":
        try:
            data = dict(request.form)
            with app.app_context():
                new_book = Book(
                    title=data['title'],
                    author=data['author'],
                    rating=data['rating']
                )
                db.session.add(new_book)
                db.session.commit()
            return redirect('/')
        except:
            return render_template('add.html', form=request.form, error=True)


@app.route('/edit/<id>', methods=["GET", "POST"])
def edit(id):
    if request.method == "GET":
        book = get_book_with_id(id)
        if book:
            return render_template('edit.html', book=book)
        else:
            return render_template('404.html', id=id)
    elif request.method == "POST":
        try:
            with app.app_context():
                result = db.session.execute(
                    db.select(Book).where(Book.id == id))
                book = result.scalar()
                print(request.form)
                book.rating = request.form['new_rating']
                db.session.commit()
            return redirect('/')
        except:
            return render_template('edit.html', book=get_book_with_id(id), error=True)


@app.route('/delete/<id>')
def delete(id):
    delete_book_with_id(id)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, port=4000)
