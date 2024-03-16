from flask import Flask, render_template, request
import requests as req
import smtplib
import os

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

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


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    elif request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        email_message = f"Subject: Message from a blog visitor!\n\nName: {
            name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg=email_message
            )
        return render_template("contact.html", message_sent=True)


if __name__ == "__main__":
    app.run(debug=True, port=4000)
