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

        return redirect('/')
    return render_template('login.html', message='Wrong password!')



if __name__ == '__main__':
    app.run()
