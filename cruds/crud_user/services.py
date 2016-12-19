from flask import jsonify, Blueprint, request
from . import models
from backend import db


user = Blueprint("user", __name__)


@user.route('/users', methods=['GET'])
def get_users():

    #Docs
    """
           Get all Users.
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
    return jsonify(users=[dict(id=user.id, username=user.username) for user in models.User.query.all()])


@user.route('/add_user', methods=['POST'])
def add_users():
    #This method it was implemented considering that all fields are required in client

    # Docs
    """
           Add User.
           ---
           tags:
             - /users
           parameters:
              - name: username
                in: formData
                description: username of user.
                required: true
                type: string
              - name: email
                in: formData
                description: email of user.
                required: true
                type: string
              - name: name
                in: formData
                description: name of user.
                required: true
                type: string
              - name: birth_date
                in: formData
                description: birth date of user. (m-d-Y)
                required: true
                type: string
              - name: gender
                in: formData
                description: gender of user (M of F)
                required: true
                type: string
              - name: address
                in: formData
                description: address of user.
                required: true
                type: string
              - name: type
                in: formData
                description: type of user. (student or teacher)
                required: true
                type: string
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
    user = models.User()
    user.set_fields(dict(request.form.items()))

    db.session.add(user)
    db.session.commit()

    return jsonify(user=[user.serialize() for user in models.User.query.filter_by(username=user.username)])


@user.route('/user_details/<user_id>', methods=['GET'])
def user_details(user_id):

    # Docs
    """
           User Details
           ---
           tags:
             - /users
           parameters:
              - name: user_id
                in: path
                description: id of user.
                required: true
                type: integer
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
    return jsonify(user=[user.serialize() for user in models.User.query.filter_by(id=user_id)])


@user.route('/update_user/<user_id>', methods=['POST'])
def update_user(user_id):

    #This method allows to update from kwargs

    # Docs
    """
           Update User.
           ---
           tags:
             - /users
           parameters:
              - name: user_id
                in: path
                description: id of user.
                required: true
                type: integer
              - name: username
                in: formData
                description: username of user.
                required: true
                type: string
              - name: email
                in: formData
                description: email of user.
                required: true
                type: string
              - name: name
                in: formData
                description: name of user.
                required: true
                type: string
              - name: birth_date
                in: formData
                description: birth date of user. (m-d-Y)
                required: true
                type: string
              - name: gender
                in: formData
                description: gender of user (M of F)
                required: true
                type: string
              - name: address
                in: formData
                description: address of user.
                required: true
                type: string
              - name: type
                in: formData
                description: type of user. (student or teacher)
                required: true
                type: string
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

    user = models.User.query.get(user_id)

    if user:
        user.set_fields(dict(request.form.items()))
        db.session.commit()
        return jsonify(user=[user.serialize() for user in models.User.query.filter_by(id=user_id)])
    return jsonify(result='invalid user id')


@user.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):

    # Docs
    """
           User Delete
           ---
           tags:
             - /users
           parameters:
              - name: user_id
                in: path
                description: id of user.
                required: true
                type: integer
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
    user = models.User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(users=[user.serialize() for user in models.User.query.all()])
    return jsonify(result='invalid user id')


@user.route('/classes_teacher/<teacher_id>', methods=['GET'])
def classes_teacher(teacher_id):
    # Docs
    """
           Classes Teacher
           ---
           tags:
             - /users
           parameters:
              - name: teacher_id
                in: path
                description: id of teacher.
                required: true
                type: integer
           responses:
             200:
               description:  This is the view to get classes of teacher.
               schema:
                 properties:
                   classes_teacher:
                     type: array
                     description: User object.
                     items:
                       type: string
                       default: {"id": 1, "teacher_id": integer, "code": string, "name":string, "subject_id":{"id": integer,"code": string,"name": string}}
       """
    teacher = models.User.query.filter_by(id=teacher_id, type="teacher").first()
    if teacher:
        return jsonify(classes_teacher=[classes.serialize() for classes in teacher._classes.all()])
    return jsonify(result='invalid teacher id')
