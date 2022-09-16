#!/usr/bin/python3
""" import app_views and create route to state """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """ return the states in json form """
    if request.method == 'GET':
        response_list = []
        for obj in storage.all(State).values():
            response_list.append(obj.to_dict())
        return jsonify(response_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_by_id(state_id):
    """ return the state by id in json form """
    if request.method == 'GET':
        obj = storage.get(State, state_id)
        if obj is not None:
            return jsonify(obj.to_dict())
        else:
            abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_by_id(state_id):
    """ deletes a state by id and returns an empty dictionary"""
    state_deleted = storage.get(State, state_id)
    if state_deleted is not None:
        storage.delete(state_deleted)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/', methods=['POST'])
def create_state():
    """ creates a new state object """
    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 404)
        if "name" not in request.get_json():
            return make_response(jsonify({"error": "Missing name"}), 404)
        state_dictionary = request.get_json()
        new_state = State(**state_dictionary)
        storage.new(new_state)
        storage.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ updates a state object """
    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 404)
        state_updated = storage.get(State, state_id)
        if state_updated is not None:
            for key, value in request.get_json().items():
                if key != "id" and key != "created_at" and key != "updated_at":
                    setattr(state_updated, key, value)
            storage.save()
            return make_response(jsonify(state_updated.to_dict()), 200)
        else:
            abort(404)
