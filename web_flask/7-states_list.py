#!/usr/bin/python3
"""
Script that starts a Flask web application:
   - Routes:
      - /states_list: display an HTML page: (inside the tag BODY)
      - H1 tag: "States"
          - UL tag: with the list of all State objects present in
              DBStorage sorted by name (A->Z) tip
          - LI tag: description of one State: <state.id>:
              <B><state.name></B>
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/states_list')
def fetch_states():
    """ Fetch all states and display on html page """
    states = storage.all(State)
    return render_template('7-states_list.html', state_objs=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
