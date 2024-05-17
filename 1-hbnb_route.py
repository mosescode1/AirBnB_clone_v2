#!/usr/bin/env python3
from flask import Flask
#from web_flask import app

app = Flask(__name__)



@app.route("/", strict_slashes=False)
def home():
    return "Hello HBNB!"
if __name__ == "__main__":
    app.run(host='0.0.0.0')
