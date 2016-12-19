from flask import Flask
import backend
import os
import importlib
from flasgger import Swagger


def create_app():
    app = Flask("emile")

    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    backend.db.init_app(app)
    return app


def register_blueprints(app):
    for crud in os.listdir(os.getcwd() + '/cruds/'):
        if 'crud' in crud:
            blueprint = getattr(importlib.import_module('cruds.{0}.services'.format(crud)), crud.replace('crud_', ''))
            app.register_blueprint(blueprint)


app = create_app()
Swagger(app)
register_blueprints(app)


if __name__ == '__main__':
    app.run()
