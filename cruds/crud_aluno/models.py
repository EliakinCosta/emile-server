import datetime
from backend import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(250))
    birth_date = db.Column(db.Date())
    gender = db.Column(db.String(1))
    address = db.Column(db.String(250))
    tipo = db.Column(db.String(50))
    _turmas = db.relationship('Turma', backref='professor', lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'birth_date': datetime.date.strftime(self.birth_date, "%m-%d-%Y"),
            'gender': self.gender,
            'address': self.address,
            'tipo': self.tipo,
            'turmas': [turma.serialize() for turma in self._turmas.all()]
        }

    def set_fields(self, fields):
        self.username = fields['username']
        self.email = fields['email']
        self.name = fields['name']
        self.birth_date = fields['birth_date']
        self.gender = fields['gender']
        self.address = fields['address']
        self.birth_date = datetime.datetime.strptime(fields['birth_date'], "%m-%d-%Y").date()
        self.tipo = fields['tipo']
