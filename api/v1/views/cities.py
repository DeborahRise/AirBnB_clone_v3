#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort
from models.state import State
from models.city import City
from models import storage

@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_cities(state_id):
    cities_list = []

    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    for c_ity in state_obj.cities:
       
        cities_list.append(c_ity.to_dict())

    return jsonify(cities_list)

@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def get_city(city_id):
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    city_obj.__class__
    return jsonify(city_obj.to_dict())