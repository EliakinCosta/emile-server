from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_aluno.models import User
from cruds.crud_turma.models import Turma
import datetime
from sqlalchemy import and_, cast, DateTime

aula = Blueprint("aula", __name__)


@aula.route('/disciplina_em_andamento/<professor_id>', methods=['GET'])
def disciplina_em_andamento(professor_id):
    aulas = (db.session.query(models.Aula).filter(User.id == Turma.professor_id).
                                       filter(Turma.id== models.Aula.turma_id).
                                       filter(User.id == professor_id).
                                       filter(and_(datetime.datetime.now() >= models.Aula.data_inicio_aula,
                                                   datetime.datetime.now() <= models.Aula.data_fim_aula)).all())
    return jsonify(aula=[aula.serialize() for aula in aulas])