from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flasgger import swag_from
from api.model.use import UseModel
from api.schema.use import UseSchema
from config import APP_TITLE
from error_handlers import not_found_error, internal_server_error, bad_request_error
from flask_jwt_extended import create_access_token



info_api = Blueprint('api', __name__)

info_api.register_error_handler(404, not_found_error)
info_api.register_error_handler(500, internal_server_error)
info_api.register_error_handler(400, bad_request_error)

@info_api.route('/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': APP_TITLE
        }
    }
})
def info():
    """
    Basic API Info
    ---
    """
    result = UseModel()
    return UseSchema().dump(result), 200

#proof of concept solely to avoid making any persistent data store for this project
users = {
    'john': 'password123',
    'alice': 'mypassword',
    'bob': 'securepass'
}

@info_api.route('/login', methods=['POST'])
@swag_from({
    "tags": ["User"],
    "description": "Endpoint to log in users",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": "true",
            "schema": {
                "id": "User",
                "required": ["username", "password"],
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The user's name",
                        "default": "testuser"
                    },
                    "password": {
                        "type": "string",
                        "description": "The user's password",
                        "default": "testpassword"
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Successful login",
            "schema": {
                "id": "Resp",
                "properties": {
                    "access_token": {
                        "type": "string",
                        "description": "Access token for the logged-in user",
                        "default": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0eSI6..."
                    }
                }
            }
        },
        "401": {
            "description": "Invalid username or password",
            "schema": {
                "id": "Error",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Error message",
                        "default": "Invalid username or password"
                    }
                }
            }
        }
    }
})
def login():
    # Fetch the request data
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # Check if the user exists and if the password matches
    if users.get(username) == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid username or password"), 401
