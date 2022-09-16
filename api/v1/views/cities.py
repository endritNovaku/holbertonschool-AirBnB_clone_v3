#!/usr/bin/python3
""" import app_views and create route to city """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """ return the cities in json form """
    if request.method == 'GET':
        state = storage.get(State, state_id)
        response_list = []
        if state is not None:
            for city in state.cities:
                response_list.append(city.to_dict())
            return jsonify(response_list)
        else:
            abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """ return the cities in json form """
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if city is not None:
            return jsonify(city.to_dict())
        else:
            abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ delete a city """
    if request.method == 'DELETE':
        city = storage.get(City, city_id)
        if city is not None:
            storage.delete(city)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ create a city """
    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in request.get_json():
            return make_response(jsonify({"error": "Missing name"}), 400)
        if state_id is not None:
            city_dictionary = request.get_json()
            new_city = City(**city_dictionary)
            new_city.state_id = state_id
            storage.new(new_city)
            storage.save()
            return make_response(jsonify(new_city.to_dict()), 201)
        else:
            abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ updates a city object """
    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        city_updated = storage.get(City, city_id)
        if city_updated is not None:
            for key, value in request.get_json().items():
                if key != "id" and key != "created_at" and key != "updated_at" and key != "state_id":
                    setattr(city_updated, key, value)
            storage.save()
            return make_response(jsonify(city_updated.to_dict()), 200)
        else:
            abort(404)
