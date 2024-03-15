from flask import Flask, render_template
from post import Post


app = Flask(__name__)

posts = Post().get_all_posts()


@app.route('/')
def home():
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def get_post(post_id):
    if 0 < post_id < len(posts):
        post = posts[post_id - 1]
        return render_template("post.html", post=post)
    else:
        return '404: Blog post not found.'


if __name__ == "__main__":
    app.run(debug=True)
