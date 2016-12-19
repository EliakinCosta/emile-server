from flask import Blueprint, jsonify, request
from . import models
from backend import db


subject = Blueprint("subject", __name__)


@subject.route('/subjects', methods=['GET'])
def get_subjects():
    # Docs
    """
           Get all Subjects.
           ---
           tags:
             - /subjects
           responses:
             200:
               description: This is the view to get all subjects.
               schema:
                 properties:
                   subjects:
                     type: array
                     description: Subject's list
                     items:
                       type: string
                       default: {"id": integer, "code": string}
       """
    return jsonify(subjects=[dict(id=subject.id, code=subject.code) for subject in models.Subject.query.all()])


@subject.route('/add_subject', methods=['POST'])
def add_subject():

    # Docs
    """
           Add Subject.
           ---
           tags:
             - /subjects
           parameters:
              - name: code
                in: formData
                description: code of subject.
                required: true
                type: string
              - name: name
                in: formData
                description: name of subject.
                required: true
                type: string
           responses:
             200:
               description:  This is the view to add an subject.
               schema:
                 properties:
                   subject:
                     type: array
                     description: Subject's list
                     items:
                       type: string
                       default: {"id": integer, "code": string, "name": string}

       """
    subject = models.Subject()
    subject.set_fields(dict(request.form.items()))

    db.session.add(subject)
    db.session.commit()

    return jsonify(subject=[subject.serialize() for subject in models.Subject.query.filter_by(code=subject.code)])


@subject.route('/subject_details/<subject_id>', methods=['GET'])
def subject_details(subject_id):

    # Docs
    """
           Subject Details
           ---
           tags:
             - /subjects
           parameters:
              - name: subject_id
                in: path
                description: id of Subject.
                required: true
                type: integer
           responses:
             200:
               description:  This is the view to get details for a Subject.
               schema:
                 properties:
                   subject:
                     type: array
                     description: Subject object.
                     items:
                       type: string
                       default: {"id": integer, "code": string, "name": string}
       """

    return jsonify(subject=[subject.serialize() for subject in models.Subject.query.filter_by(id=subject_id)])