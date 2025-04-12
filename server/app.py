#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from models import db, Plant  # adjust the imports according to your project structure

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'  # Change as necessary
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# PATCH /plants/<id>: Update a plant
@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    # Locate the plant by id
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404

    # Parse the request body JSON
    data = request.get_json()

    # Check for the "is_in_stock" key; update the field if it exists
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']
    else:
        return jsonify({'error': 'Bad Request: "is_in_stock" not provided'}), 400

    # Commit the changes to the database
    db.session.commit()

    # Return the updated plant details as JSON
    return jsonify(plant.to_dict()), 200


# DELETE /plants/<id>: Delete a plant
@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    # Locate the plant by id
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404

    # Delete the plant record from the database
    db.session.delete(plant)
    db.session.commit()

    # Return an empty response with HTTP 204 status code
    return make_response('', 204)


if __name__ == "__main__":
    app.run(port=5555, debug=True)

