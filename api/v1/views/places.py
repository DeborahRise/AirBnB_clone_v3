#!/usr/bin/python3
""" new view for Place objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City
    /cities/<city_id>/places"""

    places_list = []
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    all_places = storage.all(Place).values()
    for p in all_places:
        if p.city_id == city_id:
            places_list.append(p.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def get_place(place_id):
    """ Retrieves a Place object. : GET /api/v1/places/<place_id> """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["DELETE"])
def delete_place(place_id):
    """ Deletes a Place object """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    """Creates a Place /cities/<city_id>/places"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    place_obj = request.get_json(force=True, silent=True)
    if not place_obj:
        abort(400, "Not a Json")
    if "user_id" not in place_obj:
        abort(400, "Missing user_id")
    user_obj = storage.get(User, place_obj.get("user_id"))
    if not user_obj:
        abort(404)
    if "name" not in place_obj:
        abort(400, "Missing name")
    new_place = Place(**place_obj)
    new_place.save()
    return jsonify(new_place.to_dict())