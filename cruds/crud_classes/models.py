from backend import db
from cruds.crud_subject.models import Subject
from cruds.crud_user.models import User


student_class = db.Table('student_classes',
                       db.Column('classes_id', db.Integer, db.ForeignKey('classes.id'), nullable=False),
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
                       db.PrimaryKeyConstraint('classes_id', 'user_id'))


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(50))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    students = db.relationship('User', secondary=student_class, backref='classes')
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lessons =  db.relationship("Lesson", backref='classes_lesson', lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'subject_id': Subject.query.get(self.subject_id).serialize(),
            'teacher_id':  self.teacher_id
        }

    def set_fields(self, fields):
        self.code = fields['code']
        self.name = fields['name']
        self.subject_id = fields['subject_id']
        self.teacher_id = fields['teacher_id']