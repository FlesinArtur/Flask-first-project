from flask import Flask, request
from markupsafe import escape
from flask import render_template
from datetime import datetime


app = Flask(__name__)  # create Flask object
message = []


def create_message():
    user_id = 0
    created_at = datetime.now().time()
    text = request.form.get('message')
    message.append({
        'id': user_id,
        'created_at': created_at,
        'text': text
    })
    return message


@app.route("/hello")
def hello():
    return render_template("hello.html")


@app.route("/info/<int:id>/")
def info(id):
    return f"info {escape(id)}"


@app.route("/api/version/")
def version():
    return {'version': '0.1'}


@app.route("/chat/", methods=['GET', 'POST'])
def chat():
    if request.form.get('message') == None:
        return render_template("chat.html", message="None")
    message = create_message()
    return render_template("chat.html", message=message)
