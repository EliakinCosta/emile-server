from backend import db
from cruds.crud_disciplina.models import Disciplina
from cruds.crud_aluno.models import User
from cruds.crud_horario.models import Horario
import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func



aluno_turma= db.Table('aluno_turma',
                             db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), nullable=False),
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
                             db.PrimaryKeyConstraint('turma_id', 'user_id'))


class Aula(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    horario_id = db.Column(db.Integer, db.ForeignKey('horario.id'), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    data_aula = db.Column(db.Date())
    child = db.relationship("Horario", back_populates="parents")
    parent = db.relationship("Turma", back_populates="children")

    def serialize(self):
        return {
            'id': self.id,
            'horario': self.child.serialize(),
            'turma': self.parent.serialize(),
            'data_aula': datetime.date.strftime(self.data_aula, "%m-%d-%Y"),
        }


    @hybrid_property
    def horario_inicio_aula(self):
        return datetime.datetime.combine(self.data_aula, self.child.hora_inicio)

    @horario_inicio_aula.expression
    def horario_inicio_aula(cls):
        return db.func.datetime(cls.data_aula, Horario.hora_inicio)

    @hybrid_property
    def horario_fim_aula(self):
        return datetime.datetime.combine(self.data_aula, self.child.hora_fim)

    @horario_fim_aula.expression
    def horario_fim_aula(cls):
        return db.func.datetime(cls.data_aula, Horario.hora_fim)


class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    nome = db.Column(db.String(50))
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'))
    alunos = db.relationship('User', secondary=aluno_turma, backref='turmas')
    professor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    children = db.relationship("Aula", back_populates="parent")

    def serialize(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'disciplina_id': Disciplina.query.get(self.disciplina_id).serialize(),
            'alunos': [aluno.serialize() for aluno in self.alunos if aluno.tipo=='aluno'],
            'professor_id':  self.professor_id
        }

    def set_fields(self, fields):
        self.codigo = fields['codigo']
        self.nome = fields['nome']
        self.disciplina_id = fields['disciplina_id']
        self.professor_id = fields['professor_id']