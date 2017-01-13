from backend import db
import datetime
from cruds.crud_users.models import Users


class StudentAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_time_id = db.Column(db.Integer, db.ForeignKey('section_times.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(1))
    section_time_date = db.Column(db.Date())
    user = db.relationship("Users")

    def serialize(self):
        return {
            'id': self.id,
            'section_time_id': self.section_time_id,
            'user_id': self.user_id,
            'status': self.status,
            'section_time_date':  datetime.date.strftime(self.section_time_date, "%m-%d-%Y")
        }


