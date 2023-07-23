from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config={"apiKey": "AIzaSyCXQJqsAAAiB3txmCv7v1YYiGF40tEE1po",
  "authDomain": "poli-fire-project.firebaseapp.com",
  "projectId": "poli-fire-project",
  "storageBucket": "poli-fire-project.appspot.com",
  "messagingSenderId": "373226364464",
  "appId": "1:373226364464:web:a641aef348b5024d0097f5",
  "measurementId": "G-SC7J6EX71J",
  "databaseURL":""}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method=="POST":
        mail=request.form["email"]
        passw=request.form["password"]
        print(mail,passw)
        try:
            login_session["user"]= auth.sign_in_with_email_and_password(mail,passw)
            print('logged in?')
            return redirect(url_for("add_tweet"))
        except Exception as e:
            error="Authentication failed"
            print(e)
    return render_template("signin.html")


@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method=="POST":
        mail=request.form["email"]
        passw=request.form["password"]
        try:
            login_session["user"]= auth.create_user_with_email_and_password(mail,passw)
            return redirect(url_for("add_tweet"))
        except:
            error="Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)