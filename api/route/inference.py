from flask import Blueprint, jsonify, request
from http import HTTPStatus
import requests
from flasgger import swag_from
from config import APP_TITLE, GENHEALTH_API_KEY
from error_handlers import not_found_error, internal_server_error, bad_request_error
from flask_jwt_extended import jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError




inference_api = Blueprint('inference', __name__)
# Register error handlers for inference_api
inference_api.register_error_handler(404, not_found_error)
inference_api.register_error_handler(500, internal_server_error)
inference_api.register_error_handler(400, bad_request_error)

GENHEALTH_API_ENDPOINT = 'https://api.genhealth.ai/predict'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token ' + GENHEALTH_API_KEY,
}

## from inference API example
json_data = {
    'history': [
        {
            'code': 'female',
            'system': 'gender',
            'display': 'female',
        },
        {
            'code': 'E11',
            'system': 'ICD10CM',
            'display': 'Type 2 diabetes mellitus',
        },
        {
            'code': 'E11.3551',
            'system': 'ICD10CM',
            'display': 'Type 2 diabetes mellitus with stable proliferative diabetic retinopathy, right eye',
        },
    ],
    'num_predictions': 1,
    'generation_length': 10,
    'inference_threshold': 0.95,
    'inference_temperature': 0.95,
}
@inference_api.route('/', methods=['POST'])
@jwt_required()
@swag_from({
    'security': [
        {
            'Bearer': []
        }
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': APP_TITLE
            #'schema': WelcomeSchema
        }
    }
})
def inference():
    response = requests.post(GENHEALTH_API_ENDPOINT, headers=headers, json=json_data)
    return jsonify(response.json()), 200



@inference_api.route('/diagnosis', methods=['POST'])
@jwt_required()
@swag_from({
    'security': [
        {
            'Bearer': []
        }
    ],
    'responses': {
        '200': {
            'description': 'Successful prediction',
            'schema': {
                'type': 'object',
                'properties': {
                    'predictions': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'system': {
                                    'type': 'string'
                                },
                                'code': {
                                    'type': 'string'
                                },
                                'display': {
                                    'type': 'string'
                                }
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Bad Request. Invalid input.'
        }
    },
    'parameters': [
    {
        'name': 'body',
        'in': 'body',
        'required': True,
        'description': 'Payload containing the list of diagnosis codes',
        'schema': {
            'type': 'object',
            'properties': {
                'diagnosis_codes': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    },
                    'description': 'List of diagnosis codes'
                }
            }
        }
    }],
    'tags': ['Predictions']
})
def predict_diagnosis():
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON data received, " + str(data)}), 400

        diagnosis_codes = data.get('diagnosis_codes', [])
        if not all(isinstance(code, str) for code in diagnosis_codes):
            raise ValueError("Invalid diagnosis codes. All codes should be strings.")

        # Construct the history array
        history = [];
        for code in diagnosis_codes:
            history.append({"code": code, "system": "ICD10CM", "display": code})

        return call_genhealth_api(history)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inference_api.route('/gender', methods=['POST'])
@jwt_required()
@swag_from({
    'security': [
        {
            'Bearer': []
        }
    ],
    'responses': {
        '200': {
            'description': 'Successful prediction',
            'schema': {
                'type': 'object',
                'properties': {
                    'predictions': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'system': {
                                    'type': 'string'
                                },
                                'code': {
                                    'type': 'string'
                                },
                                'display': {
                                    'type': 'string'
                                }
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Bad Request. Invalid input.'
        }
    },
    'parameters': [
        {
            'name': 'gender',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'gender': {
                        'type': 'string',
                        'enum': ['male', 'female'],  # This creates the dropdown
                        'description': 'The gender of the patient',
                    }
                }
            },
            'required': 'true'
        }
    ],
    'tags': ['Predictions']
})
def predict_gender():
    try:
        data = request.get_json()

        #'history': [
        #{
        #    'code': 'female',
        #    'system': 'gender',
        #    'display': 'female',
        #}]

        # Validation
        gender = data.get('gender')
        if gender not in ["male", "female"]:
            raise ValueError("Invalid gender. Allowed values are 'male' and 'female'.")

        history = [{"code": gender, "system": "gender", "display": gender}]
        
        return call_genhealth_api(history)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

def call_genhealth_api(history):
    try:

        data = {
            "history": history,
            "num_predictions": 1,
            "generation_length": 10,
            "inference_threshold": 0.95,
            "inference_temperature": 0.95
        }

        response = requests.post(GENHEALTH_API_ENDPOINT, json=data, headers=headers)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            raise Exception("Failed to get a response from the GenHealth API: " + response.text)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inference_api.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return jsonify(error=str(e)), 401