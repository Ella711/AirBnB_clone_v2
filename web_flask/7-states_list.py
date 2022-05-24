#!/usr/bin/python3
"""Task7 - states list"""

from flask import Flask, render_template
from models import *
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    route /states_list (Objects State)
    """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def storage_close(exception):
    '''
    teardown close
    '''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
