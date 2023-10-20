from flask import Blueprint, jsonify
from http import HTTPStatus
import requests
from flasgger import swag_from
from config import APP_TITLE, GENHEALTH_API_KEY

inference_api = Blueprint('inference', __name__)


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token ' + GENHEALTH_API_KEY,
}

json_data = {
    'history': [
        {
            'code': '64',
            'system': 'age',
            'display': '64',
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

@inference_api.route('/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': APP_TITLE
            #'schema': WelcomeSchema
        }
    }
})
def inference():
    response = requests.post('https://api.genhealth.ai/predict', headers=headers, json=json_data)
    return jsonify(response.json()), 200