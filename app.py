import data
import bcrypt as bcrypt
from flask import Flask, render_template, request, redirect, session, make_response
import datetime

app = Flask(__name__)
app.secret_key = 'ad45iremsad123'

def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def is_loggedin():

    return 'user_email' in session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')

    email = request.form.get('email')
    is_user_email = email in data.users
    if not is_user_email:
        return render_template('login.html', message = 'Invalid login attempt')
    #
    password = request.form.get('password')
    if verify_password(password, data.users[email]):
        session["user_email"] = email
        session["points"] = 0
        session["question_count"] = 0
        return redirect('/')
    return render_template('login.html', message='Wrong password!')


@app.route('/logout')
def logout():
    session.pop("user_email", None)
    session.pop("points", None)
    session.pop("question_count", None)
    return redirect('/login')

@app.route('/test', methods=["GET", "POST"])
def test():
    if not is_loggedin():
        return redirect('/login')
    if session["question_count"] >= len(data.questions.items()):
        return redirect('/result')
    question = list(data.questions.items())[session["question_count"]]
    if request.method == "GET":
        return render_template('test.html', question=question)
    answers = list(question[1].items())
    answer = request.form.get("answer")
    answer = int(answer)
    session["question_count"] += 1
    if answers[answer][1]:
        session["points"] += 1
    return redirect('/test')


@app.route('/result')
def result():
    if not is_loggedin():
        return redirect('/login')
    return render_template('result.html')


if __name__ == '__main__':
    app.run()
