#!/usr/bin/python3
# Script that starts a Flask web application:
#   Routes:
#       - /hbnb_filters: display an HTML page like 6-index.html, which
#           was done during the project 0x01. AirBnB clone - Web static
#       - Copy files 3-footer.css, 3-header.css, 4-common.css and
#           6-filters.css from web_static/styles/ to the folder
#           web_flask/static/styles
#       - Copy files icon.png and logo.png from web_static/images/ to the
#           folder web_flask/static/images
#       - Update .popover class in 6-filters.css to allow scrolling in the
#           popover and a max height of 300 pixels.
#       - Use 6-index.html content as source code for the template
#           10-hbnb_filters.html:
#               - Replace the content of the H4 tag under each filter
#                   title (H3 States and H3 Amenities) by &nbsp;
#       - State, City and Amenity objects must be loaded from DBStorage
#           and sorted by name (A->Z)


from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


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


@app.route('/hbnb_filters')
def fetch_filters():
    """
    Fetch the state that matches that id and display on html page
    """
    state_objs = []
    amenity_objs = []
    for states in storage.all(State).values():
        state_objs.append(states)
    for amens in storage.all(Amenity).values():
        amenity_objs.append(amens)
    return render_template('10-hbnb_filters.html', state_objs=state_objs, amenity_objs=amenity_objs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
