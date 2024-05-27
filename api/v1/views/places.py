#!/usr/bin/python3
"""Creates a view for places"""

from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def all_places(city_id: str):
    """Retrieves a list of all place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'])
def place_with_id(place_id: str):
    """Retrieves place object using ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id: str):
    """Deletes place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id: str):
    """Creates a Place"""
    city = storage.get(City, city_id):

    if not city:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")

    info = request.get_json()

    if 'user_id' not in info:
        abort(400, description="Missing user_id")

    user = storage.get(User, info['user_id'])

    if not user:
        abort(404)
    if 'name' not in info:
        abort(400, description="Missing name")

    info['city_id'] = city_id
    created_place = Place(**info)
    created_place.save()
    return jsonify(created_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id: str):
    """Updates a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    for k, value in data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, value)
    place.save()
    return jsonify(place.to_dict()), 200
