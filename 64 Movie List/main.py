from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os
import requests as req


load_dotenv()
BEARER_TOKEN = os.environ["BEARER_TOKEN"]
MOVIE_API_URL = "https://api.themoviedb.org/3"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie-rankings.db"
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), nullable=False, unique=True)
    year: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String, nullable=True)
    img_url: Mapped[str] = mapped_column(String, nullable=False)


with app.app_context():
    db.create_all()


# Forms
class MovieSearchForm(FlaskForm):
    query = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


class MovieEditForm(FlaskForm):
    rating = StringField(
        label="Your rating out of 10 e.g. 7.5",
        validators=[DataRequired()]
    )
    review = StringField(
        label="Your review",
        validators=[DataRequired()]
    )
    submit = SubmitField("Add Movie")


# ROUTES
@app.route("/")
def home():
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.rating))
        movies = result.scalars().all()
        for i in range(len(movies)):
            movies[i].ranking = len(movies) - i
    return render_template("index.html", movies=movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = MovieSearchForm()
    # Searched for movie
    if form.validate_on_submit():
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }
        params = {
            'query': form.query.data
        }
        res = req.get(
            url=f"{MOVIE_API_URL}/search/movie",
            headers=headers,
            params=params
        )
        movies = res.json()['results']
        return render_template("add.html", movies=movies)
    else:
        # Get selected movie details
        if request.args.get('id'):
            movie_id = request.args.get('id')
            headers = {
                "Authorization": f"Bearer {BEARER_TOKEN}",
                "accept": "application/json",
            }
            params = {
                "language": "en-US",
            }
            res = req.get(
                url=f"{MOVIE_API_URL}/movie/{movie_id}",
                headers=headers,
                params=params
            )
            details = res.json()
            try:
                with app.app_context():
                    new_movie = Movie(
                        id=details['id'],
                        title=details['title'],
                        img_url=details['poster_path'],
                        year=details['release_date'],
                        description=details['overview'],
                    )
                    db.session.add(new_movie)
                    db.session.commit()
                    return redirect(url_for('edit', movie_id=details['id']))
            except IntegrityError:
                error = f"Could not add {details['title']} to your movie list.\n \
                    Perhaps it's already on your list?"
                return render_template("error.html", error=error)
        else:
            # Display search form
            return render_template("add.html", form=form)


@app.route("/edit/<movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    form = MovieEditForm()
    with app.app_context():
        result = db.session.execute(
            db.select(Movie).where(Movie.id == movie_id))
        movie = result.scalar()
    if form.validate_on_submit():
        with app.app_context():
            movie_to_change = db.session.execute(
                db.select(Movie).where(Movie.id == movie_id)).scalar()
            movie_to_change.rating = form.rating.data
            movie_to_change.review = form.review.data
            db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template("edit.html", movie=movie, form=form)


@app.route("/delete/<movie_id>")
def delete(movie_id):
    result = db.session.execute(
        db.select(Movie).where(Movie.id == movie_id))
    movie = result.scalar()
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)
