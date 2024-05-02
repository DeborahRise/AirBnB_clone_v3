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
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    if storage_mode == 'db':
        place_amenities = place_obj.amenities
    else:
        place_amenities  = place_obj.amenities_id

    for A in place_amenities:
        if A.id == amenity_id:
            A.delete()
            A.save()
        else:
            abort(404)
    return jsonify({}, 200)


@app_views.route("places/<place_id>/amenities/<amenity_id>", strict_slashes=False,
                 methods=["POST"])
def link_amenitiesOfPlace(place_id, amenity_id):
    """Link Amenity to a Place"""
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    if storage_mode == "db":
        place_amenities = place_obj.amenities
    else:
        place_amenities = place_obj.amenities_id

    if amenity_obj not in place_amenities:
        place_amenities.append(amenity_obj)
    else:
        return jsonify(amenity_obj, 200)
