from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_users.models import Users
from cruds.crud_section_times.models import SectionTimes
import datetime
from sqlalchemy import and_, or_

course_sections = Blueprint("course_sections", __name__)


@course_sections.route('/course_sections', methods=['GET'])
def get_course_section():
    # Docs
    """
           Get all Course Sections
           ---
           tags:
             - /course_sections
           responses:
             200:
               description: This is the view to get all Course Sections.
               schema:
                 properties:
                   course_sections:
                     type: array
                     description: Course Sections list
                     items:
                       type: string
                       default: {"id": integer, "code": string}
    """
    return jsonify(course_sections=[dict(id=course_section.id, code=course_section.code) for course_section in models.CourseSections.query.all()])


@course_sections.route('/add_course_section', methods=['POST'])
def add_course_section():
    # Docs
    """
           Add Course Section
           ---
           tags:
             - /course_sections
           parameters:
              - name: code
                in: formData
                description: code of the course.
                required: true
                type: string
              - name: name
                in: formData
                description: name of the course.
                required: true
                type: string
              - name: course_id
                in: formData
                description: course foreign key.
                required: true
                type: integer
              - name: teacher_id
                in: formData
                description: teacher foreign key.
                required: true
                type: integer
           responses:
             200:
               description:  This is the view to add a course.
               schema:
                 properties:
                   course:
                     type: array
                     description: Course Sections list
                     items:
                       type: string
                       default: {"id": integer, "code": string, "name": string, "course": { "code": string, "id": integer, "name": string }, "teacher_id": integer}
    """

    user = models.Users.query.get(request.form.get('teacher_id')).serialize()
    if user['type'] == 'teacher':
        course_section = models.CourseSections()
        course_section.set_fields(dict(request.form.items()))

        db.session.add(course_section)
        db.session.commit()

        return jsonify(course_sections=[course_section.serialize() for course_section in models.CourseSections.query.filter_by(code=course_section.code)])
    return jsonify(result='invalid teacher id')


@course_sections.route('/add_student_course_section/<course_section_id>/<user_id>', methods=['POST'])
def add_student_classes(course_section_id, user_id):
    course_section = models.CourseSections.query.get(course_section_id)
    course_section.students.append(Users.query.get(user_id))
    db.session.commit()
    return jsonify(course_section=models.CourseSections.query.get(course_section_id).serialize())


@course_sections.route('/course_section_details/<course_section_id>', methods=['GET'])
def classes_details(course_section_id):
    return jsonify(course_section=models.CourseSections.query.get(course_section_id).serialize())


@course_sections.route('/add_section_time_course_section/<course_section_id>', methods=['POST'])
def add_lesson_classes(course_section_id):
    course_section = models.CourseSections.query.get(course_section_id)

    section_time_start_time = datetime.datetime.strptime(request.form.get('section_time_start_time'), '%H:%M:%S').time()
    section_time_finish_time = datetime.datetime.strptime(request.form.get('section_time_finish_time'), '%H:%M:%S').time()
    week_day = request.form.get('week_day')

    if not (db.session.query(SectionTimes).filter(models.CourseSections.id== SectionTimes.course_section_id).
                                       filter(or_(and_(section_time_start_time >= SectionTimes.section_time_start_time,
                                                       section_time_start_time <= SectionTimes.section_time_finish_time),
                                                  and_(section_time_finish_time >= SectionTimes.section_time_start_time,
                                                       section_time_finish_time <= SectionTimes.section_time_finish_time))).filter(week_day==SectionTimes.week_day).all()):

        section_time = SectionTimes(section_time_start_time=section_time_start_time, section_time_finish_time=section_time_finish_time, week_day= week_day)
        course_section.section_times.append(section_time)

        db.session.commit()

        return jsonify(course_sections=course_section.serialize())

    return jsonify(result='invalid period')


@course_sections.route('/students_course_section/<course_section_id>', methods=['GET'])
def students_course_section(course_section_id):
    course_section = models.CourseSections.query.get(course_section_id)
    return jsonify(students_course_section=[dict(id=student.id, email=student.email) for student in course_section.students])