#!/usr/bin/python3
""" import app_views and create route to users """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """ return the users in json form """
    if request.method == 'GET':
        response_list = []
        for user in storage.all(User).values():
            response_list.append(user.to_dict())
        return jsonify(response_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """ return the user by id in json form """
    if request.method == 'GET':
        user = storage.get(User, user_id)
        if user is not None:
            return jsonify(user.to_dict())
        else:
            abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """ deletes a user by id and returns an empty dictionary"""
    user_deleted = storage.get(User, user_id)
    if user_deleted is not None:
        storage.delete(user_deleted)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users/', methods=['POST'])
def create_user():
    """ creates a new user object """
    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "email" not in request.get_json():
            return make_response(jsonify({"error": "Missing email"}), 400)
        if "password" not in request.get_json():
            return make_response(jsonify({"error": "Missing password"}), 400)
        user_dictionary = request.get_json()
        new_user = User(**user_dictionary)
        storage.new(new_user)
        storage.save()
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ updates a user object """
    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        user_updated = storage.get(User, user_id)
        if user_updated is not None:
            for key, value in request.get_json().items():
                if key != "id" and key != "created_at"\
                        and key != "updated_at" and key != "email":
                    setattr(user_updated, key, value)
            storage.save()
            return make_response(jsonify(user_updated.to_dict()), 200)
        else:
            abort(404)
