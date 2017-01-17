from flask import Blueprint, jsonify, request
from . import models
from backend import db


courses = Blueprint("subject", __name__)


@courses.route('/courses', methods=['GET'])
def get_courses():
    return jsonify(courses=[dict(id=course.id, code=course.code) for course in models.Courses.query.all()])


@courses.route('/add_course', methods=['POST'])
def add_course():
    course = models.Courses()
    course.set_fields(dict(request.form.items()))

    db.session.add(course)
    db.session.commit()

    return jsonify(course=[course.serialize() for course in models.Courses.query.filter_by(code=course.code)])


@courses.route('/course_details/<course_id>', methods=['GET'])
def course_details(course_id):
    return jsonify(course=[course.serialize() for course in models.Courses.query.filter_by(id=course_id)])