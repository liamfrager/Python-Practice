from flask import Flask, render_template, request
from projects import coding_projects
from dotenv import load_dotenv
import os
import smtplib

load_dotenv()
SMTP_PW = os.environ['GMAIL_PASSWORD']
SMTP_EMAIL = "liam.frager@gmail.com"

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', page='home', projects=coding_projects)


@app.route('/projects/<id>')
def projects(id):
    if id == 'all':
        return render_template('projects.html', page='projects', projects=coding_projects)
    else:
        return render_template('projects.html', page='projects', project=coding_projects[int(id)])


@app.route('/about')
def about():
    return render_template('about.html', page='about')


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template('contact.html', page='contact')
    else:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=SMTP_EMAIL, password=SMTP_PW)
            connection.sendmail(
                from_addr=request.form['email'],
                to_addrs=SMTP_EMAIL,
                msg=f"Subject:Message from your coding portfolio\n\n"
                f"From: {request.form['email']}\n"
                f"Subject: {request.form['subject']}\n"
                f"Message:\n{request.form['message']}".encode("UTF-8")
            )
        return render_template('contact.html', page='contact', sent=True)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
