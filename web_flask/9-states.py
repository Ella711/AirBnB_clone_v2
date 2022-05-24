#!/usr/bin/python3
# Script that starts a Flask web application:
#   - Your web application must be listening on 0.0.0.0, port 5000
#   - /cities_by_states: display an HTML page: (inside the tag BODY)
#       - H1 tag: "States"
#       - UL tag: with the list of all State objects present in DBStorage
#           sorted by name (A->Z) tip
#           - LI tag: description of one State: <state.id>:
#               <B><state.name></B>
#               + UL tag: with the list of City objects linked to the
#                   State sorted by name (A->Z)
#               - LI tag: description of one City: <city.id>:
#                   <B><city.name></B>


from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_route():
    """ Display text """
    return 'Hello HBNB!'


@app.route('/hbnb')
def display_hbnb():
    """ Display text """
    return 'HBNB'


@app.route('/c/<text>')
def display_ctext(text):
    """ Display C text """
    return "C {}".format(text.replace("_", " "))


@app.route('/python')
@app.route('/python/<text>')
def python_text(text="is cool"):
    """ Display Python text with a default of 'is cool' """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>')
def n_int(n):
    """ Display n only if it's an int """
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>')
def html_if_int(n):
    """ Display html page only if n is int """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>')
def even_or_odd(n):
    """ Display html page only if n is int """
    if n % 2 == 0:
        even_odd = "even"
    else:
        even_odd = "odd"
    return render_template('6-number_odd_or_even.html', n=n, even_odd=even_odd)


@app.teardown_appcontext
def teardown(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/states')
@app.route('/states_list')
def fetch_states():
    """ Fetch all states and display on html page """
    state_objs = []
    for states in storage.all(State).values():
        state_objs.append(states)
    return render_template('7-states_list.html', state_objs=state_objs)


@app.route('/cities_by_states')
def fetch_cities_by_states():
    """ Fetch all states and display on html page """
    state_objs = []
    for states in storage.all(State).values():
        state_objs.append(states)
    return render_template('8-cities_by_states.html', state_objs=state_objs)


@app.route('/states/<id>')
def fetch_a_state(id):
    """
    Fetch the state that matches that id and display on html page
    """
    state_obj = None
    for state in storage.all(State).values():
        if state.id == id:
            state_obj = state
    return render_template('9-states.html', state_obj=state_obj)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
