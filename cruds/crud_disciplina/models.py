from backend import db


class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    nome = db.Column(db.String(50))
    turmas = db.relationship('Turma', backref='disciplina', lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
        }

    def set_fields(self, fields):
        self.codigo = fields['codigo']
        self.nome = fields['nome']