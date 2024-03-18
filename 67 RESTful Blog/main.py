from flask import Flask, render_template, redirect, url_for, Blueprint
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)


# CREATE FORM
class CreatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    with app.app_context():
        posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)


# TODO: Add a route so that you can click on individual posts.
@app.route('/post/<post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    with app.app_context():
        requested_post = db.session.execute(
            db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/add', methods=["GET", "POST"])
def add_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        with app.app_context():
            new_post = BlogPost(
                title=form.title.data,
                subtitle=form.subtitle.data,
                date=date.today().strftime('%B %-d, %Y'),
                body=form.body.data,
                author=form.author.data,
                img_url=form.img_url.data,
            )
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for('get_all_posts'))
    else:
        return render_template("make-post.html", form=form)


# TODO: edit_post() to change an existing blog post
@app.route('/edit/<post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    with app.app_context():
        post = db.session.execute(
            db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
        form = CreatePostForm(
            title=post.title,
            subtitle=post.subtitle,
            img_url=post.img_url,
            author=post.author,
            body=post.body
        )
        if form.validate_on_submit():
            post.title = form.title.data
            post.subtitle = form.subtitle.data
            post.body = form.body.data
            post.author = form.author.data
            post.img_url = form.img_url.data
            db.session.commit()
            return redirect(url_for('show_post', post_id=post.id))
        else:
            return render_template("make-post.html", form=form, is_edit=True)


# TODO: delete_post() to remove a blog post from the database
@app.route('/delete/<post_id>')
def delete_post(post_id):
    with app.app_context():
        requested_post = db.session.execute(
            db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
        db.session.delete(requested_post)
        db.session.commit()
    return redirect(url_for('get_all_posts'))

# Below is the code from previous lessons. No changes needed.


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=4000)
