#!/usr/bin/python3
"""A place review view to handle place review request"""


from flask import jsonify, request
from models import storage
from models.review import Review
from api.v1.views import app_views
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'error': 'Place not found'}), 404

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def get_reviews():
    """Retrieves a list of all Review objects"""
    reviews = storage.all(Review).values()
    return jsonify([review.to_dict() for review in reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a specific Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/reviews', methods=['POST'], strict_slashes=False)
def create_review():
    """Creates a new Review object"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400

    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400

    if 'place_id' not in data:
        return jsonify({'error': 'Missing place_id'}), 400

    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in data.items():
        setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict())
