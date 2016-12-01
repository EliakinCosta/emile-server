from flask import jsonify, Blueprint, request
from . import models
import datetime
from backend import db


user = Blueprint("user", __name__)


@user.route('/users', methods=['GET'])
def get_users():
    """
        Get all Users.
        ---
        tags:
          - /users
        responses:
          200:
            description: This is the view to get all users. Aluno and Professo will be returned.
            schema:
              id: id
              properties:
                username:
                  type: string
                  description: The User name
                id:
                  type: int
                  description: The User id
    """
    return jsonify(users=[dict(id=user.id, username=user.username) for user in models.User.query.all()])


@user.route('/add_user', methods=['POST'])
def add_users():
    """ This method it was implemented considering that all fields are required in client """

    user = models.User()
    user.set_fields(dict(request.form.items()))

    db.session.add(user)
    db.session.commit()

    return jsonify(user=[user.serialize() for user in models.User.query.filter_by(username=user.username)])


@user.route('/user_details/<user_id>', methods=['GET'])
def user_details(user_id):
    return jsonify(user=[user.serialize() for user in models.User.query.filter_by(id=user_id)])


@user.route('/update_user/<user_id>', methods=['POST'])
def update_user(user_id):
    """ This method allows to update from kwargs """

    user = models.User.query.get(user_id)

    if user:
        user.set_fields(dict(request.form.items()))
        db.session.commit()
        return jsonify(user=[user.serialize() for user in models.User.query.filter_by(id=user_id)])
    return jsonify(result='invalid user id')


@user.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    user = models.User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(users=[user.serialize() for user in models.User.query.all()])
    return jsonify(result='invalid user id')


