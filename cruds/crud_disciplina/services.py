from flask import Blueprint, jsonify, request
from . import models
from backend import db


disciplina = Blueprint("disciplina", __name__)

@disciplina.route('/disciplinas', methods=['GET'])
def get_users():
    return jsonify(disciplinas=[dict(id=disciplina.id, codigo=disciplina.codigo) for disciplina in models.Disciplina.query.all()])


@disciplina.route('/add_disciplina', methods=['POST'])
def add_disciplina():
    """ This method it was implemented considering that all fields are required in client """

    disciplina = models.Disciplina()
    disciplina.set_fields(dict(request.form.items()))

    db.session.add(disciplina)
    db.session.commit()

    return jsonify(disciplina=[disciplina.serialize() for disciplina in models.Disciplina.query.filter_by(codigo=disciplina.codigo)])


@disciplina.route('/disciplina_details/<disciplina_id>', methods=['GET'])
def disciplina_details(disciplina_id):
    return jsonify(user=[disciplina.serialize() for disciplina in models.Disciplina.query.filter_by(id=disciplina_id)])