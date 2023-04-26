from datetime import datetime
import sqlite3

import flask
from flask import Flask, request, session, flash, redirect, url_for, make_response

from markupsafe import escape
from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash

from secret import SECRET_KEY

app = Flask(__name__)  # create Flask object
app.secret_key = SECRET_KEY
DATABASE_NAME = "my_database.db"
USER_LOGIN = False

# DATABASE :

with sqlite3.connect(DATABASE_NAME) as connection:
    cur = connection.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT,
    text TEXT
    )""")

with sqlite3.connect(DATABASE_NAME) as connection:
    cur = connection.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
    )""")


def create_message(text: str, filename: str = DATABASE_NAME):
    with sqlite3.connect(filename) as connection:
        cur = connection.cursor()
        created_at = str(datetime.now().strftime("%H:%M"))
        if text != '':
            cur.execute("INSERT INTO messages(created_at, text) VALUES(?,?)", (created_at, text))
            connection.commit()


def get_messages(filename: str = DATABASE_NAME) -> list:
    with sqlite3.connect(filename) as connection:
        cur = connection.cursor()
        table_data = cur.execute("SELECT * FROM messages").fetchall()
        messages = []
        for message_id, created_at, text in table_data:
            messages.append({
                'message_id': message_id,
                'created_at': created_at,
                'text': text
            })
    return messages


def get_users(filename: str = DATABASE_NAME) -> list:
    with sqlite3.connect(filename) as connection:
        cur = connection.cursor()
        table_data = cur.execute("SELECT * FROM users").fetchall()
        users = []
        for user_id, username, password in table_data:
            users.append({username: password, 'user_id': user_id})
    return users


def write_user(username: str, password: str, filename: str = DATABASE_NAME):
    with sqlite3.connect(filename) as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
        connection.commit()


def create_session(user_id) -> session:
    session['user_id'] = user_id
    session.modified = True
    return session


# authorization :


@app.before_request
def check_user_login():
    try:
        users = get_users()
        for user in users:
            if user['user_id'] in session:
                globals()['USER_LOGIN'] = True
                return redirect(url_for('admin'))
    except KeyError:
        pass


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = get_users()
        username = request.form.get('username')
        password = request.form.get('password')
        for user in users:
            try:
                if check_password_hash(user[username], password):
                    globals()['USER_LOGIN'] = True
                    create_session(user['user_id'])
                    return redirect(url_for('admin'))
            except KeyError:
                continue
    return render_template('login.html')


@app.route("/registration/", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        if password == repeat_password and len(password) > 5 and password is not None:
            write_user(username, generate_password_hash(password))
            return redirect(url_for('login'))
        flash('The form is filled out incorrectly or the password is not secure')
    return render_template('registration.html')


@app.route("/admin/", methods=['GET', 'POST'])
def admin():
    if globals()['USER_LOGIN']:
        return render_template("admin.html")
    return redirect(url_for('login'))


@app.route("/logout/", methods=['GET', 'POST'])
def logout():
    globals()['USER_LOGIN'] = False
    session.clear()
    return redirect(url_for('admin'))


# Chat :


@app.route("/chat/", methods=['GET', 'POST'])
def chat():
    if flask.request.method == 'GET':
        return render_template("chat.html", messages=get_messages())
    else:
        text = request.form.get('message')
        create_message(text)
        return render_template("chat.html", messages=get_messages())


# Other :


@app.route("/set_cookies/", methods=['GET', 'POST'])
def set_cookies():
    response = make_response(render_template("cookies.html"))
    response.set_cookie('time', str(datetime.now().strftime("%H:%M")))
    return response


@app.route("/get_cookies/", methods=['GET'])
def get_cookies():
    cookie = request.cookies
    return render_template('cookies.html', cookie=cookie)


@app.route("/hello")
def hello():
    return render_template("hello.html")


@app.route("/info/<int:my_id>/")
def info(my_id):
    return f"info: {escape(my_id)}"


@app.route("/api/version/")
def version():
    return {'version': '0.1'}
