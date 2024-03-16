from flask import Flask, render_template
import requests as req

app = Flask(__name__)

posts = req.get("https://api.npoint.io/55b89ae739e1e708cb9f").json()[::-1]


@app.route('/')
def home():
    return render_template("index.html", blog_posts=posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/post/<int:id>')
def post(id):
    post = posts[-id]
    return render_template("post.html", post=post)


@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=4000)
