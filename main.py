from flask import Flask, request
from markupsafe import escape
from flask import render_template
from datetime import datetime


app = Flask(__name__)  # create Flask object
MESSAGES = []
MESSAGE_ID = 0


def create_message(text):
    message_id = 0
    created_at = str(datetime.now().strftime("%H:%M"))
    MESSAGES.append({
        'id': message_id,
        'created_at': created_at,
        'text': text
    })


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
    if request.form.get('message') == '' or request.form.get('message') is None:
        return render_template("chat.html", messages='')
    text = request.form.get('message')
    create_message(text)
    return render_template("chat.html", messages=MESSAGES)


if __name__ == '__main__':
    app.run(debug=True)
