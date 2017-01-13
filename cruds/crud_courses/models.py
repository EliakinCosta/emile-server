from backend import db


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(50))
    course_sections = db.relationship('CourseSections', backref='course', lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
        }

    def set_fields(self, fields):
        self.code = fields['code']
        self.name = fields['name']