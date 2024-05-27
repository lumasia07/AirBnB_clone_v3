#!/usr/bin/python3
"""Creates a view for the link btn Place and Amenity objects"""

from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def all_place_amenities(place_id: str):
    """Retrieves the list of all Amenities of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if storage.__class__.__name__ == 'DBStorage':
        amens = place.amenities
    else:
        amens = [storage.get(Amenity, amenity_id)
                 for amenity_id in place.amenity_ids]
    return jsonify([x.to_dict() for x in amenities if x])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def del_place_amenity(place_id: str, amenity_id: str):
    """Deletes an Amenity from a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    x = storage.get(Amenity, amenity_id)

    if not x:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if x not in place.amenities:
            abort(404)
        place.amenities.remove(x)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def do_link(place_id: str, amenity_id: str):
    """Links an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
