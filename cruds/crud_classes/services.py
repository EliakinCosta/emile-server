from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_user.models import User
from cruds.crud_lesson.models import Lesson
import datetime
from sqlalchemy import and_, or_

classes = Blueprint("classes", __name__)


@classes.route('/classes', methods=['GET'])
def get_classes():
    return jsonify(classes=[dict(id=classes.id, code=classes.code) for classes in models.Classes.query.all()])


@classes.route('/add_classes', methods=['POST'])
def add_classes():
    """ This method it was implemented considering that all fields are required in client """

    user = models.User.query.get(request.form.get('teacher_id')).serialize()
    if user['type'] == 'teacher':
        classes = models.Classes()
        classes.set_fields(dict(request.form.items()))

        db.session.add(classes)
        db.session.commit()

        return jsonify(classes=[classes.serialize() for classes in models.Classes.query.filter_by(code=classes.code)])
    return jsonify(result='invalid teacher id')


@classes.route('/add_student_classes/<classes_id>/<user_id>', methods=['POST'])
def add_student_classes(classes_id, user_id):
    classes = models.Classes.query.get(classes_id)
    classes.students.append(User.query.get(user_id))
    db.session.commit()
    return jsonify(classes=models.Classes.query.get(classes_id).serialize())


@classes.route('/classes_details/<classes_id>', methods=['GET'])
def classes_details(classes_id):
    return jsonify(classes=models.Classes.query.get(classes_id).serialize())


@classes.route('/add_lesson_classes/<classes_id>', methods=['POST'])
def add_lesson_classes(classes_id):
    classes = models.Classes.query.get(classes_id)

    lesson_start_time = datetime.datetime.strptime(request.form.get('lesson_start_time'), '%H:%M:%S').time()
    lesson_finish_time = datetime.datetime.strptime(request.form.get('lesson_finish_time'), '%H:%M:%S').time()
    week_day = request.form.get('week_day')

    #Verificação de horaŕio de inicio e fim da aula. Se a aula adicionada para a turma ja existe dentro daquela faixa de horário,
    # ou começa e termina dentro de um intervalo de horário ja existente.
    if not (db.session.query(Lesson).filter(models.Classes.id== Lesson.classes_id).
                                       filter(or_(and_(lesson_start_time > Lesson.lesson_start_time,
                                                       lesson_start_time < Lesson.lesson_finish_time),
                                                  and_(lesson_finish_time > Lesson.lesson_start_time,
                                                       lesson_finish_time < Lesson.lesson_finish_time))).filter(week_day==Lesson.week_day).all()):

        lesson = Lesson(lesson_start_time=lesson_start_time, lesson_finish_time=lesson_finish_time, week_day= week_day)
        classes.lessons.append(lesson)

        db.session.commit()

        return jsonify(classes=classes.serialize())

    return jsonify(result='invalid period')


@classes.route('/students_classes/<classes_id>', methods=['GET'])
def students_classes(classes_id):
    classes = models.Classes.query.get(classes_id)
    return jsonify(students_classes=[dict(id=student.id, email=student.email) for student in classes.students])