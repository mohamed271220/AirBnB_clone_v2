#!/usr/bin/python3

"""initialize a flask web app
"""

from flask import Flask, render_template


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


@app.route('/number_template/<int:n>')
def number_template(n):
    """
    number_template:
        n: integer
    return a html template
    """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>')
def number_odd_or_even(n):
    """
    number_odd_or_even:
        n: integer
    return a html template
    """
    if n % 2 == 0:
        return render_template('6-number_odd_or_even.html',
                               n=n, odd_even='even')
    else:
        return render_template('6-number_odd_or_even.html',
                               n=n, odd_even='odd')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
