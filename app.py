from flask import Flask, redirect, url_for
from flasgger import Swagger
from api.route.info import info_api
from api.route.inference import inference_api
from config import APP_TITLE, JWT_SECRET_KEY
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager


#rate limiting the API calls
limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
)



def create_app():

    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': APP_TITLE,
    }

    limiter.init_app(app)
    #app.limiter = limiter 

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header'
            }
        },
        'security': [
            {
                'Bearer': []
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }

    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    jwt = JWTManager(app)

    swagger = Swagger(app, config=swagger_config)
     ## Initialize Config
    app.config.from_pyfile('config.py')
    app.register_blueprint(info_api, url_prefix='/api')
    app.register_blueprint(inference_api, url_prefix='/api/inference')

    @app.route('/')
    def root():
        return redirect(url_for('flasgger.apidocs')) 

    return app



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
