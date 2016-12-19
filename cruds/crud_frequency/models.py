from backend import db
import datetime
from cruds.crud_user.models import User


class Frequency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.String(1))
    created = db.Column(db.DateTime(), default=datetime.datetime.now)
    user = db.relationship("User")

    def serialize(self):
        return {
            'id': self.id,
            'lesson_id': self.lesson_id,
            'user_id': self.user_id,
            'status': self.status,
            'created':  self.created
        }


