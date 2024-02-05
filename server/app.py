#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.json

    # Validate request body
    if not data or 'name' not in data or 'image' not in data or 'price' not in data or 'is_in_stock' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    # Create a new plant object
    new_plant = {
        'id': len(plants) + 1,  # Generate unique ID (replace with database-generated ID)
        'name': data['name'],
        'image': data['image'],
        'price': data['price'],
        'is_in_stock': data['is_in_stock']
    }

    # Add the new plant to the plants list (or save to database)
    plants.append(new_plant)

    # Return the newly created plant as JSON response
    return jsonify(new_plant), 201


@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get_or_404(id)
    data = request.json
    
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']
    
    db.session.commit()
    
    return jsonify({
        'id': plant.id,
        'name': plant.name,
        'image': plant.image,
        'price': plant.price,
        'is_in_stock': plant.is_in_stock
    })

@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get_or_404(id)
    db.session.delete(plant)
    db.session.commit()
    
    return '', 204




if __name__ == '__main__':
    app.run(port=5555, debug=True)
