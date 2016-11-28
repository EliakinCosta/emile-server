import datetime
from backend import db


class Aula(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    data_inicio_aula = db.Column(db.DateTime())
    data_fim_aula = db.Column(db.DateTime())


    def serialize(self):
        return {
            'id': self.id,
            'data_inicio_aula': datetime.date.strftime(self.data_inicio_aula, "%m-%d-%Y %H:%M:%S"),
            'data_fim_aula': datetime.date.strftime(self.data_fim_aula, "%m-%d-%Y %H:%M:%S"),
            'turma': self.turma_aula.serialize(),
        }

    def set_fields(self, fields):
        self.turma_id = fields['turma_id']
        self.data_inicio_aula = fields['data_inicio_aula']
        self.data_fim_aula = fields['data_fim_aula']