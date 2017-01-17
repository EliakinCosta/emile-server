from flask import Blueprint, jsonify, request
from . import models
from backend import db


courses = Blueprint("subject", __name__)


@courses.route('/courses', methods=['GET'])
def get_courses():
    # Docs
    """
           Get all Courses
           ---
           tags:
             - /courses
           responses:
             200:
               description: This is the view to get all Courses.
               schema:
                 properties:
                   courses:
                     type: array
                     description: Course's list
                     items:
                       type: string
                       default: {"id": integer, "code": string}
    """
    return jsonify(courses=[dict(id=course.id, code=course.code) for course in models.Courses.query.all()])


@courses.route('/add_course', methods=['POST'])
def add_course():
    # Docs
    """
           Add Course.
           ---
           tags:
             - /courses
           responses:
             200:
               description:  This is the view to add a course.
               schema:
                 properties:
                   course:
                     type: array
                     description: Course's list
                     items:
                       type: string
                       default: {"id": integer, "code": string, "name": string}

    """
    course = models.Courses()
    course.set_fields(dict(request.form.items()))

    db.session.add(course)
    db.session.commit()

    return jsonify(course=[course.serialize() for course in models.Courses.query.filter_by(code=course.code)])


@courses.route('/course_details/<course_id>', methods=['GET'])
def course_details(course_id):
    # Docs
    """
           Course Details
           ---
           tags:
             - /courses
           responses:
             200:
               description:  This is the view to get details for a Course.
               schema:
                 properties:
                   course:
                     type: array
                     description: Course object.
                     items:
                       type: string
                       default: {"id": integer, "code": string, "name": string}
    """
    return jsonify(course=[course.serialize() for course in models.Courses.query.filter_by(id=course_id)])