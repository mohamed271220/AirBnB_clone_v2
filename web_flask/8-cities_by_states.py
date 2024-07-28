#!/usr/bin/python3

"""initialize a flask web app
"""

from flask import Flask, render_template
from models.state import State
from models import storage

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    """teardown_db
    """
    storage.close()

@app.route('/cities_by_states', strict_slashes=False)
def states_list():
    """states_list
    """
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
