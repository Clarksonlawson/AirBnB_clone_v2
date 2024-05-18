#!/usr/bin/python3
"""
This script starts a Flask web application.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Route that displays 'Hello HBNB!'"""
    return 'Hello HBNB!'

@app.route('/airbnb-onepage/', strict_slashes=False)
def hello():
    """ Route to return a simple string. """
    return "Hello HBNB!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
