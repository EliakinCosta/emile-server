from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_users.models import Users
from cruds.crud_course_sections.models import CourseSections
import datetime
from sqlalchemy import and_
from cruds.crud_student_attendance.models import StudentAttendance
import pdb


section_times = Blueprint("section_times", __name__)


@section_times.route('/section_time_in_progress/<teacher_id>', methods=['GET'])
def section_time_in_progress(teacher_id):
    # Docs
    """
           Section Time in Progress
           ---
           tags:
             - /section_times
           parameters:
              - name: teacher_id
                in: path
                description: teacher id.
                required: true
                type: integer
           responses:
             200:
               description:  This is the service to get the section time in progress to the teacher id
               schema:
                 properties:
                   section_times:
                     type: array
                     description: Section Times list
                     items:
                       type: string
                       default: { "course_section": {
                                                        "code": string,
                                                        "course": {
                                                          "code": string,
                                                          "id": integer,
                                                          "name": string
                                                        },
                                                        "id": 1,
                                                        "name": string,
                                                        "teacher_id": integer
                                                      },
                                                      "id": 1,
                                                      "section_time_finish_time": "HH:MM:SS",
                                                      "section_time_start_time": "HH:MM:SS",
                                                      "week_day": integer}
    """
    section_times = (db.session.query(models.SectionTimes).filter(Users.id == CourseSections.teacher_id).
                       filter(CourseSections.id == models.SectionTimes.course_section_id).
                       filter(Users.id == teacher_id).all())
    return jsonify(section_times=[section_time.serialize() for section_time in section_times])


@section_times.route('/student_attendance_register/<section_time_id>', methods=['POST'])
def student_attendance_register(section_time_id):
    # Docs
    """
           Register of the Student Attendance
           ---
           tags:
             - /section_times
           parameters:
              - name: section_time_id
                in: path
                description: section time id.
                required: true
                type: integer
              - name: student_attendance
                in: body
                description: section time start time.
                required: true
                type: array
                items: {
                  type: string,
                  type: integer
                }
           responses:
             200:
               description:  This is the service to add a new section time in the course section.
               schema:
                 properties:
                   course_section:
                     type: array
                     description: Course Sections list
                     items:
                       type: string
                       default: {"id": integer, "code": string, "name": string, "course": { "code": string, "id": integer, "name": string }, "teacher_id": integer}
    """

    student_attendance_list = request.get_json()['student_attendance']
    try:
        section_time = models.SectionTimes.query.get(section_time_id)
        with db.session.no_autoflush:
            for register in student_attendance_list:
                student_attendance = StudentAttendance(status=register['status'], section_time_date=datetime.datetime.now().date())
                student_attendance.user = Users.query.get(register['student_id'])
                section_time.student_attendance.append(student_attendance)

        db.session.commit()
    except:
        return jsonify(result="Invalid request")
    return jsonify(student_attendance=[student_attendance.serialize() for student_attendance in section_time.student_attendance])


@section_times.route('/update_section_time/<section_time_id>', methods=['POST'])
def update_lesson(section_time_id):
    """ This method allows to update from kwargs """

    section_time = models.SectionTimes.query.get(section_time_id)

    if section_time:
        section_time.set_fields(dict(request.form.items()))
        db.session.commit()
        return jsonify(section_time=[section_time.serialize() for section_time in models.Lesson.query.filter_by(id=section_time_id)])
    return jsonify(result='invalid lesson id')