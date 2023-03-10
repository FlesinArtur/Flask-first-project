from datetime import datetime
import sqlite3

import flask
from flask import Flask, request
from markupsafe import escape
from flask import render_template


app = Flask(__name__)  # create Flask object

DATABASE_NAME = "messages.db"

with sqlite3.connect(DATABASE_NAME) as connection:
    cur = connection.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT,
    text TEXT
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
