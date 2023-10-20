from http import HTTPStatus
from flask import Blueprint, jsonify
from flasgger import swag_from
from api.model.use import UseModel
from api.schema.use import UseSchema
from config import APP_TITLE

info_api = Blueprint('api', __name__)

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