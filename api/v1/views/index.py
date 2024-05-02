#!/usr/bin/python3
"""
This module contains endpoint(route) status
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns a JSON response with the status "OK".

    Returns:
        Response: A JSON response with the status "OK".
    """
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def stats():
    _count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(_count)
