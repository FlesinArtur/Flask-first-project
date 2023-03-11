from datetime import datetime
import sqlite3

import flask
from flask import Flask, request
from markupsafe import escape
from flask import render_template


app = Flask(__name__)  # create Flask object

DATABASE_NAME = "my_database.db"

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


def get_users(filename: str = DATABASE_NAME):
    with sqlite3.connect(filename) as connection:
        cur = connection.cursor()
        table_data = cur.execute("SELECT * FROM users").fetchall()
        users = {}
        for user_id, username, password in table_data:
            users[username] = password
    return users


def login(username: str, password: str):
    users = get_users()
    if users.get(f'{username}') == f'{password}':
        return True
    else:
        return False


@app.route("/registration/", methods=['GET', 'POST'])
def registration(filename: str = DATABASE_NAME):
    username = request.form.get('username')
    password = request.form.get('password')
    repeat_password = request.form.get('repeat_password')
    if password == repeat_password and password is not None:
        with sqlite3.connect(filename) as connection:
            cur = connection.cursor()
            cur.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, password))
            connection.commit()
            return render_template('admin.html')
    return render_template('registration.html')


@app.route("/hello")
def hello():
    return render_template("hello.html")


@app.route("/info/<int:my_id>/")
def info(my_id):
    return f"info: {escape(my_id)}"


@app.route("/api/version/")
def version():
    return {'version': '0.1'}


@app.route("/chat/", methods=['GET', 'POST'])
def chat():
    if flask.request.method == 'GET':
        return render_template("chat.html", messages=get_messages())
    else:
        text = request.form.get('message')
        create_message(text)
        return render_template("chat.html", messages=get_messages())


@app.route("/admin/", methods=['GET', 'POST'])
def admin():
    username = request.form.get('username')
    password = request.form.get('password')
    if login(username, password):
        return render_template("admin.html")
    return render_template('login.html')
