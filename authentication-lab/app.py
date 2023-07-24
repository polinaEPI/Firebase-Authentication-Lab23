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
  "databaseURL":"https://poli-fire-project-default-rtdb.europe-west1.firebasedatabase.app/"}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=="POST":
        mail=request.form["email"]
        passw=request.form["password"]
        name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
        try:
            print(0)
            login_session["user"]= auth.create_user_with_email_and_password(mail,passw)
            print(1)
            UID = login_session["user"]["localId"]
            print(2)
            user = {"email": mail, "full_name":name,"username":username,"bio":bio}
            print(3)
            db.child("Users").child(UID).set(user)
            print(4)
            return redirect(url_for("add_tweet"))
        except Exception as e:
            print(e)
            error="Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method=="POST":
        try:
            UID = login_session["user"]["localId"]
            tweet={"title":request.form["title"],"text":request.form["text"],"uid":UID}
            db.child('Tweets').push(tweet)
        except Exception as e:
            print(e)

    return render_template("add_tweet.html")


@app.route('/all_tweets')
def all_tweets():
    UID = login_session['user']['localId']
    tweets = db.child("Tweets").get().val()
    return render_template('tweets.html', tweets=tweets)

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))



if __name__ == '__main__':
    app.run(debug=True)