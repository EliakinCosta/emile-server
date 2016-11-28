from flask import Flask
import settings
import backend
import os
from cruds.crud_aluno import services as aluno_services
from cruds.crud_disciplina import services as disciplina_services
from cruds.crud_turma import services as turma_services


def create_app(backend_path=''):
    app = Flask("emile")
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print(os.environ['APP_SETTINGS'])
    print(backend_path)
    backend.db.init_app(app)
    return app


app = create_app(settings.BACKEND_PATH)
app.register_blueprint(aluno_services.user)
app.register_blueprint(disciplina_services.disciplina)
app.register_blueprint(turma_services.turma)


if __name__ == '__main__':
    app.run()
