from backend import db
from cruds.crud_courses.models import Courses


class CourseSectionStudents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_section_id = db.Column(db.Integer, db.ForeignKey('course_sections.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_section = db.relationship("CourseSections")

    def serialize(self):
        return {
            'course_section_id': self.course_section_id,
            'user_id': self.user_id,
        }