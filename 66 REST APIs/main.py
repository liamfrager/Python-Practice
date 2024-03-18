from dataclasses import dataclass
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random as rand
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_API_KEY = os.environ["API_KEY"]


app = Flask(__name__)

# CREATE DB


class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
@dataclass
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    with app.app_context():
        all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
        random_cafe = jsonify(rand.choice(all_cafes))
        return random_cafe, 200


@app.route("/all")
def get_all_cafes():
    with app.app_context():
        all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
        return jsonify({
            "cafes": all_cafes
        }), 200


@app.route("/search")
def get_cafe():
    loc = request.args.get('loc')
    with app.app_context():
        cafes = db.session.execute(db.select(Cafe).where(
            Cafe.location == loc)).scalars().all()
        if cafes:
            return jsonify({
                "cafes": cafes
            }), 200
        else:
            return jsonify({
                "error": {
                    "Not Found": "Sorry, we don't have a cafe at that location."
                }
            }), 404

# HTTP POST - Create Record


@app.route("/add", methods=["POST"])
def add_cafe():
    data = request.form
    try:
        with app.app_context():
            new_cafe = Cafe(
                can_take_calls=bool(data["can_take_calls"]),
                coffee_price=data["coffee_price"],
                has_sockets=bool(data["has_sockets"]),
                has_toilet=bool(data["has_toilet"]),
                has_wifi=bool(data["has_wifi"]),
                img_url=data["img_url"],
                location=data["location"],
                map_url=data["map_url"],
                name=data["name"],
                seats=data["seats"]
            )
            db.session.add(new_cafe)
            db.session.commit()
            return jsonify({
                "response": {
                    "success": "Successfully added the new cafe."
                }
            }), 201
    except Exception as error:
        return jsonify({
            "error": {
                type(error).__name__: str(error).replace(f"(sqlite3.{type(error).__name__}) ", "").split("\n")[0],
            }
        }), 400


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update(cafe_id):
    new_price = request.args.get('new_price')
    try:
        with app.app_context():
            cafe = db.get_or_404(Cafe, cafe_id)
            cafe.coffee_price = new_price
            db.session.commit()
            return jsonify({
                "success": "Successfully updated the price."
            }), 200
    except Exception as error:
        return jsonify({
            "error": {
                type(error).__name__: f"There is no cafe with id: {cafe_id}",
            }
        }), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == SECRET_API_KEY:
        try:
            with app.app_context():
                cafe = db.get_or_404(Cafe, cafe_id)
                db.session.delete(cafe)
                db.session.commit()
                return jsonify({
                    "success": "Successfully deleted cafe."
                }), 200
        except Exception as error:
            return jsonify({
                "error": {
                    type(error).__name__: f"There is no cafe with id: {cafe_id}",
                }
            }), 404
    else:
        return jsonify({
            "error": {
                "Forbidden": "You are not authorized to delete cafes. Make sure you have the correct api-key.",
            }
        }), 403


if __name__ == '__main__':
    app.run(debug=True, port=4000)
