from backend import db
from cruds.crud_disciplina.models import Disciplina
from cruds.crud_aluno.models import User



aluno_turma= db.Table('aluno_turma',
                             db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), nullable=False),
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
                             db.PrimaryKeyConstraint('turma_id', 'user_id'))


class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    nome = db.Column(db.String(50))
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'))
    alunos = db.relationship('User', secondary=aluno_turma, backref='turmas')
    professor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    aulas = db.relationship("Aula", backref='turma_aula', lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'disciplina_id': Disciplina.query.get(self.disciplina_id).serialize(),
            'professor_id':  self.professor_id,
        }

    def set_fields(self, fields):
        self.codigo = fields['codigo']
        self.nome = fields['nome']
        self.disciplina_id = fields['disciplina_id']
        self.professor_id = fields['professor_id']