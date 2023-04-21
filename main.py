from flask import Flask, render_template, request
import requests
import datetime as dt
import smtplib
import os

blog_data = requests.get(url="https://api.npoint.io/831d110784808fb11ca1").json()

all_blogs = [blog for blog in blog_data]

current_year = dt.datetime.now().year

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', blogs=all_blogs, year=current_year)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_num = request.form['phone_num']
        message = request.form['message']
        send_email(name, email, phone_num, message)
        return render_template('contact.html', received=True)
    return render_template('contact.html', received=False)


def send_email(name, email, phone_num, msg):
    email_msg = f"Subject:New Message\n\n" \
                f"Name: {name}\n" \
                f"Email: {email}\n" \
                f"Phone Number: {phone_num}\n" \
                f"Message: {msg}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(os.environ.get("MY_EMAIL"), os.environ.get("MY_APP_PW"))
        connection.sendmail(os.environ.get("MY_EMAIL"),os.environ.get("MY_EMAIL"), msg=email_msg)


@app.route('/<int:id>')
def blog_post(id):
    chosen_blog = None
    for blog in all_blogs:
        if blog['id'] == id:
           chosen_blog = blog
    return render_template('post.html', blog=chosen_blog, year=current_year)


if __name__ == "__main__":
    app.run(debug=True)