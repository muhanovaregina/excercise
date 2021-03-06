# -*- coding: utf-8 -*-

try:
    from os import getuid

except ImportError:
    def getuid():
        return 4000

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index2.html')#"Hello from Flask!"


if __name__ == "__main__":
    app.run(port=getuid() + 1000, debug=True)
