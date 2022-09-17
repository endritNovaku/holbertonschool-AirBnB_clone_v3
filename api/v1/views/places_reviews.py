#!/usr/bin/python3
""" import app_views and create route to reviews """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """ return the review in json form """
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        response_list = []
        if place is not None:
            for review in place.reviews:
                response_list.append(review.to_dict())
            return jsonify(response_list)
        else:
            abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_by_id(review_id):
    """ return a review by id in json form """
    if request.method == 'GET':
        review = storage.get(Review, review_id)
        if review is not None:
            return jsonify(review.to_dict())
        else:
            abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_reviews(review_id):
    """ delete a review by id """
    if request.method == 'DELETE':
        review = storage.get(Review, review_id)
        if review is not None:
            storage.delete(review)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/places/<place_id>/reviews/', methods=['POST'])
def create_review(place_id):
    """ create a review """
    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "text" not in request.get_json():
            return make_response(jsonify({"error": "Missing text"}), 400)
        if "user_id" not in request.get_json():
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        api_content = request.get_json()
        user_id = api_content['user_id']
        user = storage.get(User, user_id)
        place = storage.get(Place, place_id)
        if place_id is not None and place is not None and user is not None:
            review_dictionary = request.get_json()
            new_review = Review(**review_dictionary)
            new_review.place_id = place.id
            storage.new(new_review)
            storage.save()
            return make_response(jsonify(new_review.to_dict()), 201)
        else:
            abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """ updates a review object """
    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        review_updated = storage.get(Review, review_id)
        if review_updated is not None:
            for key, value in request.get_json().items():
                if key != "id" and key != "created_at" and key != "updated_at"\
                        and key != "place_id" and key != "user_id":
                    setattr(review_updated, key, value)
            storage.save()
            return make_response(jsonify(review_updated.to_dict()), 200)
        else:
            abort(404)
