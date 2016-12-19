from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_user.models import User
from cruds.crud_classes.models import Classes
import datetime
from sqlalchemy import and_
from cruds.crud_frequency.models import Frequency


lesson = Blueprint("lesson", __name__)


@lesson.route('/lesson_in_progress/<teacher_id>', methods=['GET'])
def lesson_in_progress(teacher_id):
    lessons = (db.session.query(models.Lesson).filter(User.id == Classes.teacher_id).
               filter(Classes.id == models.Lesson.classes_id).
               filter(User.id == teacher_id).
               filter(and_(datetime.datetime.now() >= models.Lesson.lesson_start_date,
                           datetime.datetime.now() <= models.Lesson.lesson_finish_date)).all())
    return jsonify(lesson=[lesson.serialize() for lesson in lessons])


@lesson.route('/frequency_register/<lesson_id>', methods=['POST'])
def frequency_register(lesson_id):
    frequency_list = request.get_json()['frequency']

    try:
        lesson = models.Lesson.query.get(lesson_id)
        if not lesson.frequency_status:
            with db.session.no_autoflush:
                for register in frequency_list:
                    frequency = Frequency(status=register['status'])
                    frequency.user = User.query.get(register['student_id'])
                    lesson.frequency.append(frequency)

            lesson.frequency_status=True
            db.session.commit()
    except:
        return jsonify(result="Invalid request")
    return jsonify(frequency=[frequency.serialize() for frequency in lesson.frequency])


@lesson.route('/update_lesson/<lesson_id>', methods=['POST'])
def update_lesson(lesson_id):
    """ This method allows to update from kwargs """

    lesson = models.Lesson.query.get(lesson_id)

    if lesson:
        lesson.set_fields(dict(request.form.items()))
        db.session.commit()
        return jsonify(lesson=[lesson.serialize() for lesson in models.Lesson.query.filter_by(id=lesson_id)])
    return jsonify(result='invalid lesson id')