#!/usr/bin/python3
"""
This module contains the principal application
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r'/*': {'origins': 'http://0.0.0.0'}})


@app.teardown_appcontext
def close_db(exception):
    """
    Close the storage when the application context ends.

    Args:
        exception (Exception): An optional exception
        that occurred during request handling.
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    response = make_response(jsonify(error="Not found"), 404)
    return response


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
