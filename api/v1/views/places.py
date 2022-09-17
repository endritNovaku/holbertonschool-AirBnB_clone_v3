#!/usr/bin/python3
""" import app_views and create route to places """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """ return the places in json form """
    if request.method == 'GET':
        city = storage.get(City, city_id)
        response_list = []
        if city is not None:
            for place in city.places:
                response_list.append(place.to_dict())
            return jsonify(response_list)
        else:
            abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    """ return a place by id in json form """
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place is not None:
            return jsonify(place.to_dict())
        else:
            abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ delete a place by id """
    if request.method == 'DELETE':
        place = storage.get(Place, place_id)
        if place is not None:
            storage.delete(place)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/cities/<city_id>/places/', methods=['POST'])
def create_place(city_id):
    """ create a place """
    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in request.get_json():
            return make_response(jsonify({"error": "Missing name"}), 400)
        if "user_id" not in request.get_json():
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        test = request.get_json()
        a_test = test['user_id']
        user = storage.get(User, a_test)
        city = storage.get(City, city_id)
        if city_id is not None and city is not None and user is not None:
            place_dictionary = request.get_json()
            new_place = Place(**place_dictionary)
            new_place.city_id = city.id
            storage.new(new_place)
            storage.save()
            return make_response(jsonify(new_place.to_dict()), 201)
        else:
            abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ updates a place object """
    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        place_updated = storage.get(Place, place_id)
        if place_updated is not None:
            for key, value in request.get_json().items():
                if key != "id" and key != "created_at" and key != "updated_at"\
                        and key != "city_id" and key != "user_id":
                    setattr(place_updated, key, value)
            storage.save()
            return make_response(jsonify(place_updated.to_dict()), 200)
        else:
            abort(404)
