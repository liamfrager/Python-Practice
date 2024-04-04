from typing import List
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy import ForeignKey, Integer, String, Time, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from bs4 import BeautifulSoup
import requests as req


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    cafes_added: Mapped[List["Cafe"]] = relationship(
        back_populates="added_by")


class Cafe(db.Model):
    __tablename__ = 'cafes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    url: Mapped[str] = mapped_column(String(100))
    open_time: Mapped[datetime.time] = mapped_column(Time)
    close_time: Mapped[datetime.time] = mapped_column(Time)
    coffee_rating: Mapped[int] = mapped_column(Integer)
    wifi_rating: Mapped[int] = mapped_column(Integer)
    outlet_rating: Mapped[int] = mapped_column(Integer)
    added_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    added_by: Mapped["User"] = relationship(
        back_populates="cafes_added")


class DatabaseFunctions():
    def get_user(*args, **kwargs):
        if kwargs['id']:
            user = db.session.execute(
                db.select(User).where(User.id == kwargs['id'])).scalar()
        elif kwargs['email']:
            user = db.session.execute(
                User.query.filter(User.email == kwargs['email'])).scalar()
        return user

    def add_user(self, form_data):
        new_user = User(
            email=form_data['email'],
            password=generate_password_hash(
                password=form_data['password'],
                method='pbkdf2:sha256',
                salt_length=8
            ),
            name=form_data['name'],
        )
        db.session.add(new_user)
        db.session.commit()

    def get_all_cafes(self):
        return Cafe.query.all()

    def get_cafe(self, cafe_id):
        cafe = Cafe.query.filter(Cafe.id == cafe_id).scalar()
        return self.scrape_cafe_data(cafe)

    def get_user_cafes(self, user_id):
        cafes = db.session.execute(Cafe.query.filter(
            Cafe.added_by_id == user_id)).scalars()
        return cafes

    def add_cafe(self, form_data, user_id):
        new_cafe = Cafe(
            name=form_data['name'],
            url=form_data['url'],
            open_time=form_data['open_time'],
            close_time=form_data['close_time'],
            coffee_rating=0 if form_data['coffee_rating'] == '❌' else len(
                form_data['coffee_rating']),
            wifi_rating=0 if form_data['wifi_rating'] == '❌' else len(
                form_data['wifi_rating']),
            outlet_rating=0 if form_data['outlet_rating'] == '❌' else len(
                form_data['outlet_rating']),
            added_by_id=user_id
        )
        db.session.add(new_cafe)
        db.session.commit()

    def scrape_cafe_data(self, cafe):
        cafe.stats = [
            {'name': '☕️', 'rating': cafe.coffee_rating},
            {'name': '🛜', 'rating': cafe.wifi_rating},
            {'name': '🔌', 'rating': cafe.outlet_rating}
        ]
        try:
            res = req.get(cafe.url)
            html = res.text
            soup = BeautifulSoup(html, "html.parser")
            cafe.menu_link = self.get_menu_link(soup)
            cafe.images = self.get_images(soup)
            print(cafe.images)
        finally:
            return cafe

    def get_menu_link(self, soup):
        try:
            menu_btn = soup.find('a', text='Menu')
            return menu_btn['href']
        except:
            return None

    def get_images(self, soup):
        try:
            imgs = soup.find_all('img')
            print([img['src'] for img in imgs])
            return [img['src'] for img in imgs]
        except:
            return None


db_func = DatabaseFunctions()
