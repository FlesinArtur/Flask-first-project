from flask import Flask
from markupsafe import escape
from flask import render_template


app = Flask(__name__)  # create Flask object


@app.route("/hello")
def hello():
    return render_template("hello.html")


@app.route("/info/<int:id>/")
def info(id):
    return f"info {escape(id)}"


@app.route("/api/version/")
def version():
    return {'version': '0.1'}


@app.route("/chat/")
def chat():
    pass
