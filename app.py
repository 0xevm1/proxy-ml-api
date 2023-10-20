from flask import Flask
from flasgger import Swagger
from api.route.info import info_api
from api.route.inference import inference_api
from config import APP_TITLE

def create_app():
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': APP_TITLE,
    }

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
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }

    swagger = Swagger(app, config=swagger_config)
     ## Initialize Config
    app.debug = True;
    app.config.from_pyfile('config.py')
    app.register_blueprint(info_api, url_prefix='/api')
    app.register_blueprint(inference_api, url_prefix='/api/inference')

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
