from flask import Flask
from flask import url_for
from markupsafe import escape
from flask import make_response
from flask import render_template


app = Flask(__name__)  # create Flask object


@app.route("/hello")
def hello_world():
    return render_template("hello.html")


