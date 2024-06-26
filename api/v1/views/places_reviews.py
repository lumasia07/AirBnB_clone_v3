#!/usr/bin/python3
"""Creates a view for reviews"""

from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id: str):
    """Retrieves a list of all review objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def review_with_id(review_id: str):
    """Retrieves review object using ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id: str):
    """Deletes review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id: str):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing User_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    data['place_id'] = place_id
    created_review = Review(**data)
    created_review.save()
    return jsonify(created_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id: str):
    """Updates a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()

    for k, value in data.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, value)
    review.save()
    return jsonify(review.to_dict()), 200
