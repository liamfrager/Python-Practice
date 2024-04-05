from typing import List
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy import ForeignKey, Integer, String, Time, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class DB():
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id: Mapped[int] = mapped_column(Integer, primary_key=True)
        email: Mapped[str] = mapped_column(String(100), unique=True)
        password: Mapped[str] = mapped_column(String(100))
        name: Mapped[str] = mapped_column(String(1000))
        list_items: Mapped[List["DB.ListItem"]] = relationship(
            back_populates="user")

    class ListItem(db.Model):
        __tablename__ = 'cafes'
        id: Mapped[int] = mapped_column(Integer, primary_key=True)
        text: Mapped[str] = mapped_column(String(100), unique=True)
        due_date: Mapped[datetime.time] = mapped_column(Time)
        is_completed: Mapped[bool] = mapped_column(Boolean)
        tags: Mapped[str] = mapped_column(String(16))
        user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
        user: Mapped["DB.User"] = relationship(
            back_populates="list_items")

    def get_user(**kwargs):
        if 'id' in kwargs:
            user = db.session.execute(
                db.select(DB.User).where(DB.User.id == kwargs['id'])).scalar()
        elif 'email' in kwargs:
            user = db.session.execute(
                DB.User.query.filter(DB.User.email == kwargs['email'])).scalar()
        return user

    def add_user(self, form_data):
        new_user = DB.User(
            email=form_data['email'],
            password=generate_password_hash(
                password=form_data['password'],
                method='pbkdf2:sha256',
                salt_length=8
            ),
            name=form_data['name']
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user


database = DB()
