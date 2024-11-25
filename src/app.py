"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    response_body = [user.serialize() for user in users]
    return jsonify(response_body), 200

@app.route('/users/<int:user_id>/', methods=['GET'])
def get_user_with_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user_data = user.serialize()
    user_data['favorites'] = [favorite.serialize() for favorite in user.favorites]
    
    return jsonify(user_data), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    characters_list = [character.serialize() for character in characters]
    return jsonify(characters_list), 200

@app.route('/character/<int:character_id>/', methods=['GET'])
def get_character_by_id(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character.serialize()), 200

@app.route('/planet/<int:planet_id>/', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets_list = [planet.serialize() for planet in planets]
    return jsonify(planets_list), 200

@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['POST'])
def add_favorite_planet(planet_id, user_id):
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if user is None or planet is None:
        return jsonify({"error": "User or Planet not found"}), 404
    favorite = Favorite(user_id=user_id, user_planet=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet added successfully"}), 201

@app.route('/favorite/character/<int:character_id>/<int:user_id>', methods=['POST'])
def add_favorite_character(character_id, user_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)
    if user is None or character is None:
        return jsonify({"error": "User or Character not found"}), 404
    favorite = Favorite(user_id=user_id, user_character=character_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite character added successfully"}), 201

@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id, user_id):
    favorite = Favorite.query.filter_by(user_id=user_id, user_planet=planet_id).first()
    if favorite is None:
        return jsonify({"error": "Favorite planet not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet removed successfully"}), 200

@app.route('/favorite/character/<int:people_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_person(people_id, user_id):
    favorite = Favorite.query.filter_by(user_id=user_id, user_character=people_id).first()
    if favorite is None:
        return jsonify({"error": "Favorite person not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite person removed successfully"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
