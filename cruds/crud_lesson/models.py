import datetime
from backend import db
from cruds.crud_frequency.models import Frequency


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classes_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    lesson_start_date = db.Column(db.DateTime())
    lesson_finish_date = db.Column(db.DateTime())
    frequency = db.relationship("Frequency")
    frequency_status = db.Column(db.Boolean(), default=False)


    def serialize(self):
        return {
            'id': self.id,
            'lesson_start_date': datetime.date.strftime(self.lesson_start_date, "%m-%d-%Y-%H:%M:%S"),
            'lesson_finish_date': datetime.date.strftime(self.lesson_finish_date, "%m-%d-%Y-%H:%M:%S"),
            'classes': self.classes_lesson.serialize(),
            'frequency_status': self.frequency_status
        }

    def set_fields(self, fields):
        self.classes_id = fields['classes_id']
        self.lesson_start_date = datetime.datetime.strptime(fields['lesson_start_date'],  "%d/%m/%Y-%H:%M:%S")
        self.lesson_finish_date = datetime.datetime.strptime(fields['lesson_finish_date'], "%d/%m/%Y-%H:%M:%S")
        self.frequency_status = fields['frequency_status']