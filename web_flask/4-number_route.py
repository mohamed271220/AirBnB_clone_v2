#!/usr/bin/python3

"""initialize a flask web app
"""

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/')
def home():
    """return a string
    """
    return "Hello HBNB!"

@app.route('/hbnb')
def hbnb():
    """return a string
    """
    return "HBNB"

@app.route('/c/<text>')
def c_params(text):
    """return a string
    """
    return "C {}".format(text.replace("_", " "))

@app.route('/python/', defaults={'text': 'is cool'})
@app.route('/python/<text>')
def python_params(text):
    """
    python_params:
        text: string
    return a string
    """
    return "Python {}".format(text.replace("_", " "))

@app.route('/number/<int:n>')
def number_params(n):
    """
    number_params:
        n: integer
    return a string
    """
    return "{} is a number".format(n)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
