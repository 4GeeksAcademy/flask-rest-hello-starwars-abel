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
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/characters', methods=['GET', 'POST'])
def characters_collection():
    if request.method == 'GET':
        items = Character.query.all()
        return jsonify([i.serialize() for i in items]), 200
    body = request.get_json(silent=True) or {}
    name = body.get('name')
    if not name:
        return jsonify({'msg': 'name required'}), 400
    height = body.get('height')
    mass = body.get('mass')
    item = Character(name=name, height=height, mass=mass)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.serialize()), 201


@app.route('/characters/<int:character_id>', methods=['GET', 'PUT', 'DELETE'])
def characters_item(character_id):
    item = Character.query.get(character_id)
    if item is None:
        return jsonify({'msg': 'not found'}), 404
    if request.method == 'GET':
        return jsonify(item.serialize()), 200
    if request.method == 'PUT':
        body = request.get_json(silent=True) or {}
        if 'name' in body:
            item.name = body['name']
        if 'height' in body:
            item.height = body['height']
        if 'mass' in body:
            item.mass = body['mass']
        db.session.commit()
        return jsonify(item.serialize()), 200
    db.session.delete(item)
    db.session.commit()
    return jsonify({'msg': 'deleted'}), 200


@app.route('/planets', methods=['GET', 'POST'])
def planets_collection():
    if request.method == 'GET':
        items = Planet.query.all()
        return jsonify([i.serialize() for i in items]), 200
    body = request.get_json(silent=True) or {}
    name = body.get('name')
    if not name:
        return jsonify({'msg': 'name required'}), 400
    climate = body.get('climate')
    population = body.get('population')
    item = Planet(name=name, climate=climate, population=population)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.serialize()), 201


@app.route('/planets/<int:planet_id>', methods=['GET', 'PUT', 'DELETE'])
def planets_item(planet_id):
    item = Planet.query.get(planet_id)
    if item is None:
        return jsonify({'msg': 'not found'}), 404
    if request.method == 'GET':
        return jsonify(item.serialize()), 200
    if request.method == 'PUT':
        body = request.get_json(silent=True) or {}
        if 'name' in body:
            item.name = body['name']
        if 'climate' in body:
            item.climate = body['climate']
        if 'population' in body:
            item.population = body['population']
        db.session.commit()
        return jsonify(item.serialize()), 200
    db.session.delete(item)
    db.session.commit()
    return jsonify({'msg': 'deleted'}), 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'not found'}), 404
    fav_chars = FavoriteCharacter.query.filter_by(user_id=user_id).all()
    fav_planets = FavoritePlanet.query.filter_by(user_id=user_id).all()
    return jsonify({
        'favorite_characters': [f.serialize() for f in fav_chars],
        'favorite_planets': [f.serialize() for f in fav_planets]
    }), 200


@app.route('/users/<int:user_id>/favorites/characters/<int:character_id>', methods=['POST', 'DELETE'])
def favorite_character(user_id, character_id):
    if request.method == 'POST':
        user = User.query.get(user_id)
        character = Character.query.get(character_id)
        if user is None or character is None:
            return jsonify({'msg': 'not found'}), 404
        fav = FavoriteCharacter(user_id=user_id, character_id=character_id)
        db.session.add(fav)
        db.session.commit()
        return jsonify(fav.serialize()), 201
    fav = FavoriteCharacter.query.filter_by(
        user_id=user_id, character_id=character_id).first()
    if fav is None:
        return jsonify({'msg': 'not found'}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({'msg': 'deleted'}), 200


@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST', 'DELETE'])
def favorite_planet(user_id, planet_id):
    if request.method == 'POST':
        user = User.query.get(user_id)
        planet = Planet.query.get(planet_id)
        if user is None or planet is None:
            return jsonify({'msg': 'not found'}), 404
        fav = FavoritePlanet(user_id=user_id, planet_id=planet_id)
        db.session.add(fav)
        db.session.commit()
        return jsonify(fav.serialize()), 201
    fav = FavoritePlanet.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if fav is None:
        return jsonify({'msg': 'not found'}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({'msg': 'deleted'}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
