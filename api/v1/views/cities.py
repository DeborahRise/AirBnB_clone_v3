#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort,request
from models.state import State
from models.city import City
from models import storage

@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_cities(state_id):
    """ Retrieves the list of all City objects of a State """
    cities_list = []

    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    for c_ity in state_obj.cities:
       
        cities_list.append(c_ity.to_dict())

    return jsonify(cities_list)

@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def get_city(city_id):
    """ Retrieves a City object """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    return jsonify(city_obj.to_dict())

@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):
    """ Deletes a City object: DELETE /api/v1/cities/<city_id> """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return ({}, 200)

@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=["POST"])
def create_city(state_id, ):
    """ Creates a City: POST /api/v1/states/<state_id>/cities """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    
    city_data = request.get_json(force=True, silent=True)
    if not city_data:
        abort(404, "Not a JSON")
    if 'name' not  in city_data:
        abort(404, "Missing name")
    city_data["state_id"] = state_id
    city_obj = City(**city_data)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 201
