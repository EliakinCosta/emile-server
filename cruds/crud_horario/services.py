from flask import Blueprint, jsonify, request
from . import models
from backend import db


horario = Blueprint("horario", __name__)

@horario.route('/horarios', methods=['GET'])
def get_horarios():
    return jsonify(horarios=[horario.serialize() for horario in models.Horario.query.all()])


@horario.route('/add_horario', methods=['POST'])
def add_disciplina():
    """ This method it was implemented considering that all fields are required in client """

    horario = models.Horario()
    horario.set_fields(dict(request.form.items()))

    db.session.add(horario)
    db.session.commit()

    return jsonify(horario=[horario.serialize() for horario in models.Horario.query.filter_by(hora_inicio=horario.hora_inicio,
                                                                                              hora_fim=horario.hora_fim)])