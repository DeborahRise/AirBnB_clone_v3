#!/usr/bin/python3
"""  a new view for the link between Place objects and Amenity objects
that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort
import os

storage_mode = os.getenv("HBNB_TYPE_STORAGE")

@app_views.route("places/<place_id>/amenities", strict_slashes=False, methods=["GET"])
def get_amenitiesOfPlace(place_id):
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    amenity_list = []
    if storage_mode == 'db':
        all_amenities = place_obj.amenities
        for A in all_amenities:
            amenity_list.append(A.to_dict())
    else:
        amenity_list = place_obj.amenity_ids
    return jsonify(amenity_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", strict_slashe=False,
                 methods=["DELETE"])
def delete_amenitiesOfPlace(place_id, amenity_id):
    """ deleting the amenity obj in a unique place """
    obj_place = storage.get("Place", place_id)
    obj_amenity = storage.get("Amenity", amenity_id)
    if obj_amenity is None:
        abort(404)
    if obj_place is None:
        abort(404)
    amenities = obj_place.amenities
    list_am = [am.id for am in amenities]
    if amenity_id not in list_am:
        abort(404)
    for am in amenities:
        if am.id == amenity_id:
            obj_amenity.delete()
    storage.save()
    return (jsonify({})), 200
