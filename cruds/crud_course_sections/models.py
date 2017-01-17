from backend import db
from cruds.crud_courses.models import Courses
from cruds.crud_users.models import Users


class CourseSections(db.Model):
    __tablename__ = 'course_sections'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(50))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    section_times = db.relationship("SectionTimes", backref='course_section', lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'course': Courses.query.get(self.course_id).serialize(),
            'teacher_id':  self.teacher_id
        }

    def set_fields(self, fields):
        self.code = fields['code']
        self.name = fields['name']
        self.course_id = fields['course_id']
        self.teacher_id = fields['teacher_id']