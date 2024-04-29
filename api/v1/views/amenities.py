#!/usr/bin/python3
"""new view for Amenity objects
that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", strict_slashes=False,
                 methods=["GET"])
def get_Amenities():
    """ Retrieves the list of all Amenity objects """
    Amenity_list = []

    Amenity_obj = storage.all(Amenity)
    if not Amenity_obj:
        abort(404)
    for a_menities in Amenity_obj:
        Amenity_list.append(a_menities.to_dict())

    return jsonify(Amenity_list)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["GET"])
def get_Amenity(amenity_id):
    """ Retrieves an amentiy object """
    Amenity_obj = storage.get(Amenity, amenity_id)
    if not Amenity_obj:
        abort(404)
    return jsonify(Amenity_obj.to_dict())


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_Amenity(amenity_id):
    """ Deletes an amenitobject: DELETE /api/v1/cities/<city_id> """
    Amenity_obj = storage.get(Amenity, amenity_id)
    if not Amenity_obj:
        abort(404)
    storage.delete(Amenity_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False,
                 methods=["POST"])
def create_Amenity():
    """ Creates a City: POST /api/v1/states/<state_id>/cities """
    Amenity_obj = request.get_json(force=True, silent=True)
    if not Amenity_obj:
        abort(404, "Not a JSON")
    if 'name' not in Amenity_obj:
        abort(404, "Missing name")
    Amenity_data = Amenity(**Amenity_obj)
    Amenity_data.save()
    return jsonify(Amenity_data.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def update_Amenity(amenity_id):
    """ Updates a City object: PUT /api/v1/cities/<city_id> """
    Amenity_obj = storage.get(Amenity, amenity_id)
    if not Amenity_obj:
        abort(404)
    Amenity_data = request.get_json(force=True, silent=True)
    if not Amenity_data:
        abort(404, "Not a JSON")
    Amenity_obj.name = Amenity_data.get("name", Amenity_obj.name)
    Amenity_obj.save()
    return jsonify(Amenity_obj.to_dict()), 200
