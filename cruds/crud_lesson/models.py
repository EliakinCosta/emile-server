import datetime
from backend import db
from cruds.crud_frequency.models import Frequency


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classes_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    week_day = db.Column(db.Integer())
    lesson_start_time = db.Column(db.Time())
    lesson_finish_time = db.Column(db.Time())
    frequency = db.relationship("Frequency")
    frequency_status = db.Column(db.Boolean(), default=False)


    def serialize(self):
        return {
            'id': self.id,
            'week_day': self.week_day,
            'lesson_start_time': self.lesson_start_time.strftime("%H:%M:%S"),
            'lesson_finish_time':self.lesson_finish_time.strftime("%H:%M:%S"),
            'classes': self.classes_lesson.serialize(),
            'frequency_status': self.frequency_status
        }

    def set_fields(self, fields):
        self.classes_id = fields['classes_id']
        self.lesson_start_date = datetime.time.strptime("%H:%M:%S",fields['lesson_start_time'])
        self.lesson_finish_date = datetime.time.strptime("%H:%M:%S", fields['lesson_finish_time'])
        self.week_day = fields['week_day']
        self.frequency_status = fields['frequency_status']