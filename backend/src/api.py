import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from .auth.auth import AuthError, requires_auth
from .database.models import db_drop_and_create_all, setup_db, Drink
from flask_cors import CORS
import sys

app = Flask(__name__)
setup_db(app)
CORS(app)

# Done uncomment the following line to initialize the datbase

db_drop_and_create_all()


## ROUTES

# Done implement endpoint
#     GET /drinks

@app.route("/", methods=["GET"])
def index():
    return "Here is my coffee"


# Done implement endpoint
#     GET /drinks-detail
@app.route("/drinks", methods=["GET"])
def get_drinks():
    # get all drinks

    drinks_result = Drink.query.all()

    # get short drinks
    shortDrinks = [drink.short() for drink in drinks_result]

    return jsonify({

        "Success": True,
        "drinks": shortDrinks
    }), 200


# Get long drink details
@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def get_drinks_detail(jwt):
    # get all drinks
    drinks_result = Drink.query.all()
    # get long drinks
    longDrinks = [drink.long() for drink in drinks_result]

    return jsonify({
        "Success": True,
        "drinks": longDrinks
    }), 200


# Done implement endpoint POST /drinks

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    body = request.get_json()
    # get title and Recipe
    title = body.get("title", None)
    recipe = body.get("recipe", None)

    # Add newly created drink to db
    Drink(
        title=title,
        recipe=json.dumps(recipe)
    ).insert()

    return jsonify({
        "success": True,
        "drinks": [Drink(
            title=title,
            recipe=json.dumps(recipe)
        ).long()],
    }), 200


# Done implement endpoint PATCH /drinks/<id>


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    drink_query = Drink.query.filter(Drink.id == id).one_or_none()
    req = request.get_json()

    title = req.get('title')
    recipe = req.get('recipe')

    # updated the existed data with new data
    if title: drink_query.title = title

    if recipe: drink_query.recipe = json.dumps(req['recipe'])

    drink_query.update()

    # respond with a 404 error if <id> is not found
    if not drink_query:
        abort(404)

    return jsonify({'success': True, 'drinks': [drink_query.long()]}), 200


# Done implement endpoint DELETE /drinks/<id>


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    drink.delete()

    # respond with a 404 error if <id> is not found
    if not drink:
        abort(404)

    return jsonify({'success': True, 'delete': id}), 200


## Error Handling

# Example error handling for unprocessable entity

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


# Done implement error handlers using the @app.errorhandler(error) decorator

# Done error handler


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found",
    }), 404


@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error",
    }), 500

@app.errorhandler(400)
def internal_server_error(error):

    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request",
    }), 400

@app.errorhandler(403)
def internal_server_error(error):

    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden",
    }), 403

@app.errorhandler(401)
def internal_server_error(error):

    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized",
    }), 401



# Done implement error handler for AuthError

@app.errorhandler(AuthError)
def auth_error(exception):
    response = jsonify(exception.error)
    response.status_code = exception.status_code
    return response
