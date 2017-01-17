from flask import Blueprint, jsonify
from . import models
from cruds.crud_users.models import Users
from cruds.crud_course_sections.models import CourseSections
from cruds.crud_course_section_students.models import CourseSectionStudents
from backend import db


student_attendance = Blueprint("student_attendance", __name__)


@student_attendance.route('/students_attendance/<course_section_id>/<student_id>', methods=["GET"])
def students_attendance(course_section_id, student_id):
    # Docs
    """
           Student's Attendance
           ---
           tags:
             - /students_attendance
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
                       default: {
                                  "students_attendance": [
                                    {
                                      "course_section_student_id": integer,
                                      "id": integer,
                                      "section_time_date": string(mm/dd/YYYY),
                                      "section_time_id": integer,
                                      "status": string(P or F)
                                    }
                                  ]
                                }
    """
    students_attendance_list = (db.session.query(models.StudentAttendance).
                                 filter(models.StudentAttendance.course_section_student_id == CourseSectionStudents.id).
                                 filter(CourseSectionStudents.course_section_id == course_section_id).
                                 filter(CourseSectionStudents.user_id == student_id).all())

    return jsonify(students_attendance=[student_attendance.serialize() for student_attendance in students_attendance_list])