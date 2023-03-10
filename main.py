from datetime import datetime
import sqlite3

from flask import Flask, request
from markupsafe import escape
from flask import render_template


app = Flask(__name__)  # create Flask object
DATABASE_NAME = "messages.db"


def create_table(filename: str):
    with sqlite3.connect(filename) as connection:
        cur = connection.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT,
        text TEXT
        )""")


def create_message(text: str, filename: str):
    with sqlite3.connect(filename) as connection:
        cur = connection.cursor()
        created_at = str(datetime.now().strftime("%H:%M"))
        cur.execute("INSERT INTO messages(created_at, text) VALUES(?,?)", (created_at, text))
        connection.commit()


def get_messages(filename: str):
    with sqlite3.connect(filename) as connection:
        cur = connection.cursor()
        table_data = cur.execute("SELECT * FROM messages").fetchall()
        messages = []
        for tuple_ in table_data:
            message_id, created_at, text = tuple_
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
    return f"info {escape(my_id)}"


@app.route("/api/version/")
def version():
    return {'version': '0.1'}


@app.route("/chat/", methods=['GET', 'POST'])
def chat():
    create_table(DATABASE_NAME)
    if request.form.get('message') == '' or request.form.get('message') is None:
        return render_template("chat.html", messages='')
    text = request.form.get('message')
    create_message(text, DATABASE_NAME)
    messages = get_messages(DATABASE_NAME)
    return render_template("chat.html", messages=messages)
