#!/usr/bin/python3
""" import app_views and create route to amenity """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """ return the amenities in json form """
    if request.method == 'GET':
        response_list = []
        for amenity in storage.all(Amenity).values():
            response_list.append(amenity.to_dict())
        return jsonify(response_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """ return the amenity by id in json form """
    if request.method == 'GET':
        amenity = storage.get(Amenity, amenity_id)
        if amenity is not None:
            return jsonify(amenity.to_dict())
        else:
            abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
    """ deletes an amenity by id and returns an empty dictionary"""
    amenity_deleted = storage.get(Amenity, amenity_id)
    if amenity_deleted is not None:
        storage.delete(amenity_deleted)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """ creates a new amenity object """
    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in request.get_json():
            return make_response(jsonify({"error": "Missing name"}), 400)
        amenity_dictionary = request.get_json()
        new_amenity = Amenity(**amenity_dictionary)
        storage.new(new_amenity)
        storage.save()
        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ updates an amenity object """
    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        amenity_updated = storage.get(Amenity, amenity_id)
        if amenity_updated is not None:
            for key, value in request.get_json().items():
                if key != "id" and key != "created_at" and key != "updated_at":
                    setattr(amenity_updated, key, value)
            storage.save()
            return make_response(jsonify(amenity_updated.to_dict()), 200)
        else:
            abort(404)
