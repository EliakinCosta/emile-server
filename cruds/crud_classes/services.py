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

    classes = models.Classes()
    classes.set_fields(dict(request.form.items()))

    db.session.add(classes)
    db.session.commit()

    return jsonify(classes=[classes.serialize() for classes in models.Classes.query.filter_by(code=classes.code)])


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

    lesson_start_date = datetime.datetime.strptime(request.form.get('lesson_start_date'), '%d/%m/%Y-%H:%M:%S')
    lesson_finish_date = datetime.datetime.strptime(request.form.get('lesson_finish_date'), '%d/%m/%Y-%H:%M:%S')

    if not (db.session.query(Lesson).filter(models.Classes.id== Lesson.classes_id).
                                       filter(or_(and_(lesson_start_date > Lesson.lesson_start_date,
                                                       lesson_start_date < Lesson.lesson_finish_date),
                                                  and_(lesson_finish_date > Lesson.lesson_start_date,
                                                       lesson_finish_date < Lesson.lesson_finish_date))).all()):

        lesson = Lesson(lesson_start_date=lesson_start_date, lesson_finish_date=lesson_finish_date)
        classes.lessons.append(lesson)

        db.session.commit()

        return jsonify(classes=classes.serialize())

    return jsonify(result='invalid period')


@classes.route('/students_classes/<classes_id>', methods=['GET'])
def students_classes(classes_id):
    classes = models.Classes.query.get(classes_id)
    return jsonify(students_classes=[dict(id=student.id, email=student.email) for student in classes.students])