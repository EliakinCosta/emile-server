from backend import db
import datetime

class Horario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Time())
    hora_fim = db.Column(db.Time())
    parents = db.relationship("Aula", back_populates="child")

    def serialize(self):
        return {
            'id': self.id,
            'hora_inicio': self.hora_inicio.strftime('%H:%M:%S'),
            'hora_fim': self.hora_fim.strftime('%H:%M:%S'),
        }

    def set_fields(self, fields):
        FMT = '%H:%M:%S'
        hora_inicio = datetime.datetime.strptime(fields['hora_inicio'], FMT).time()
        hora_fim = datetime.datetime.strptime(fields['hora_fim'], FMT).time()
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim