#!/usr/bin/python3
from flask import Flask
"""Flask Initilization"""
# from web_flask import app

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    return "C {}".format(text.replace("_", " "))


@app.route("/python/<text>", strict_slashes=False)
def python_route(text="is cool"):
    return "Python {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
