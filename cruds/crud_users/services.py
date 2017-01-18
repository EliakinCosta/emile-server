from flask import jsonify, Blueprint, request
from . import models
from backend import db


users = Blueprint("user", __name__)


@users.route('/users', methods=['GET'])
def get_users():
    # Docs
    """
           Get all Users
           ---
           tags:
             - /users
           responses:
             200:
               description: This is the view to get all users. Student and Teacher will be returned.
               schema:
                 properties:
                   users:
                     type: array
                     description: User's list
                     items:
                       type: string
                       default: {"id": integer, "username": string}
    """
    return jsonify(users=[dict(id=user.id, username=user.username) for user in models.Users.query.all()])


@users.route('/add_user', methods=['POST'])
def add_users():
    #This method it was implemented considering that all fields are required in client

    # Docs
    """
           Add User
           ---
           tags:
             - /users
           responses:
             200:
               description:  This is the view to add an user.(This user can be student or teacher)
               schema:
                 properties:
                   user:
                     type: array
                     description: User's list
                     items:
                       type: string
                       default: {"id": integer, "username": string, "email":string, "name":string,
                       "birth_date": string, "gender": string, "address": string, "type": string}

    """

    user = models.Users()
    user.set_fields(dict(request.form.items()))

    db.session.add(user)
    db.session.commit()

    return jsonify(user=[user.serialize() for user in models.Users.query.filter_by(username=user.username)])


@users.route('/user_details/<user_id>', methods=['GET'])
def user_details(user_id):
    # Docs
    """
           User Details
           ---
           tags:
             - /users
           responses:
             200:
               description:  This is the view to get details for an user.
               schema:
                 properties:
                   user:
                     type: array
                     description: User object.
                     items:
                       type: string
                       default: {"id": integer, "username": string, "email":string, "name":string,
                       "birth_date": string, "gender": string, "address": string, "type": string}
    """
    return jsonify(user=[user.serialize() for user in models.Users.query.filter_by(id=user_id)])


@users.route('/update_user/<user_id>', methods=['POST'])
def update_user(user_id):
    # Docs
    """
           Update User
           ---
           tags:
             - /users
           responses:
             200:
               description:  This is the view to update an user.(This user can be student or teacher)
               schema:
                 properties:
                   user:
                     type: array
                     description: User Object.
                     items:
                       type: string
                       default: {"id": integer, "username": string, "email":string, "name":string,
                       "birth_date": string, "gender": string, "address": string, "type": string}
    """
    user = models.Users.query.get(user_id)

    if user:
        user.set_fields(dict(request.form.items()))
        db.session.commit()
        return jsonify(user=[user.serialize() for user in models.Users.query.filter_by(id=user_id)])
    return jsonify(result='invalid user id')


@users.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    # Docs
    """
           User Delete
           ---
           tags:
             - /users
           responses:
             200:
               description:  This is the view to delete an user.
               schema:
                 properties:
                   users:
                     type: array
                     description: User's list
                     items:
                       type: string
                       default: {"id": integer, "username": string, "email":string, "name":string,
                       "birth_date": string, "gender": string, "address": string, "type": string}


    """
    user = models.Users.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(users=[user.serialize() for user in models.Users.query.all()])
    return jsonify(result='invalid user id')


@users.route('/teachers_course_sections/<teacher_id>', methods=['GET'])
def teachers_course_sections(teacher_id):
    #Docs
    """
           Course Sections Teacher
           This is the view to get course sections  from a teacher.
           ---
           tags:
             - /users
           responses:
             200:
               description:  This is the view to get course sections  from a teacher.
               schema:
                 properties:
                   classes_teacher:
                     type: array
                     description: User object.
                     items:
                       type: string
                       default: {"id": 1, "teacher_id": integer, "code": string, "name":string, "subject_id":{"id": integer,"code": string,"name": string}}
    """

    teacher = models.Users.query.filter_by(id=teacher_id, type="teacher").first()
    if teacher:
        return jsonify(course_sections_teacher=[course_sections.serialize() for course_sections in teacher.course_sections])
    return jsonify(result='invalid teacher id')


@users.route('/students_course_sections/<student_id>', methods=['GET'])
def students_course_sections(student_id):
    # Docs
    """
           Student's Course Sections
           This is the view to get course sections  from a student.
           ---
           tags:
             - /users
           responses:
             200:
               description:  This is the view to get course sections  from a teacher.
               schema:
                 properties:
                   classes_teacher:
                     type: array
                     description: User object.
                     items:
                       type: string
                       default: {"id": 1, "teacher_id": integer, "code": string, "name":string, "subject_id":{"id": integer,"code": string,"name": string}}
    """

    student = models.Users.query.filter_by(id=student_id, type="student").first()

    if student:
        return jsonify(students_course_sections=[course_sections_students.course_section.serialize() for course_sections_students in student.course_sections])
    return jsonify(result='invalid student id')